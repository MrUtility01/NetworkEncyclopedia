# -*- coding: utf-8 -*-
"""بارگذاری پک — فقط وقتی عنوان درس و پک واقعاً هم‌موضوع باشند."""
from __future__ import annotations

import json
import re
import sys
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(sys._MEIPASS) if getattr(sys, "frozen", False) else Path(__file__).resolve().parents[2]

_STOP = {
    "با", "برای", "از", "و", "در", "به", "که", "این", "آن", "یک",
    "the", "and", "for", "with", "from", "into", "lesson", "درس",
    "آشنایی", "مقدماتی", "ادمین", "مهندس", "خبره", "پیاده‌سازی", "مبانی",
}


def _as_text(v: Any) -> str:
    if v is None:
        return ""
    if isinstance(v, list):
        return "\n".join(str(x) for x in v)
    if isinstance(v, dict):
        return json.dumps(v, ensure_ascii=False, indent=2)
    return str(v)


def _norm_title(title: str) -> str:
    t = re.sub(r"^\[L[0-4]\]\s*", "", title or "", flags=re.I)
    t = re.sub(r"\s*[—\-]\s*(آشنایی|مقدماتی|ادمین|مهندس|خبره|پیاده‌سازی|مبانی).*$", "", t, flags=re.I)
    t = re.sub(r"[^\w\u0600-\u06FF\s]", " ", t)
    t = re.sub(r"\s+", " ", t).strip().lower()
    return t


def _tokens(title: str) -> List[str]:
    return [w for w in _norm_title(title).split() if len(w) >= 3 and w not in _STOP]


def _lesson_fields(raw: Dict[str, Any]) -> Optional[Dict[str, str]]:
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
        "meta_json": json.dumps(raw.get("meta") or {}, ensure_ascii=False),
        "source_status": str(raw.get("source_status") or ""),
    }


def load_lessons_from_file(path: Path) -> List[Dict[str, str]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        print("pack load error", path, e)
        return []

    out: List[Dict[str, str]] = []

    def add(item: dict):
        f = _lesson_fields(item)
        if f:
            out.append(f)

    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                add(item)
        return out

    if not isinstance(data, dict):
        return out

    if isinstance(data.get("lessons"), list):
        for item in data["lessons"]:
            if isinstance(item, dict):
                add(item)

    curriculum = data.get("curriculum") or {}
    if isinstance(curriculum, dict):
        for ch in curriculum.get("chapters") or []:
            for col in ch.get("collections") or []:
                for les in col.get("lessons") or []:
                    for sub in les.get("sub_lessons") or [les]:
                        if not isinstance(sub, dict):
                            continue
                        merged = dict(sub)
                        if not merged.get("title_fa"):
                            merged["title_fa"] = les.get("title_fa") or ""
                        add(merged)

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
            key = str(p.resolve())
            if key in seen:
                continue
            if p.name.upper().startswith("README"):
                continue
            seen.add(key)
            found.append(p)
    return sorted(found)


def _score(pack_title: str, db_title: str) -> float:
    a = _norm_title(pack_title)
    b = _norm_title(db_title)
    if not a or not b:
        return 0.0
    if a == b:
        return 1.0
    if a in b or b in a:
        shorter, longer = (a, b) if len(a) <= len(b) else (b, a)
        if len(shorter) >= 6:
            return 0.92
    ta, tb = set(_tokens(pack_title)), set(_tokens(db_title))
    if not ta or not tb:
        return 0.0
    inter = ta & tb
    if not inter:
        return 0.0
    strong = {t for t in inter if len(t) >= 4}
    if not strong:
        return 0.0
    jacc = len(inter) / len(ta | tb)
    cover = len(inter) / max(len(ta), 1)
    return max(jacc, cover * 0.85)


def match_lesson_id(conn: sqlite3.Connection, title: str) -> Optional[int]:
    title = (title or "").strip()
    if not title:
        return None
    # Prefer the exact canonical title so L0-L4 versions never collapse onto one row.
    exact = conn.execute("SELECT id FROM lessons WHERE title_fa=? ORDER BY id LIMIT 1", (title,)).fetchone()
    if exact:
        return int(exact["id"] if isinstance(exact, sqlite3.Row) else exact[0])
    bare = _norm_title(title)
    if len(bare) < 4:
        return None

    rows = conn.execute(
        "SELECT id, title_fa FROM lessons WHERE title_fa LIKE ? LIMIT 30",
        (f"%{bare[:80]}%",),
    ).fetchall()

    if not rows:
        strong_toks = [t for t in _tokens(title) if len(t) >= 4][:4]
        if not strong_toks:
            return None
        q = "SELECT id, title_fa FROM lessons WHERE " + " AND ".join(
            ["title_fa LIKE ?"] * len(strong_toks)
        ) + " LIMIT 40"
        rows = conn.execute(q, [f"%{t}%" for t in strong_toks]).fetchall()

    best_id = None
    best_score = 0.0
    for r in rows:
        rid = int(r[0] if not isinstance(r, sqlite3.Row) else r["id"])
        rtitle = r[1] if not isinstance(r, sqlite3.Row) else r["title_fa"]
        sc = _score(title, rtitle or "")
        if sc > best_score:
            best_score = sc
            best_id = rid

    if best_score >= 0.55:
        return best_id
    return None


def apply_packs_to_db(db_path: Path, overwrite: bool = True) -> Dict[str, Any]:
    db_path = Path(db_path)
    if not db_path.is_file():
        return {"ok": False, "error": f"db not found: {db_path}"}

    packs = find_pack_files()
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    now = datetime.now(timezone.utc).isoformat()
    matched = missing = updated = skipped_weak = skipped_shorter = 0
    details = []

    for pack in packs:
        lessons = load_lessons_from_file(pack)
        # These curated professional chapter packs are authoritative for their exact canonical lesson titles.
        force_professional = pack.name in {
            "ch34_m365_intune_email_professional.json",
            "ch35_powershell_cmd_professional.json",
            "ch36_linux_admin_professional.json",
            "ch37_linux_network_professional.json",
            "ch38_linux_web_services_professional.json",
            "ch39_linux_security_professional.json",
        }
        m = x = u = 0
        for les in lessons:
            lid = match_lesson_id(conn, les["title_fa"])
            if lid is None:
                x += 1
                continue
            row = conn.execute("SELECT title_fa FROM lessons WHERE id=?", (lid,)).fetchone()
            db_title = row["title_fa"] if row else ""
            if _score(les["title_fa"], db_title) < 0.55:
                skipped_weak += 1
                continue
            m += 1
            # هرگز محتوای غنی‌تر را با کوتاه‌تر عوض نکن
            cur = conn.execute(
                "SELECT length(COALESCE(full_content,'')) n, COALESCE(meta_json,'{}') meta_json, source_status FROM lessons WHERE id=?",
                (lid,),
            ).fetchone()
            cur_n = int(cur["n"] or 0) if cur else 0
            new_n = len(les.get("full_content") or "")
            if not force_professional and cur_n > 0 and new_n + 200 < cur_n:
                skipped_shorter += 1
                continue
            if not overwrite and cur_n >= new_n and not force_professional:
                continue
            try:
                old_meta = json.loads(cur["meta_json"] or "{}") if cur else {}
            except Exception:
                old_meta = {}
            try:
                incoming_meta = json.loads(les.get("meta_json") or "{}")
            except Exception:
                incoming_meta = {}
            if not isinstance(old_meta, dict):
                old_meta = {}
            if isinstance(incoming_meta, dict):
                old_meta.update(incoming_meta)
            merged_meta_json = json.dumps(old_meta, ensure_ascii=False)
            status = les.get("source_status") or (cur["source_status"] if cur else "") or "review_required"
            conn.execute(
                """UPDATE lessons SET
                    summary=?, full_content=?, commands=?, examples=?, notes=?,
                    learning_objectives=CASE WHEN ?!='' THEN ? ELSE learning_objectives END,
                    meta_json=?, source_status=?, last_updated=?
                 WHERE id=?""",
                (
                    les["summary"],
                    les["full_content"],
                    les["commands"],
                    les["examples"],
                    les["notes"],
                    les["learning_objectives"],
                    les["learning_objectives"],
                    merged_meta_json,
                    status,
                    now,
                    lid,
                ),
            )
            u += 1
        conn.commit()
        matched += m
        missing += x
        updated += u
        details.append(
            {
                "pack": pack.name,
                "lessons": len(lessons),
                "matched": m,
                "missing": x,
                "updated": u,
            }
        )
        print(f"  pack {pack.name}: lessons={len(lessons)} matched={m} updated={u} missing={x}")

    conn.close()
    return {
        "ok": True,
        "packs": len(packs),
        "matched": matched,
        "updated": updated,
        "missing": missing,
        "skipped_weak": skipped_weak,
        "skipped_shorter": skipped_shorter,
        "details": details,
    }
