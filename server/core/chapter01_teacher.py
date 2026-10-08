# -*- coding: utf-8 -*-
from __future__ import annotations
import re
from typing import Any, Dict
from core.chapter01_cpu import _cpu
from core.chapter01_hw import _ram, _storage, _mb, _psu, _general

def _level(title: str) -> str:
    m = re.match(r"\[(L[0-4])\]", title or "")
    return m.group(1) if m else "L0"

def _topic(title: str) -> str:
    t = re.sub(r"^\[L[0-4]\]\s*", "", title or "")
    t = re.sub(r"\s*[—\-]\s*(آشنایی|مقدماتی|ادمین|مهندس|خبره).*$", "", t, flags=re.I)
    return t.strip()

def _bucket(topic: str) -> str:
    t = topic.lower()
    if any(k in t for k in ("cpu", "alu", "پردازنده", "core", "thread", "cache", "instruction")):
        return "cpu"
    if any(k in t for k in ("motherboard", "chipset", "مادربرد", "سوکت", "بایوس", "bios", "uefi", "pcie")):
        return "mb"
    if any(k in t for k in ("ram", "ddr", "حافظه", "ecc", "memory")):
        return "ram"
    if any(k in t for k in ("hdd", "ssd", "nvme", "sata", "ذخیره", "disk", "raid")):
        return "storage"
    if any(k in t for k in ("psu", "تغذیه", "توان", "80plus", "power")):
        return "psu"
    return "general"

def build_chapter01_lesson(title_fa: str, title_en: str = "") -> Dict[str, Any] | None:
    topic, level = _topic(title_fa), _level(title_fa)
    b = _bucket(topic)
    builders = {"cpu": _cpu, "ram": _ram, "storage": _storage, "mb": _mb, "psu": _psu, "general": _general}
    summary, full, commands, lab = builders[b](topic, level)
    return {
        "summary": summary, "full_content": full, "commands": commands,
        "examples": lab, "notes": f"فصل۰۱ · {b} · {level}", "lab": lab,
        "level": level, "topic": topic, "category": b, "chapter": 1,
    }
