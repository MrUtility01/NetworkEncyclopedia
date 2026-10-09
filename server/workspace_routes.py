# -*- coding: utf-8 -*-
"""Tasks / Notes / Vault for Windows server."""
from __future__ import annotations
import uuid
from datetime import datetime, timezone
from pathlib import Path
import sqlite3
from flask import Blueprint, request, jsonify, render_template_string

bp = Blueprint("workspace", __name__)

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
</style></head><body>
<nav>
<a href="/">خانه</a>
<a href="/workspace?tab=tasks">کارها</a>
<a href="/workspace?tab=notes">یادداشت</a>
<a href="/workspace?tab=vault">رمزها</a>
</nav>
<h2>{{ title }}</h2>
<form method=post>
<input name=title placeholder="عنوان" required>
<textarea name=body rows=4 placeholder="متن / رمز"></textarea>
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

@bp.route("/workspace", methods=["GET", "POST"])
def workspace_page():
    tab = request.args.get("tab") or "tasks"
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
                    c.execute("INSERT INTO ws_vault VALUES(?,?,?,?,?)", (uid, title, username, body, now))
                else:
                    c.execute("INSERT INTO ws_tasks VALUES(?,?,?,?,?)", (uid, title, body, 0, now))
                c.commit()
    if tab == "notes":
        items = c.execute("SELECT uid,title,body FROM ws_notes ORDER BY last_updated DESC").fetchall()
        title = "یادداشت‌ها"
    elif tab == "vault":
        rows = c.execute("SELECT uid,title,username,secret FROM ws_vault ORDER BY title").fetchall()
        items = [{"uid": r["uid"], "title": r["title"], "body": f"{r['username']}\n{r['secret']}"} for r in rows]
        title = "مدیریت رمز ورود"
    else:
        items = c.execute("SELECT uid,title,body FROM ws_tasks ORDER BY last_updated DESC").fetchall()
        title = "مدیریت کارها"
    return render_template_string(PAGE, items=items, title=title, tab=tab)

@bp.route("/api/workspace/export")
def workspace_export():
    c = _conn()
    return jsonify({
        "tasks": [dict(r) for r in c.execute("SELECT * FROM ws_tasks").fetchall()],
        "notes": [dict(r) for r in c.execute("SELECT * FROM ws_notes").fetchall()],
        "vault": [dict(r) for r in c.execute("SELECT * FROM ws_vault").fetchall()],
    })
