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
    from workspace_routes import bp as workspace_bp
    app.register_blueprint(workspace_bp)
except Exception as _e:
    print("workspace routes skipped", _e)

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
    auth = request.headers.get("Authorization", "")
    token = auth[7:].strip() if auth.startswith("Bearer ") else request.headers.get("X-NetEnc-Token", "")
    return token == SYNC_TOKEN


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/health")
def health():
    return jsonify({"ok": True, "device": DEVICE_ID, "schema": SCHEMA_VERSION})


@app.get("/api/chapters")
def chapters():
    return jsonify(db().list_chapters())


@app.get("/api/lessons")
def lessons():
    chapter_id = request.args.get("chapter_id")
    return jsonify(db().list_lessons(chapter_id=chapter_id))


@app.get("/api/lesson/<uid>")
def lesson(uid: str):
    row = db().get_lesson(uid)
    if not row:
        return jsonify({"error": "not found"}), 404
    return jsonify(row)


@app.post("/api/sync/pull")
def sync_pull():
    if not check_token():
        return jsonify({"error": "unauthorized"}), 401
    body = request.get_json(force=True, silent=True) or {}
    since = body.get("since")
    records = db().export_sync_records(since=since)
    return jsonify(build_manifest(records, since=since))


@app.post("/api/sync/push")
def sync_push():
    if not check_token():
        return jsonify({"error": "unauthorized"}), 401
    body = request.get_json(force=True, silent=True) or {}
    items = body.get("items") or []
    accepted = kept = conflicts = 0
    for item in items:
        server = db().get_sync_record(item.get("uid"))
        decision = compare_lww(server or {}, item) if server else "accept_client"
        if decision == "accept_client":
            db().upsert_sync_record(item)
            accepted += 1
        elif decision == "keep_server":
            kept += 1
        elif decision == "conflict":
            conflicts += 1
        else:
            kept += 1
    return jsonify({"accepted": accepted, "kept": kept, "conflicts": conflicts})


def main():
    host = os.environ.get("NETENC_HOST", "0.0.0.0")
    port = int(os.environ.get("NETENC_PORT", "5050"))
    db()
    if register_study_routes:
        try:
            register_study_routes(app, db)
        except Exception as e:
            print("study routes", e)
    print(f"NetEnc listening on http://{host}:{port}")
    app.run(host=host, port=port, debug=False)


if __name__ == "__main__":
    main()
