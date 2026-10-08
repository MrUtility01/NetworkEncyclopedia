# -*- coding: utf-8 -*-
"""سرور وب + API همگام‌سازی LAN + مطالعه — میزبان ویندوز."""
from __future__ import annotations

import hashlib
import json
import os
import socket
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, jsonify, render_template, request

from core.db import WebDB

try:
    from shared.sync_engine import SCHEMA_VERSION, build_manifest, compare_lww, content_hash, utc_now
except Exception:
    SCHEMA_VERSION = 1

    def utc_now():
        return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    def content_hash(payload):
        keys = sorted(k for k in payload.keys() if k not in ("device_id", "last_updated", "content_hash"))
        blob = json.dumps({k: payload[k] for k in keys}, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(blob.encode("utf-8")).hexdigest()

    def compare_lww(server, client):
        su, cu = server.get("last_updated") or "", client.get("last_updated") or ""
        sh, ch = server.get("content_hash") or "", client.get("content_hash") or content_hash(client)
        if cu > su:
            return "accept_client"
        if cu < su:
            return "keep_server"
        if sh == ch:
            return "equal"
        return "conflict"

    def build_manifest(records, since=None):
        items = []
        for r in records:
            if since and (r.get("last_updated") or "") <= since:
                continue
            items.append({
                "uid": r["uid"], "entity": r.get("entity", "lesson"),
                "last_updated": r.get("last_updated"), "content_hash": r.get("content_hash"),
                "deleted": bool(r.get("deleted")),
            })
        return {"schema_version": SCHEMA_VERSION, "generated_at": utc_now(), "items": items}


BASE = Path(__file__).resolve().parent
app = Flask(__name__, template_folder=str(BASE / "templates"), static_folder=str(BASE / "static"))
app.config["JSON_AS_ASCII"] = False

try:
    from study_routes import register_study_routes
except Exception:
    register_study_routes = None

SYNC_TOKEN = os.environ.get("NETENC_TOKEN", "09136555866")
DEVICE_ID = os.environ.get("NETENC_DEVICE", socket.gethostname() or "windows-host")

_db = None


def db() -> WebDB:
    global _db
    if _db is None:
        _db = WebDB()
        if not _db.is_seeded():
            print("seed 63 chapters...")
            print(_db.seed_full(force=True))
        _db.ensure_sync_columns()
    return _db


def check_token():
    if not SYNC_TOKEN:
        return True
    return request.headers.get("X-NetEnc-Token") == SYNC_TOKEN


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/stats")
def api_stats():
    s = db().stats()
    s["device_id"] = DEVICE_ID
    s["lan_hint"] = _lan_ip()
    return jsonify(s)


@app.route("/api/chapters")
def api_chapters():
    return jsonify(db().list_chapters())


@app.route("/api/chapters/<int:chapter_id>/levels")
def api_levels(chapter_id):
    ch = db().get_chapter(chapter_id)
    if not ch:
        return jsonify({"error": "not found"}), 404
    return jsonify({"chapter": ch, "levels": db().list_levels(chapter_id)})


@app.route("/api/levels/<int:level_id>/lessons")
def api_lessons(level_id):
    return jsonify({"lessons": db().list_lessons(level_id)})


@app.route("/api/lessons/<int:lesson_id>")
def api_lesson(lesson_id):
    les = db().get_lesson(lesson_id)
    if not les:
        return jsonify({"error": "not found"}), 404
    return jsonify(les)


@app.route("/api/scenarios")
def api_scenarios():
    return jsonify(db().list_scenarios())


@app.route("/api/scenarios/<int:sid>")
def api_scenario(sid):
    sc = db().get_scenario(sid)
    if not sc:
        return jsonify({"error": "not found"}), 404
    return jsonify(sc)


@app.route("/api/search")
def api_search():
    return jsonify(db().search(request.args.get("q", "")))


@app.route("/api/sources")
def api_sources():
    try:
        from core.sources_catalog import DEFAULT_SOURCES
        return jsonify({"sources": DEFAULT_SOURCES})
    except Exception as e:
        return jsonify({"sources": [], "error": str(e)})


@app.route("/api/reseed", methods=["POST"])
def api_reseed():
    info = db().seed_full(force=True)
    db().ensure_sync_columns()
    return jsonify(info)


@app.route("/api/sync/hello")
def sync_hello():
    return jsonify({
        "ok": True,
        "schema_version": SCHEMA_VERSION,
        "device_id": DEVICE_ID,
        "lan_ip": _lan_ip(),
        "stats": db().stats(),
    })


@app.route("/api/sync/manifest")
def sync_manifest():
    if not check_token():
        return jsonify({"error": "unauthorized"}), 401
    since = request.args.get("since")
    records = db().sync_index()
    return jsonify(build_manifest(records, since=since))


@app.route("/api/sync/pull", methods=["POST"])
def sync_pull():
    if not check_token():
        return jsonify({"error": "unauthorized"}), 401
    body = request.get_json(force=True, silent=True) or {}
    uids = body.get("uids") or []
    return jsonify({"records": db().sync_pull(uids)})


@app.route("/api/sync/push", methods=["POST"])
def sync_push():
    if not check_token():
        return jsonify({"error": "unauthorized"}), 401
    body = request.get_json(force=True, silent=True) or {}
    client_records = body.get("records") or []
    server_list = db().sync_index()
    server_by_uid = {r["uid"]: r for r in server_list}

    applied, rejected, conflicts = [], [], []
    full_applied = []
    for c in client_records:
        uid = c.get("uid")
        if not uid:
            continue
        if not c.get("content_hash"):
            c["content_hash"] = content_hash(c)
        s = server_by_uid.get(uid)
        if s is None:
            applied.append(uid)
            full_applied.append(c)
            continue
        decision = compare_lww(
            {"last_updated": s.get("last_updated"), "content_hash": s.get("content_hash")},
            c,
        )
        if decision == "accept_client":
            applied.append(uid)
            full_applied.append(c)
        elif decision in ("keep_server", "equal"):
            rejected.append({"uid": uid, "reason": decision})
        else:
            conflicts.append({"uid": uid, "reason": "conflict"})

    if full_applied:
        db().sync_apply(full_applied)

    return jsonify({
        "applied": applied,
        "rejected": rejected,
        "conflicts": conflicts,
        "server_time": utc_now(),
    })


def _lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


if register_study_routes:
    register_study_routes(app, db)


def main():
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "5050"))
    db()
    print(f"LAN: http://{_lan_ip()}:{port}")
    print(f"Local: http://127.0.0.1:{port}")
    app.run(host=host, port=port, debug=False)


if __name__ == "__main__":
    main()
