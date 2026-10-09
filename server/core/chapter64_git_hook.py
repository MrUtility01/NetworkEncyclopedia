# -*- coding: utf-8 -*-
"""Hook فصل ۶۴ Git — بارگذاری از tools/chapter_git_teacher.py"""
from __future__ import annotations
from pathlib import Path
import sys

def _load():
    try:
        from core import chapter_git_teacher as m
        return m
    except Exception:
        pass
    root = Path(__file__).resolve().parents[2]
    tools = root / "tools"
    if str(tools) not in sys.path:
        sys.path.insert(0, str(tools))
    import chapter_git_teacher as m
    return m

def get_git_chapter_levels():
    return _load().get_git_chapter_levels()

def is_git_title(title: str) -> bool:
    return _load().is_git_title(title)

def build_git_lesson(title_fa: str, title_en: str = ""):
    return _load().build_git_lesson(title_fa, title_en)
