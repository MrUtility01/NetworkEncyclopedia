# -*- coding: utf-8 -*-
"""درج درس در seed — همیشه محتوای واقعی از build_rich_lesson."""
from __future__ import annotations

import json

from core.rich_content import build_rich_lesson
from core.phase_a import default_meta


def insert_rich_lesson(cur, lv_id: int, oi: int, lfa: str, len_: str, now: str) -> None:
    tag = lfa[1:3] if str(lfa).startswith("[L") else "L0"
    meta = default_meta(lfa, level=tag)
    rich = {}
    try:
        rich = build_rich_lesson(lfa, len_, level=tag) or {}
    except Exception as e:
        rich = {"summary": str(lfa), "full_content": f"# {lfa}\n\n{len_}\n\n(seed fallback: {e})"}

    summary = (rich.get("summary") or "").strip() or str(lfa)
    full_content = (rich.get("full_content") or "").strip() or summary
    commands = rich.get("commands") or ""
    examples = rich.get("examples") or ""
    notes = rich.get("notes") or ""
    objectives = rich.get("learning_objectives") or [
        f"درک مفهوم «{lfa}»",
        "اجرای تمرین کنترل‌شده در Lab",
        "عیب‌یابی با شواهد قابل اندازه‌گیری",
    ]
    if isinstance(objectives, str):
        obj_text = objectives
        obj_list = [x.strip() for x in objectives.splitlines() if x.strip()]
    else:
        obj_list = list(objectives)
        obj_text = "\n".join(str(x) for x in obj_list)

    meta["description"] = summary
    meta["learning_objectives"] = obj_list

    cur.execute(
        """INSERT INTO lessons(
            level_id, order_index, title_fa, title_en, tags,
            summary, full_content, commands, examples, notes,
            search_query, learning_objectives, meta_json, last_updated
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (
            lv_id,
            oi,
            lfa,
            len_,
            tag,
            summary,
            full_content,
            commands,
            examples,
            notes,
            meta.get("ai_search_prompt") or lfa,
            obj_text,
            json.dumps(meta, ensure_ascii=False),
            now,
        ),
    )
