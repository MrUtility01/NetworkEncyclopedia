# -*- coding: utf-8 -*-
"""موتور محتوای عمیق و ملموس."""
from __future__ import annotations
# See full version in local improvements - restoring non-empty stub
from typing import Any, Dict

def build_deep_fallback(title_fa: str, title_en: str = "", level: str | None = None) -> Dict[str, Any]:
    return {
        "summary": f"«{title_fa}» — محتوای عمیق سازمانی",
        "full_content": f"# {title_fa}\n\nمحتوای غنی در حال بارگذاری کامل...",
        "commands": "show version",
        "examples": "Lab",
        "notes": "RCA",
        "level": level or "L0",
        "topic": title_fa,
        "category": "general",
    }
