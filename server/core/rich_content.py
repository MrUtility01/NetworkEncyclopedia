# -*- coding: utf-8 -*-
from __future__ import annotations
import re
from typing import Any, Dict
from core.rich_data import BANKS, COMMON

def level_tag(title: str) -> str:
    m = re.match(r"\[(L[0-4])\]", title or "")
    return m.group(1) if m else "L0"

def clean_topic(title: str) -> str:
    t = re.sub(r"^\[L[0-4]\]\s*", "", title or "").strip()
    t = re.sub(r"\s*[—\-]\s*(آشنایی|مقدماتی|ادمین|مهندس|خبره).*$", "", t, flags=re.I)
    return t.strip() or (title or "موضوع")

def _fmt_cmds(pairs):
    return "\n".join(f"```\n{cmd}\n```\n→ {desc}\n" for cmd, desc in pairs)

def build_rich_lesson(title_fa: str, title_en: str = "", level: str | None = None) -> Dict[str, Any]:
    try:
        from core.chapter03_teacher import build_chapter03_lesson
        if any(k in (title_fa or "") for k in ("BIOS", "UEFI", "بوت", "Boot", "Secure Boot", "TPM", "CMOS", "GRUB", "BOOTMGR", "زنجیره", "فیرمور", "ESP", "Bootloader", "PXE", "BCD", "Setup")):
            c = build_chapter03_lesson(title_fa, title_en)
            if c: return c
    except Exception:
        pass
    try:
        from core.chapter05_teacher import build_chapter05_lesson
        if any(k in (title_fa or "") for k in ("FAT", "exFAT", "NTFS", "ext4", "ext3", "XFS", "Btrfs", "inode", "MBR", "GPT", "پارتیشن", "Partition", "RAID", "Mirror", "Stripe", "fsck", "fstab", "mount", "Volume", "BitLocker", "mdadm", "فایل‌سیستم", "parity", "Rebuild")):
            c = build_chapter05_lesson(title_fa, title_en)
            if c: return c
    except Exception:
        pass
    try:
        from core.chapter04_teacher import build_chapter04_lesson
        if any(k in (title_fa or "") for k in ("Kernel", "هسته", "Registry", "ویندوز", "Windows", "لینوکس", "Linux", "سلسله‌مراتب", "systemd", "journalctl", "CPU بالا", "منابع", "Process", "Thread", "Scheduler", "Syscall", "Event Viewer", "Services", "chmod", "FHS", "swap", "گلوگاه", "Task Manager", "PowerShell", "عیب‌یابی منابع")):
            c = build_chapter04_lesson(title_fa, title_en)
            if c: return c
    except Exception:
        pass
    try:
        from core.chapter02_teacher import build_chapter02_lesson
        if any(k in (title_fa or "") for k in ("ESD", "ایمنی", "اسمبل", "Beep", "تمیز", "ProLiant", "iLO", "سرور HP", "نگهداری", "خمیر")):
            c = build_chapter02_lesson(title_fa, title_en)
            if c: return c
    except Exception:
        pass
    try:
        from core.chapter01_teacher import build_chapter01_lesson, _bucket, _topic
        topic0 = _topic(title_fa)
        if _bucket(topic0) in ("cpu", "ram", "storage", "mb", "psu") or any(k in (title_fa or "") for k in ("CPU", "ALU", "RAM", "DDR", "SSD", "HDD", "NVMe", "مادربرد", "Chipset", "PSU", "تغذیه", "حافظه", "ذخیره", "سوکت")):
            if not any(k in (title_fa or "") for k in ("BIOS", "UEFI", "Secure Boot", "Boot", "CPU بالا", "RAID", "NTFS", "ext4")):
                c = build_chapter01_lesson(title_fa, title_en)
                if c: return c
    except Exception:
        pass
    level = level or level_tag(title_fa)
    topic = clean_topic(title_fa)
    summary = f"«{topic}» ({level}): مفهوم، دستورات، Lab."
    full = f"# {topic}\n\n**سطح:** {level}\n\n{summary}\n"
    commands = "## پایه\n" + _fmt_cmds(COMMON[:8])
    lab = f"## آزمایشگاه — {topic}\n1) بخوان 2) اجرا کن 3) یادداشت کن\n"
    return {"summary": summary, "full_content": full, "commands": commands, "examples": lab, "notes": "", "level": level, "topic": topic, "category": "general"}
