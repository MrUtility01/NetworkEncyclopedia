# -*- coding: utf-8 -*-
"""سرور وب + API همگام‌سازی LAN — bind روی 0.0.0.0 — پورت پیش‌فرض 83."""
from __future__ import annotations

import hashlib
import json
import os
import socket
import sys
import threading
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, jsonify, render_template, request


def _configure_console_encoding():
    """Prevent Windows cp1252 consoles from crashing on Persian lesson text."""
    for stream in (sys.stdout, sys.stderr):
        if stream is None or not hasattr(stream, "reconfigure"):
            continue
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (OSError, ValueError):
            pass


_configure_console_encoding()

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

DEFAULT_DEV_TOKEN = "engineerjokar"
SYNC_TOKEN = os.environ.get("NETENC_TOKEN", DEFAULT_DEV_TOKEN)
DEVICE_ID = os.environ.get("NETENC_DEVICE", socket.gethostname() or "windows-host")
BIND_HOST = os.environ.get("NETENC_HOST", "0.0.0.0")
BIND_PORT = int(os.environ.get("NETENC_PORT", "83"))

if SYNC_TOKEN == DEFAULT_DEV_TOKEN:
    print("WARNING: using default NETENC_TOKEN — set env NETENC_TOKEN for production")

_db = None


def get_lan_ips():
    ips = []
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.3)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        if ip and not ip.startswith("127."):
            ips.append(ip)
    except Exception:
        pass
    try:
        hostname = socket.gethostname()
        for info in socket.getaddrinfo(hostname, None, socket.AF_INET):
            ip = info[4][0]
            if ip and not ip.startswith("127.") and ip not in ips:
                ips.append(ip)
    except Exception:
        pass
    if not ips:
        ips = ["127.0.0.1"]
    return ips


PACK_CONTENT_VERSION = "v36-ch36-ch37-ch38-ch39"

def _apply_content_packs_if_needed(database: WebDB, force: bool = False):
    """Apply and verify required lesson packs only after the full lesson seed completes."""
    if not force and database.get_meta("packs_applied") == PACK_CONTENT_VERSION:
        return {"ok": True, "skipped": True, "version": PACK_CONTENT_VERSION}
    if not database.is_seeded():
        return {"ok": False, "pending": True, "reason": "seed_not_complete"}

    required = {
        "ch36_linux_admin_professional.json": 45,
        "ch37_linux_network_professional.json": 45,
        "ch38_linux_web_services_professional.json": 40,
        "ch39_linux_security_professional.json": 45,
    }
    try:
        from core.pack_loader import apply_packs_to_db
        print("applying versioned content packs (chapters 36-39 are authoritative)...")
        res = apply_packs_to_db(Path(database.path), overwrite=False)
        print("pack apply:", res.get("updated"), "updated /", res.get("matched"), "matched",
              "skipped_shorter", res.get("skipped_shorter"))
        details = {item.get("pack"): item for item in (res.get("details") or [])}
        bad = []
        for name, expected in required.items():
            item = details.get(name)
            if not item or item.get("matched") != expected or item.get("updated") != expected or item.get("missing") != 0:
                bad.append({"pack": name, "expected": expected, "actual": item})
        if not res.get("ok") or bad:
            print("required content pack verification failed; version marker not updated:", bad)
            return {"ok": False, "error": "required_content_pack_verification_failed", "details": bad, "result": res}
        database.set_meta("packs_applied", PACK_CONTENT_VERSION)
        return {"ok": True, "version": PACK_CONTENT_VERSION, "result": res}
    except Exception as exc:
        print("pack apply skipped:", exc)
        return {"ok": False, "error": str(exc)}

def db() -> WebDB:
    global _db
    if _db is None:
        _db = WebDB()
        if _db.chapter_count() < 65:
            print("skeleton chapters 1-68 (fast)...")
            print(_db.seed_full(force=True, skeleton_only=True))
        if not _db.is_seeded():
            def _bg():
                try:
                    print("background rich enrich started...")
                    print(_db.seed_full(force=True, skeleton_only=False))
                    _apply_content_packs_if_needed(_db)
                except Exception as ex:
                    print("background enrich error:", ex)
            threading.Thread(target=_bg, daemon=True).start()
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


@app.get("/api/lan")
def api_lan():
    ips = get_lan_ips()
    port = BIND_PORT
    return jsonify({
        "ok": True,
        "bind_host": BIND_HOST,
        "port": port,
        "lan_ip": ips[0],
        "lan_ips": ips,
        "urls": [f"http://{ip}:{port}" for ip in ips],
        "hint_fa": "اگر از سیستم دیگر باز نشد: فایروال ویندوز پورت 83 را باز کنید و NETENC_HOST=0.0.0.0 باشد.",
    })


@app.get("/api/health")
def health():
    st = {}
    try:
        st = db().stats()
    except Exception as e:
        st = {"error": str(e)}
    ips = get_lan_ips()
    return jsonify({
        "ok": True,
        "device": DEVICE_ID,
        "schema_version": SCHEMA_VERSION,
        "sync_protocol": "v1-aligned",
        "bind_host": BIND_HOST,
        "port": BIND_PORT,
        "lan_ip": ips[0],
        "lan_ips": ips,
        "token_required_for_sync": bool(SYNC_TOKEN),
        "default_token_in_use": SYNC_TOKEN == DEFAULT_DEV_TOKEN,
        "modules": {
            "workspace": _MODULE_STATUS["workspace"],
            "study": bool(register_study_routes),
            "workspace_error": _MODULE_STATUS.get("workspace_error") or None,
            "study_error": _MODULE_STATUS.get("study_error") or None,
        },
        "stats": st,
        "content_seeded": bool(db().is_seeded()),
        "packs_applied": db().get_meta("packs_applied") or "",
    })


@app.get("/api/stats")
def api_stats():
    return jsonify(db().stats())


@app.get("/api/chapters")
def chapters():
    rows = db().list_chapters()
    return jsonify({"chapters": rows, "count": len(rows)})


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
        return jsonify({"error": str(e), "items": []})
    return jsonify({"items": items, "count": len(items)})


@app.get("/api/search")
def search():
    q = request.args.get("q") or ""
    return jsonify(db().search(q))


@app.post("/api/apply-packs")
def apply_packs():
    denied = require_token()
    if denied:
        return denied
    try:
        result = _apply_content_packs_if_needed(db(), force=True)
        status = 200 if result.get("ok") else 503
        return jsonify(result), status
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.post("/api/reseed")
def reseed():
    denied = require_token()
    if denied:
        return denied
    database = db()
    database.set_meta("packs_applied", "")  # Force professional packs to be reapplied after reseeding.
    result = database.seed_full(force=True, skeleton_only=True)
    # Do not apply rich packs to the skeleton while the background seed is still running.
    def _bg():
        try:
            database = db()
            seed_result = database.seed_full(force=True, skeleton_only=False)
            print("reseed enrich", seed_result)
            pack_result = _apply_content_packs_if_needed(database)
            print("reseed pack apply", pack_result.get("ok"), pack_result.get("version") or pack_result.get("error"))
        except Exception as ex:
            print("reseed enrich", ex)
    threading.Thread(target=_bg, daemon=True).start()
    result["enrich"] = "background"
    result["packs"] = "apply_after_enrichment"
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
    ips = get_lan_ips()
    return jsonify({
        "ok": True,
        "schema_version": SCHEMA_VERSION,
        "device_id": DEVICE_ID,
        "lan_ip": ips[0],
        "lan_ips": ips,
        "port": BIND_PORT,
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
    port = BIND_PORT
    print("init db / rich seed if needed...")
    d = db()
    try:
        if d.is_seeded():
            _apply_content_packs_if_needed(d)
        else:
            print("rich seed is running; versioned content packs will apply after enrichment")
    except Exception as e:
        print("pack apply skipped:", e)
    if register_study_routes:
        try:
            register_study_routes(app, db)
            _MODULE_STATUS["study"] = True
        except Exception as e:
            _MODULE_STATUS["study_error"] = str(e)
            print("study routes", e)
    ips = get_lan_ips()
    print(f"NetEnc listening on http://{host}:{port}")
    for ip in ips:
        print(f"  LAN URL: http://{ip}:{port}")
    print("  If other PCs cannot open: allow TCP 83 in Windows Firewall (see docs/LAN_ACCESS_FA.md)")
    print("  Note: port 83 may need Administrator on Windows")
    app.run(host=host, port=port, debug=False, threaded=True)


if __name__ == "__main__":
    main()
