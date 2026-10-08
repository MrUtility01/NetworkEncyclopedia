# -*- coding: utf-8 -*-
"""درج درس‌های غنی در seed — توسط db.seed_full فراخوانی می‌شود."""
from __future__ import annotations

import json
from typing import Any

from core.rich_content import build_rich_lesson
from core.phase_a import default_meta


def insert_rich_lesson(cur, lv_id: int, oi: int, lfa: str, len_: str, now: str) -> None:
    tag = lfa[1:3] if lfa.startswith("[L") else "L0"
    meta = default_meta(lfa, level=tag)
    rich = build_rich_lesson(lfa, len_, level=tag)
    meta["description"] = rich["summary"]
    meta["learning_objectives"] = rich["learning_objectives"]
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
            rich["summary"],
            rich["full_content"],
            rich["commands"],
            rich["examples"],
            rich["notes"],
            meta.get("ai_search_prompt", ""),
            "\n".join(rich["learning_objectives"]),
            json.dumps(meta, ensure_ascii=False),
            now,
        ),
    )
