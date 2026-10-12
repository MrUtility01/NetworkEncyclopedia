# -*- coding: utf-8 -*-
"""سرور وب + API همگام‌سازی LAN — فهرست دروس عمومی؛ Sync با توکن."""
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

_MODULE_STATUS = {"workspace": False, "study": False, "workspace_error": "", "study_error": ""}

try:
    from workspace_routes import bp as workspace_bp, set_auth_checker
    app.register_blueprint(workspace_bp)
    _MODULE_STATUS["workspace"] = True
except Exception as _e:
    _MODULE_STATUS["workspace_error"] = str(_e)
    print("workspace routes skipped", _e)

try:
    from study_routes import register_study_routes
except Exception as _e:
    register_study_routes = None
    _MODULE_STATUS["study_error"] = str(_e)

DEFAULT_DEV_TOKEN = "09136555866"
SYNC_TOKEN = os.environ.get("NETENC_TOKEN", DEFAULT_DEV_TOKEN)
DEVICE_ID = os.environ.get("NETENC_DEVICE", socket.gethostname() or "windows-host")
BIND_HOST = os.environ.get("NETENC_HOST", "0.0.0.0")

if SYNC_TOKEN == DEFAULT_DEV_TOKEN:
    print("WARNING: using default NETENC_TOKEN — set env NETENC_TOKEN for production")

_db = None


def db() -> WebDB:
    global _db
    if _db is None:
        _db = WebDB()
        if not _db.is_seeded():
            print("seed curriculum (rich content) — may take a few minutes...")
            print(_db.seed_full(force=True))
        _db.ensure_sync_columns()
    return _db


def extract_token() -> str:
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        return auth[7:].strip()
    t = request.headers.get("X-NetEnc-Token", "") or ""
    if t:
        return t.strip()
    t = request.cookies.get("netenc_token") or request.args.get("token") or ""
    return (t or "").strip()


def check_token() -> bool:
    if not SYNC_TOKEN:
        return False
    return extract_token() == SYNC_TOKEN


def require_token():
    if check_token():
        return None
    return jsonify({"ok": False, "error": "unauthorized", "hint": "Authorization: Bearer <NETENC_TOKEN>"}), 401


if _MODULE_STATUS["workspace"]:
    try:
        set_auth_checker(check_token, extract_token, SYNC_TOKEN)
    except Exception as e:
        print("workspace auth wire", e)


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/health")
def health():
    st = {}
    try:
        st = db().stats()
    except Exception as e:
        st = {"error": str(e)}
    return jsonify({
        "ok": True,
        "device": DEVICE_ID,
        "schema_version": SCHEMA_VERSION,
        "sync_protocol": "v1-aligned",
        "token_required_for_sync": bool(SYNC_TOKEN),
        "default_token_in_use": SYNC_TOKEN == DEFAULT_DEV_TOKEN,
        "modules": {
            "workspace": _MODULE_STATUS["workspace"],
            "study": bool(register_study_routes),
            "workspace_error": _MODULE_STATUS.get("workspace_error") or None,
            "study_error": _MODULE_STATUS.get("study_error") or None,
        },
        "stats": st,
    })


@app.get("/api/stats")
def api_stats():
    return jsonify(db().stats())


@app.get("/api/chapters")
def chapters():
    return jsonify(db().list_chapters())


@app.get("/api/chapters/<int:chapter_id>/levels")
def chapter_levels(chapter_id: int):
    levels = db().list_levels(chapter_id)
    return jsonify({"levels": levels, "count": len(levels)})


@app.get("/api/levels/<int:level_id>/lessons")
def level_lessons(level_id: int):
    lessons = db().list_lessons(level_id)
    return jsonify({"lessons": lessons, "count": len(lessons)})


@app.get("/api/lessons/<int:lesson_id>")
def lesson_by_id(lesson_id: int):
    row = db().get_lesson(lesson_id)
    if not row:
        return jsonify({"error": "not found"}), 404
    return jsonify(row)


@app.get("/api/lessons")
def lessons_query():
    level_id = request.args.get("level_id") or request.args.get("chapter_id")
    try:
        lid = int(level_id) if level_id else None
    except ValueError:
        lid = None
    if lid is None:
        return jsonify({"lessons": []})
    lessons = db().list_lessons(lid)
    return jsonify({"lessons": lessons, "count": len(lessons)})


@app.get("/api/scenarios")
def scenarios():
    return jsonify(db().list_scenarios())


@app.get("/api/scenarios/<int:sid>")
def scenario_one(sid: int):
    row = db().get_scenario(sid)
    if not row:
        return jsonify({"error": "not found"}), 404
    return jsonify(row)


@app.get("/api/infographics")
def api_infographics():
    try:
        from core.infographics import all_infographics
        items = [{"title": t, "svg": s} for t, s in all_infographics()]
    except Exception as e:
        return jsonify({"items": [], "error": str(e)})
    return jsonify({"items": items, "count": len(items)})


@app.get("/api/search")
def search():
    q = request.args.get("q") or ""
    return jsonify(db().search(q))


@app.post("/api/apply-packs")
def apply_packs():
    """اعمال محتوای واقعی JSON پک‌ها روی درس‌های موجود بدون پاک کردن کل DB."""
    denied = require_token()
    if denied:
        return denied
    try:
        from core.pack_loader import apply_packs_to_db
        result = apply_packs_to_db(Path(db().path), overwrite=True)
        db().set_meta("packs_applied", "v1")
        return jsonify(result)
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.post("/api/reseed")
def reseed():
    denied = require_token()
    if denied:
        return denied
    result = db().seed_full(force=True)
    try:
        from core.pack_loader import apply_packs_to_db
        packs = apply_packs_to_db(Path(db().path), overwrite=True)
        result["packs"] = packs
        db().set_meta("packs_applied", "v1")
    except Exception as e:
        result["packs_error"] = str(e)
    return jsonify(result)


@app.get("/api/sync/hello")
def sync_hello():
    denied = require_token()
    if denied:
        return denied
    st = {}
    try:
        st = db().stats()
    except Exception:
        pass
    lan = ""
    try:
        lan = socket.gethostbyname(socket.gethostname())
    except Exception:
        pass
    return jsonify({
        "ok": True,
        "schema_version": SCHEMA_VERSION,
        "device_id": DEVICE_ID,
        "lan_ip": lan,
        "stats": st,
        "protocol": {
            "hello": "GET /api/sync/hello",
            "manifest": "GET /api/sync/manifest?since=",
            "pull": "POST /api/sync/pull {uids:[]}",
            "push": "POST /api/sync/push {records:[]}",
            "auth": "Authorization: Bearer <token> or X-NetEnc-Token",
        },
    })


@app.get("/api/sync/manifest")
def sync_manifest():
    denied = require_token()
    if denied:
        return denied
    since = request.args.get("since") or None
    records = db().sync_index()
    return jsonify(build_manifest(records, since=since))


@app.post("/api/sync/pull")
def sync_pull():
    denied = require_token()
    if denied:
        return denied
    body = request.get_json(force=True, silent=True) or {}
    uids = body.get("uids") or []
    if not isinstance(uids, list):
        return jsonify({"error": "uids must be a list"}), 400
    records = db().sync_pull(uids)
    return jsonify({"records": records, "count": len(records), "generated_at": utc_now()})


@app.post("/api/sync/push")
def sync_push():
    denied = require_token()
    if denied:
        return denied
    body = request.get_json(force=True, silent=True) or {}
    records = body.get("records") or body.get("items") or []
    if not isinstance(records, list):
        return jsonify({"error": "records must be a list"}), 400
    accepted = kept = conflicts = 0
    conflict_uids = []
    index = {r["uid"]: r for r in db().sync_index()}
    to_apply = []
    for item in records:
        if not isinstance(item, dict):
            continue
        uid = item.get("uid") or ""
        if not uid:
            continue
        server = index.get(uid) or {}
        decision = compare_lww(server, item)
        if decision == "accept_client":
            to_apply.append(item)
            accepted += 1
        elif decision == "conflict":
            conflicts += 1
            conflict_uids.append(uid)
            kept += 1
        else:
            kept += 1
    if to_apply:
        db().sync_apply(to_apply)
    return jsonify({
        "accepted": accepted,
        "kept": kept,
        "conflicts": conflicts,
        "conflict_uids": conflict_uids,
        "server_time": utc_now(),
    })


def main():
    host = BIND_HOST
    port = int(os.environ.get("NETENC_PORT", "5050"))
    print("init db / rich seed if needed...")
    d = db()
    # محتوای واقعی پک‌های JSON را یک‌بار روی درس‌ها بنویس
    try:
        if d.get_meta("packs_applied") != "v1":
            from core.pack_loader import apply_packs_to_db
            print("applying REAL JSON pack content into lessons...")
            res = apply_packs_to_db(Path(d.path), overwrite=True)
            print("pack apply:", res.get("updated"), "updated /", res.get("matched"), "matched")
            d.set_meta("packs_applied", "v1")
    except Exception as e:
        print("pack apply skipped:", e)
    if register_study_routes:
        try:
            register_study_routes(app, db)
            _MODULE_STATUS["study"] = True
        except Exception as e:
            _MODULE_STATUS["study_error"] = str(e)
            print("study routes", e)
    print(f"NetEnc listening on http://{host}:{port}")
    app.run(host=host, port=port, debug=False, threaded=True)


if __name__ == "__main__":
    main()
