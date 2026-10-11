# -*- coding: utf-8 -*-
"""درج درس در seed — حالت fast برای استارت سریع."""
from __future__ import annotations

import json
import os


def insert_rich_lesson(cur, lv_id: int, oi: int, lfa: str, len_: str, now: str) -> None:
    """اگر NETENC_FAST_SEED=0 باشد محتوای غنی می‌سازد؛ پیش‌فرض fast."""
    fast = os.environ.get("NETENC_FAST_SEED", "1") != "0"
    tag = lfa[1:3] if str(lfa).startswith("[L") else "L0"
    if fast:
        summary = f"{lfa}"
        full_content = (
            f"# {lfa}\n\n"
            f"**سطح:** {tag}\n\n"
            f"محتوای پایهٔ این درس. برای نسخهٔ کتاب‌گونه از پک‌های tools/packs استفاده کنید.\n\n"
            f"## انگلیسی\n{len_}\n"
        )
        commands = ""
        examples = ""
        notes = "fast-seed"
        obj_text = f"درک {lfa}"
        meta = {"learning_objectives": [obj_text], "fast": True}
    else:
        from core.rich_content import build_rich_lesson
        from core.phase_a import default_meta

        meta = default_meta(lfa, level=tag)
        rich = build_rich_lesson(lfa, len_, level=tag) or {}
        summary = rich.get("summary") or f"{lfa}"
        full_content = rich.get("full_content") or summary
        commands = rich.get("commands") or ""
        examples = rich.get("examples") or ""
        notes = rich.get("notes") or ""
        objectives = rich.get("learning_objectives") or [f"درک {lfa}"]
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
            lfa,
            obj_text if fast else obj_text,
            json.dumps(meta, ensure_ascii=False),
            now,
        ),
    )
