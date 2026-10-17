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


def _lesson_fields(raw: Dict[str, Any], inherited_chapter_order: Any = None) -> Optional[Dict[str, Any]]:
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
        cmd = raw.get("command") or raw.get("syntax") or raw.get("cli") or raw.get("commands") or ""
        detail = raw.get("description_fa") or raw.get("description") or raw.get("when_to_use_fa") or raw.get("purpose") or ""
        if cmd or detail:
            full = (
                f"# {title}\n\n## Command\n{_as_text(cmd)}\n\n"
                f"## Purpose\n{_as_text(detail)}\n\n"
                f"## Syntax / Example\n{_as_text(raw.get('syntax') or cmd)}\n\n"
                f"## Lab and verification\n{_as_text(raw.get('lab_hint_fa') or raw.get('example') or raw.get('sample_output') or '')}\n\n"
                f"## Common mistakes / security\n{_as_text(raw.get('common_mistakes_fa') or raw.get('security_notes_fa') or raw.get('notes') or '')}\n"
            )
    if len(full) < 200:
        return None
    summary = _as_text(raw.get("summary") or raw.get("when_to_use_fa") or full[:200]).strip()
    meta = raw.get("meta") if isinstance(raw.get("meta"), dict) else {}
    if raw.get("uid"):
        meta = dict(meta)
        meta.setdefault("uid", str(raw.get("uid")))
    return {
        "title_fa": title,
        "summary": summary,
        "full_content": full,
        "commands": _as_text(raw.get("commands") or raw.get("cli") or ""),
        "examples": _as_text(raw.get("examples") or raw.get("lab") or ""),
        "notes": _as_text(raw.get("notes") or raw.get("troubleshooting") or ""),
        "learning_objectives": _as_text(raw.get("learning_objectives") or ""),
        "title_en": str(raw.get("title_en") or raw.get("name") or ""),
        "meta_json": json.dumps(meta, ensure_ascii=False),
        "source_status": str(raw.get("source_status") or ""),
        "chapter_order": raw.get("chapter_order") or raw.get("chapterOrder") or raw.get("chapter_order_index") or inherited_chapter_order,
        "subchapter_order": raw.get("subchapter_order") or raw.get("subchapter") or 1,
        "lesson_order": raw.get("lesson_order") or raw.get("order") or 0,
        "topic": str(raw.get("topic") or raw.get("domain") or raw.get("category") or ""),
        "uid": str(raw.get("uid") or ""),
        "level": str(raw.get("level") or ""),
    }


def load_lessons_from_file(path: Path) -> List[Dict[str, str]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        print("pack load error", path, e)
        return []

    out: List[Dict[str, str]] = []

    def add(item: dict, inherited_chapter_order: Any = None):
        f = _lesson_fields(item, inherited_chapter_order)
        if f:
            out.append(f)

    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                add(item)
        return out

    if not isinstance(data, dict):
        return out

    if isinstance(data.get("commands"), list):
        root_chapter = data.get("chapter_order") or 68
        vendor_pack = str(data.get("vendor_pack") or data.get("vendor") or path.stem)
        for i, command in enumerate(data["commands"], 1):
            if not isinstance(command, dict):
                continue
            cmd = str(command.get("command") or command.get("title_en") or command.get("name") or f"command-{i}")
            title = str(command.get("title_fa") or command.get("title") or cmd)
            level = str(command.get("level") or "L1")
            if not re.match(r"^\[L[0-4]\]", title, re.I):
                title = f"[{level}] {title}"
            topic = str(command.get("subcategory") or command.get("category") or vendor_pack)
            args = command.get("arguments") or []
            args_text = "\n".join(
                f"- {a.get('name', '')}: {a.get('meaning_fa', '')} (example: {a.get('example', '')})"
                if isinstance(a, dict) else f"- {a}" for a in args
            )
            steps = command.get("steps_fa") or []
            steps_text = "\n".join(f"{n}. {v}" for n, v in enumerate(steps, 1)) if isinstance(steps, list) else str(steps)
            mistakes = command.get("common_mistakes_fa") or []
            mistakes_text = "\n".join(f"- {v}" for v in mistakes) if isinstance(mistakes, list) else str(mistakes)
            full = (
                f"# {title}\n\n## Command\n{cmd}\n\n## When to use\n{command.get('when_to_use_fa') or command.get('description') or title}\n\n"
                f"## Syntax and arguments\n{command.get('syntax') or cmd}\n{args_text}\n\n## Steps\n{steps_text}\n\n"
                f"## Example output\n{command.get('sample_output') or ''}\n\n## Common mistakes\n{mistakes_text}\n\n"
                f"## Lab\n{command.get('lab_hint_fa') or ''}\n\n## Security\n{command.get('security_notes_fa') or ''}\n"
            )
            add({
                "uid": command.get("uid") or f"lesson:ch{int(root_chapter):02d}:{vendor_pack}:{i:04d}",
                "chapter_order": root_chapter, "subchapter_order": command.get("subchapter_order") or 1,
                "lesson_order": command.get("lesson_order") or i, "level": level, "topic": topic,
                "title_fa": title, "title_en": command.get("title_en") or cmd,
                "summary": command.get("when_to_use_fa") or command.get("description") or title,
                "full_content": full, "commands": cmd, "examples": command.get("sample_output") or "",
                "notes": mistakes_text, "learning_objectives": command.get("learning_objectives") or "",
                "meta": command.get("meta") or {}, "source_status": command.get("source_status") or "review_required",
            }, root_chapter)
        return out

    if isinstance(data.get("lessons"), list):
        for item in data["lessons"]:
            if isinstance(item, dict):
                add(item)

    curriculum = data.get("curriculum") or {}
    if isinstance(curriculum, dict):
        for ch in curriculum.get("chapters") or []:
            for col in ch.get("collections") or []:
                chapter_order = (66 if "OSPF_BGP" in path.name.upper() else 67 if "VPN_ENTERPRISE" in path.name.upper() else ch.get("chapter_order") or ch.get("order_index") or ch.get("order") or ch.get("chapter_no") or ch.get("chapter"))
                for les in col.get("lessons") or []:
                    for sub in les.get("sub_lessons") or [les]:
                        if not isinstance(sub, dict):
                            continue
                        merged = dict(sub)
                        if not merged.get("title_fa"):
                            merged["title_fa"] = les.get("title_fa") or ""
                        add(merged, chapter_order)

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
            if p.name in {"ENGINEER_JOKAR_OSPF_BGP_Redistribution_deep_v1.json", "ENGINEER_JOKAR_VPN_Enterprise_IPsec_SSL_Troubleshooting_deep_v1.json"}:
                continue
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


def match_lesson_id(conn: sqlite3.Connection, title: str, chapter_order: Any = None) -> Optional[int]:
    title = (title or "").strip()
    if not title:
        return None
    try:
        chapter_order = int(chapter_order) if chapter_order is not None else None
    except (TypeError, ValueError):
        chapter_order = None

    # Chapter-aware matching prevents a lesson from one pack overwriting a same-named lesson elsewhere.
    join = " JOIN levels lv ON lv.id=lessons.level_id JOIN chapters ch ON ch.id=lv.chapter_id " if chapter_order is not None else ""
    scope = " AND ch.order_index=?" if chapter_order is not None else ""
    args = [chapter_order] if chapter_order is not None else []
    exact = conn.execute(
        "SELECT lessons.id FROM lessons" + join + " WHERE lessons.title_fa=?" + scope + " ORDER BY lessons.id LIMIT 1",
        [title, *args],
    ).fetchone()
    if exact:
        return int(exact["id"] if isinstance(exact, sqlite3.Row) else exact[0])

    bare = _norm_title(title)
    if len(bare) < 4:
        return None
    rows = conn.execute(
        "SELECT lessons.id, lessons.title_fa FROM lessons" + join +
        " WHERE lessons.title_fa LIKE ?" + scope + " LIMIT 50",
        [f"%{bare[:80]}%", *args],
    ).fetchall()
    if not rows:
        strong_toks = [t for t in _tokens(title) if len(t) >= 4][:4]
        if not strong_toks:
            return None
        clauses = ["lessons.title_fa LIKE ?"] * len(strong_toks)
        rows = conn.execute(
            "SELECT lessons.id, lessons.title_fa FROM lessons" + join +
            " WHERE " + " AND ".join(clauses) + scope + " LIMIT 50",
            [*[f"%{t}%" for t in strong_toks], *args],
        ).fetchall()
    best_id, best_score = None, 0.0
    for r in rows:
        rid = int(r[0] if not isinstance(r, sqlite3.Row) else r["id"])
        rtitle = r[1] if not isinstance(r, sqlite3.Row) else r["title_fa"]
        score = _score(title, rtitle or "")
        if score > best_score:
            best_id, best_score = rid, score
    return best_id if best_score >= 0.55 else None


def _insert_pack_lesson(conn: sqlite3.Connection, lesson: Dict[str, Any], now: str) -> Optional[int]:
    try:
        chapter_order = int(lesson.get("chapter_order"))
    except (TypeError, ValueError):
        return None
    chapter = conn.execute("SELECT id FROM chapters WHERE order_index=? ORDER BY id LIMIT 1", (chapter_order,)).fetchone()
    if not chapter:
        return None
    chapter_id = int(chapter["id"])
    topic = str(lesson.get("topic") or "").strip() or f"محتوای فصل {chapter_order}"
    level = conn.execute("SELECT id FROM levels WHERE chapter_id=? AND title_fa=? ORDER BY id LIMIT 1", (chapter_id, topic)).fetchone()
    if level:
        level_id = int(level["id"])
    else:
        row = conn.execute("SELECT COALESCE(MAX(order_index),0)+1 n FROM levels WHERE chapter_id=?", (chapter_id,)).fetchone()
        conn.execute("INSERT INTO levels(chapter_id,order_index,title_fa,title_en) VALUES(?,?,?,?)",
                     (chapter_id, int(row["n"] or 1), topic, topic))
        level_id = int(conn.execute("SELECT last_insert_rowid()").fetchone()[0])
    title = str(lesson.get("title_fa") or "درس افزوده")
    existing = conn.execute("SELECT id FROM lessons WHERE level_id=? AND title_fa=? ORDER BY id LIMIT 1", (level_id, title)).fetchone()
    if existing:
        return int(existing["id"])
    row = conn.execute("SELECT COALESCE(MAX(order_index),0)+1 n FROM lessons WHERE level_id=?", (level_id,)).fetchone()
    try:
        meta = json.loads(lesson.get("meta_json") or "{}")
    except Exception:
        meta = {}
    if not isinstance(meta, dict):
        meta = {}
    if lesson.get("uid"):
        meta.setdefault("uid", lesson["uid"])
    cur = conn.execute(
        """INSERT INTO lessons(level_id,order_index,title_fa,title_en,tags,summary,full_content,commands,examples,notes,meta_json,learning_objectives,source_status,last_updated)
           VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (level_id, int(row["n"] or 1), title, lesson.get("title_en") or "", lesson.get("level") or "",
         lesson.get("summary") or "", lesson.get("full_content") or "", lesson.get("commands") or "",
         lesson.get("examples") or "", lesson.get("notes") or "", json.dumps(meta, ensure_ascii=False),
         str(lesson.get("learning_objectives") or ""), lesson.get("source_status") or "review_required", now),
    )
    return int(cur.lastrowid)


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
            "security_ethical_hacking_pack.json", "wireless_security_pack.json",
            "ch66_ospf_bgp_redistribution_professional.json",
            "ch67_vpn_enterprise_ipsec_ssl_professional.json",
            "chapter_68_cisco_routing_1600.json", "cisco_switching.json",
            "mikrotik.json", "linux.json", "powershell.json", "batch.json",
        }
        # فصل‌های حرفه‌ای فصل‌محور، منبع مرجع درس‌های canonical هستند.
        if re.match(r"ch(?:31|32|33|4[0-9]|5[0-9]|6[0-3])_.*_professional(?:_part\d+)?\.json$", pack.name, re.I):
            force_professional = True

        m = x = u = 0
        for les in lessons:
            lid = match_lesson_id(conn, les["title_fa"], les.get("chapter_order"))
            if lid is None:
                lid = _insert_pack_lesson(conn, les, now)
                if lid is None:
                    x += 1
                    continue
                m += 1
                u += 1
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
