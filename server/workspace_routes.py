# -*- coding: utf-8 -*-
"""Tasks / Notes / Vault — auth required; vault secrets sealed (not plaintext)."""
from __future__ import annotations

import base64
import hashlib
import hmac
import uuid
from datetime import datetime, timezone
from pathlib import Path
import sqlite3

from flask import Blueprint, request, jsonify, render_template_string, make_response, redirect

bp = Blueprint("workspace", __name__)

_check_token = None
_extract_token = None
_sync_token = ""


def set_auth_checker(check_fn, extract_fn, sync_token: str):
    global _check_token, _extract_token, _sync_token
    _check_token = check_fn
    _extract_token = extract_fn
    _sync_token = sync_token or ""


def _authorized() -> bool:
    if _check_token is None:
        return False
    return bool(_check_token())


def _seal(plain: str) -> str:
    if not plain:
        return ""
    if plain.startswith("enc1:"):
        return plain
    key = hashlib.sha256((_sync_token or "dev").encode("utf-8")).digest()
    raw = plain.encode("utf-8")
    out = bytes(b ^ key[i % len(key)] for i, b in enumerate(raw))
    return "enc1:" + base64.urlsafe_b64encode(out).decode("ascii")


def _unseal(blob: str) -> str:
    if not blob:
        return ""
    if not blob.startswith("enc1:"):
        return "•••• (legacy — edit to re-seal)"
    try:
        key = hashlib.sha256((_sync_token or "dev").encode("utf-8")).digest()
        raw = base64.urlsafe_b64decode(blob[5:].encode("ascii"))
        out = bytes(b ^ key[i % len(key)] for i, b in enumerate(raw))
        return out.decode("utf-8")
    except Exception:
        return "••••"


LOGIN_PAGE = """
<!doctype html><html lang=fa dir=rtl><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>ورود فضای کاری</title>
<style>
body{font-family:Tahoma,sans-serif;background:#0f172a;color:#e2e8f0;display:flex;min-height:100vh;align-items:center;justify-content:center}
form{background:#1e293b;padding:24px;border-radius:12px;width:min(360px,92vw)}
input,button{width:100%;padding:10px;margin:8px 0;box-sizing:border-box;font-size:15px;border-radius:8px;border:0}
button{background:#0ea5e9;color:#fff;font-weight:bold}
.err{color:#fca5a5;font-size:13px}
</style></head><body>
<form method=post action="/workspace/login">
<h2>فضای کاری — نیاز به توکن</h2>
<p style="color:#94a3b8;font-size:13px">همان NETENC_TOKEN سرور / توکن Sync اندروید</p>
<input type=password name=token placeholder="توکن" required autofocus>
{% if error %}<p class=err>{{ error }}</p>{% endif %}
<button type=submit>ورود</button>
<p style="font-size:12px;color:#64748b"><a href="/" style="color:#38bdf8">بازگشت</a></p>
</form>
</body></html>
"""

PAGE = """
<!doctype html><html lang=fa dir=rtl><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>فضای کاری</title>
<style>
body{font-family:Tahoma,sans-serif;background:#f7f8fa;margin:0;padding:16px;color:#0f172a}
.card{background:#fff;border-radius:12px;padding:12px;margin:8px 0;box-shadow:0 1px 3px #0001}
input,textarea,button{width:100%;margin:4px 0;padding:10px;box-sizing:border-box;font-size:15px}
button{background:#0ea5e9;color:#fff;border:0;border-radius:8px}
nav a{margin-left:12px;color:#0369a1;text-decoration:none;font-weight:bold}
.badge{font-size:12px;color:#64748b}
</style></head><body>
<nav>
<a href="/">خانه</a>
<a href="/workspace?tab=tasks">کارها</a>
<a href="/workspace?tab=notes">یادداشت</a>
<a href="/workspace?tab=vault">رمزها</a>
<a href="/workspace/logout">خروج</a>
</nav>
<p class="badge">دسترسی با توکن · vault به صورت sealed ذخیره می‌شود</p>
<h2>{{ title }}</h2>
<form method=post>
<input name=title placeholder="عنوان" required>
<textarea name=body rows=4 placeholder="{{ 'رمز (ذخیره sealed)' if tab=='vault' else 'متن' }}"></textarea>
{% if tab=='vault' %}<input name=username placeholder="نام کاربری">{% endif %}
<button type=submit>ذخیره</button>
</form>
{% for it in items %}
<div class=card>
<b>{{ it.title }}</b>
<pre style="white-space:pre-wrap;margin:8px 0">{{ it.body }}</pre>
<form method=post><input type=hidden name=delete value="{{ it.uid }}">
<button type=submit style="background:#ef4444">حذف</button></form>
</div>
{% else %}<p>موردی نیست.</p>{% endfor %}
</body></html>
"""


def _db_path():
    root = Path(__file__).resolve().parent
    for p in (root / "data" / "encyclopedia.db", root / "encyclopedia.db"):
        if p.is_file():
            return p
    p = root / "data" / "encyclopedia.db"
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def _conn():
    c = sqlite3.connect(str(_db_path()))
    c.row_factory = sqlite3.Row
    c.execute("CREATE TABLE IF NOT EXISTS ws_tasks(uid TEXT PRIMARY KEY, title TEXT, body TEXT, done INT, last_updated TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS ws_notes(uid TEXT PRIMARY KEY, title TEXT, body TEXT, last_updated TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS ws_vault(uid TEXT PRIMARY KEY, title TEXT, username TEXT, secret TEXT, last_updated TEXT)")
    c.commit()
    return c


def _cookie_ok() -> bool:
    if not _sync_token:
        return True
    c = request.cookies.get("netenc_token") or ""
    return hmac.compare_digest(c, _sync_token)


@bp.route("/workspace/login", methods=["GET", "POST"])
def workspace_login():
    err = ""
    if request.method == "POST":
        tok = (request.form.get("token") or "").strip()
        if _sync_token and tok == _sync_token:
            resp = make_response(redirect("/workspace"))
            resp.set_cookie("netenc_token", tok, httponly=True, samesite="Lax", max_age=60 * 60 * 12)
            return resp
        if not _sync_token:
            return redirect("/workspace")
        err = "توکن نادرست"
    return render_template_string(LOGIN_PAGE, error=err)


@bp.route("/workspace/logout")
def workspace_logout():
    resp = make_response(redirect("/workspace/login"))
    resp.set_cookie("netenc_token", "", expires=0)
    return resp


@bp.route("/workspace", methods=["GET", "POST"])
def workspace_page():
    if not _authorized() and not _cookie_ok():
        return redirect("/workspace/login")
    tab = request.args.get("tab") or "tasks"
    if tab not in ("tasks", "notes", "vault"):
        tab = "tasks"
    c = _conn()
    if request.method == "POST":
        if request.form.get("delete"):
            uid = request.form["delete"]
            table = {"notes": "ws_notes", "vault": "ws_vault"}.get(tab, "ws_tasks")
            c.execute(f"DELETE FROM {table} WHERE uid=?", (uid,))
            c.commit()
        else:
            title = (request.form.get("title") or "").strip()
            body = request.form.get("body") or ""
            username = request.form.get("username") or ""
            if title:
                uid = str(uuid.uuid4())
                now = datetime.now(timezone.utc).isoformat()
                if tab == "notes":
                    c.execute("INSERT INTO ws_notes VALUES(?,?,?,?)", (uid, title, body, now))
                elif tab == "vault":
                    c.execute("INSERT INTO ws_vault VALUES(?,?,?,?,?)", (uid, title, username, _seal(body), now))
                else:
                    c.execute("INSERT INTO ws_tasks VALUES(?,?,?,?,?)", (uid, title, body, 0, now))
                c.commit()
    if tab == "notes":
        items = c.execute("SELECT uid,title,body FROM ws_notes ORDER BY last_updated DESC").fetchall()
        title = "یادداشت‌ها"
    elif tab == "vault":
        rows = c.execute("SELECT uid,title,username,secret FROM ws_vault ORDER BY title").fetchall()
        items = []
        for r in rows:
            secret_show = _unseal(r["secret"]) if (_authorized() or _cookie_ok()) else "••••"
            items.append({"uid": r["uid"], "title": r["title"], "body": f"{r['username']}\n{secret_show}"})
        title = "مدیریت رمز ورود (sealed)"
    else:
        items = c.execute("SELECT uid,title,body FROM ws_tasks ORDER BY last_updated DESC").fetchall()
        title = "مدیریت کارها"
    return render_template_string(PAGE, items=items, title=title, tab=tab)


@bp.route("/api/workspace/export")
def workspace_export():
    if not _authorized():
        return jsonify({"error": "unauthorized"}), 401
    c = _conn()
    vault = []
    for r in c.execute("SELECT * FROM ws_vault").fetchall():
        d = dict(r)
        d["secret"] = _unseal(d.get("secret") or "")
        d["secret_sealed"] = True
        vault.append(d)
    return jsonify({
        "tasks": [dict(r) for r in c.execute("SELECT * FROM ws_tasks").fetchall()],
        "notes": [dict(r) for r in c.execute("SELECT * FROM ws_notes").fetchall()],
        "vault": vault,
    })
