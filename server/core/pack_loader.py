# -*- coding: utf-8 -*-
"""بارگذاری محتوای واقعی از JSON پک‌ها روی جدول lessons."""
from __future__ import annotations

import json
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[2]


def _as_text(v: Any) -> str:
    if v is None:
        return ""
    if isinstance(v, list):
        return "\n".join(str(x) for x in v)
    if isinstance(v, dict):
        return json.dumps(v, ensure_ascii=False, indent=2)
    return str(v)


def _lesson_fields(raw: Dict[str, Any]) -> Optional[Dict[str, str]]:
    """استاندارد کردن فیلدهای یک رکورد درس از پک‌های مختلف."""
    title = (raw.get("title_fa") or raw.get("title") or raw.get("name") or "").strip()
    full = (
        raw.get("full_content")
        or raw.get("content")
        or raw.get("body")
        or raw.get("lesson_body")
        or ""
    )
    if isinstance(full, dict):
        full = json.dumps(full, ensure_ascii=False, indent=2)
    full = str(full).strip()
    if len(full) < 200:
        return None
    summary = (raw.get("summary") or full[:200]).strip()
    return {
        "title_fa": title,
        "summary": summary,
        "full_content": full,
        "commands": _as_text(raw.get("commands") or raw.get("cli") or ""),
        "examples": _as_text(raw.get("examples") or raw.get("lab") or ""),
        "notes": _as_text(raw.get("notes") or raw.get("troubleshooting") or ""),
        "learning_objectives": _as_text(raw.get("learning_objectives") or ""),
    }


def load_lessons_from_file(path: Path) -> List[Dict[str, str]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        print("pack load error", path, e)
        return []

    out: List[Dict[str, str]] = []

    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                f = _lesson_fields(item)
                if f:
                    out.append(f)
        return out

    if not isinstance(data, dict):
        return out

    # curriculum pack with lessons array
    if isinstance(data.get("lessons"), list):
        for item in data["lessons"]:
            if isinstance(item, dict):
                f = _lesson_fields(item)
                if f:
                    out.append(f)

    # blueprint ENGINEER_JOKAR
    curriculum = (data.get("curriculum") or {})
    if isinstance(curriculum, dict):
        for ch in curriculum.get("chapters") or []:
            for col in ch.get("collections") or []:
                for les in col.get("lessons") or []:
                    for sub in les.get("sub_lessons") or [les]:
                        if not isinstance(sub, dict):
                            continue
                        merged = dict(sub)
                        if not merged.get("title_fa"):
                            merged["title_fa"] = les.get("title_fa") or ch.get("title_fa")
                        f = _lesson_fields(merged)
                        if f:
                            out.append(f)

    # commands encyclopedia style: categories -> commands (not full lessons)
    if data.get("vendor") or data.get("commands") or data.get("categories"):
        # build synthetic lessons from command groups if long enough
        cats = data.get("categories") or data.get("sections") or []
        if isinstance(cats, list):
            for cat in cats:
                if not isinstance(cat, dict):
                    continue
                cmds = cat.get("commands") or cat.get("items") or []
                if not cmds:
                    continue
                lines = [f"# {cat.get('title_fa') or cat.get('name') or 'دستورات'}\n"]
                for c in cmds[:80]:
                    if isinstance(c, dict):
                        lines.append(f"## {c.get('name') or c.get('command') or ''}\n")
                        lines.append(f"```\n{c.get('command') or c.get('syntax') or ''}\n```\n")
                        if c.get("description"):
                            lines.append(str(c["description"]) + "\n")
                        if c.get("example"):
                            lines.append(f"مثال:\n```\n{c['example']}\n```\n")
                    else:
                        lines.append(str(c))
                body = "\n".join(lines)
                if len(body) > 300:
                    out.append(
                        {
                            "title_fa": cat.get("title_fa") or cat.get("name") or data.get("vendor") or "commands",
                            "summary": (cat.get("description") or body[:180]).strip(),
                            "full_content": body,
                            "commands": body,
                            "examples": "",
                            "notes": "منبع: commands encyclopedia pack",
                            "learning_objectives": "",
                        }
                    )

    return out


def find_pack_files() -> List[Path]:
    patterns = [
        "tools/**/*_pack.json",
        "tools/**/*curriculum*.json",
        "tools/packs/**/*.json",
        "tools/engineer_jokar_*/**/*.json",
    ]
    found: List[Path] = []
    seen = set()
    for pat in patterns:
        for p in ROOT.glob(pat):
            if not p.is_file() or p.stat().st_size < 500:
                continue
            # skip schema-only tiny files
            key = str(p.resolve())
            if key in seen:
                continue
            if p.name.upper().startswith("README"):
                continue
            seen.add(key)
            found.append(p)
    return sorted(found)


def match_lesson_id(conn: sqlite3.Connection, title: str) -> Optional[int]:
    title = (title or "").strip()
    if not title:
        return None
    bare = re.sub(r"^\[L[0-4]\]\s*", "", title)
    bare = re.sub(r"\s*[—\-]\s*(آشنایی|مقدماتی|ادمین|مهندس|خبره).*$", "", bare).strip()
    # prefer longest meaningful token match
    if len(bare) >= 4:
        row = conn.execute(
            "SELECT id, title_fa FROM lessons WHERE title_fa LIKE ? ORDER BY length(full_content) ASC LIMIT 5",
            (f"%{bare}%",
            ),
        ).fetchall()
        if row:
            return int(row[0][0] if not isinstance(row[0], sqlite3.Row) else row[0]["id"])
    # token fallback: significant words
    tokens = [t for t in re.split(r"\s+", bare) if len(t) >= 4][:3]
    for tok in tokens:
        row = conn.execute(
            "SELECT id FROM lessons WHERE title_fa LIKE ? LIMIT 1",
            (f"%{tok}%",
            ),
        ).fetchone()
        if row:
            return int(row[0] if not isinstance(row, sqlite3.Row) else row["id"])
    return None


def apply_packs_to_db(db_path: Path, overwrite: bool = True) -> Dict[str, Any]:
    """محتوای واقعی پک‌ها را روی درس‌های موجود می‌نویسد."""
    db_path = Path(db_path)
    if not db_path.is_file():
        return {"ok": False, "error": f"db not found: {db_path}"}

    packs = find_pack_files()
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    now = datetime.now(timezone.utc).isoformat()
    matched = missing = updated = 0
    details = []

    for pack in packs:
        lessons = load_lessons_from_file(pack)
        m = x = u = 0
        for les in lessons:
            lid = match_lesson_id(conn, les["title_fa"])
            if lid is None:
                x += 1
                continue
            m += 1
            if not overwrite:
                cur = conn.execute(
                    "SELECT length(COALESCE(full_content,'')) n FROM lessons WHERE id=?",
                    (lid,),
                ).fetchone()
                if cur and int(cur["n"] or 0) > len(les["full_content"]):
                    continue
            conn.execute(
                """UPDATE lessons SET
                    summary=?, full_content=?, commands=?, examples=?, notes=?,
                    learning_objectives=CASE WHEN ?!='' THEN ? ELSE learning_objectives END,
                    last_updated=?
                 WHERE id=?""",
                (
                    les["summary"],
                    les["full_content"],
                    les["commands"],
                    les["examples"],
                    les["notes"],
                    les["learning_objectives"],
                    les["learning_objectives"],
                    now,
                    lid,
                ),
            )
            u += 1
        conn.commit()
        matched += m
        missing += x
        updated += u
        details.append({"pack": pack.name, "lessons": len(lessons), "matched": m, "missing": x, "updated": u})
        print(f"  pack {pack.name}: lessons={len(lessons)} matched={m} updated={u} missing={x}")

    conn.close()
    return {
        "ok": True,
        "packs": len(packs),
        "matched": matched,
        "updated": updated,
        "missing": missing,
        "details": details,
    }
