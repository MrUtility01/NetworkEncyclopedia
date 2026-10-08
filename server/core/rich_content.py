# -*- coding: utf-8 -*-
from __future__ import annotations
import re
from typing import Any, Dict, List
from core.rich_data import BANKS, ERRORS, COMMON

def level_tag(title: str) -> str:
    m = re.match(r"\[(L[0-4])\]", title or "")
    return m.group(1) if m else "L0"

def clean_topic(title: str) -> str:
    t = re.sub(r"^\[L[0-4]\]\s*", "", title or "").strip()
    t = re.sub(r"\s*[—\-]\s*(آشنایی|مقدماتی|ادمین|مهندس|خبره).*$", "", t, flags=re.I)
    return t.strip() or (title or "موضوع")

_LEVEL_FA = {"L0": "آشنایی", "L1": "مقدماتی", "L2": "ادمین", "L3": "مهندس", "L4": "خبره"}
_CATS = [
    ("vlan", ["vlan", "trunk"]), ("ospf", ["ospf"]), ("bgp", ["bgp"]),
    ("linux", ["linux", "bash"]), ("windows", ["windows", "powershell"]),
    ("ansible", ["ansible"]), ("python", ["python", "netmiko"]), ("sql", ["sql", "postgres"]),
]

def _cat(topic: str) -> str:
    t = topic.lower()
    for c, keys in _CATS:
        if any(k in t for k in keys):
            return c
    return "general"

def _fmt_cmds(pairs):
    return "\n".join(f"```\n{cmd}\n```\n→ {desc}\n" for cmd, desc in pairs)

def build_rich_lesson(title_fa: str, title_en: str = "", level: str | None = None) -> Dict[str, Any]:
    # فصل ۱
    try:
        from core.chapter01_teacher import build_chapter01_lesson, _bucket, _topic
        topic0 = _topic(title_fa)
        if _bucket(topic0) in ("cpu", "ram", "storage", "mb", "psu") or any(
            k in (title_fa or "") for k in ("CPU", "ALU", "RAM", "DDR", "SSD", "HDD", "NVMe", "مادربرد", "Chipset", "PSU", "تغذیه", "BIOS", "UEFI", "حافظه", "ذخیره")
        ):
            c1 = build_chapter01_lesson(title_fa, title_en)
            if c1:
                return c1
    except Exception:
        pass
    # فصل ۲
    try:
        from core.chapter02_teacher import build_chapter02_lesson
        if any(k in (title_fa or "") for k in (
            "ESD", "ایمنی", "اسمبل", "POST", "Beep", "تمیز", "ProLiant", "iLO",
            "سرور", "عیب", "نگهداری", "خمیر", "HP", "بایوس"
        )):
            c2 = build_chapter02_lesson(title_fa, title_en)
            if c2:
                return c2
    except Exception:
        pass

    level = level or level_tag(title_fa)
    topic = clean_topic(title_fa)
    cat = _cat(topic)
    summary = f"«{topic}» ({level}): مفهوم، دستورات، عیب‌یابی، Lab."
    full = f"# {topic}\n\n**سطح:** {level}\n\n{summary}\n"
    commands = "## پایه\n" + _fmt_cmds(COMMON[:8]) + "\n## تخصصی\n" + _fmt_cmds(BANKS.get(cat, BANKS.get("linux", []))[:12])
    lab = f"## آزمایشگاه — {topic}\n1) بخوان 2) دستور را اجرا کن 3) نتیجه را یادداشت کن\n"
    return {
        "summary": summary, "full_content": full, "commands": commands,
        "examples": lab, "notes": f"دسته={cat}", "level": level, "topic": topic, "category": cat,
    }
