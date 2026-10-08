# -*- coding: utf-8 -*-
"""فصل 04 — سیستم‌عامل پایه: Kernel / Windows / Linux / عیب‌یابی منابع"""
from __future__ import annotations
import re
from typing import Any, Dict, Tuple

def _level(title: str) -> str:
    m = re.match(r"\[(L[0-4])\]", title or "")
    return m.group(1) if m else "L0"

def _topic(title: str) -> str:
    t = re.sub(r"^\[L[0-4]\]\s*", "", title or "")
    t = re.sub(r"\s*[\u2014\-]\s*(\u0622\u0634\u0646\u0627\u06cc\u06cc|\u0645\u0642\u062f\u0645\u0627\u062a\u06cc|\u0627\u062f\u0645\u06cc\u0646|\u0645\u0647\u0646\u062f\u0633|\u062e\u0628\u0631\u0647|Intro|Junior|Admin|Senior|Architect).*$", "", t, flags=re.I)
    return t.strip()

def _bucket(topic: str) -> str:
    t = (topic or "").lower()
    if any(k in t for k in ("kernel", "\u0647\u0633\u062a\u0647", "process", "thread", "scheduler", "syscall", "user mode", "\u0645\u0641\u0647\u0648\u0645", "virtual memory")):
        return "kernel"
    if any(k in t for k in ("registry", "\u0648\u06cc\u0646\u062f\u0648\u0632", "windows", "powershell", "event viewer", "task manager", "services")):
        return "windows"
    if any(k in t for k in ("\u0644\u06cc\u0646\u0648\u06a9\u0633", "linux", "\u0633\u0644\u0633\u0644\u0647", "filesystem", "systemd", "chmod", "journalctl", "fhs", "ext4")):
        return "linux"
    if any(k in t for k in ("cpu \u0628\u0627\u0644\u0627", "\u0645\u0646\u0627\u0628\u0639", "resource", "swap", "\u06af\u0644\u0648\u06af\u0627\u0647", "iostat", "bottleneck")):
        return "resource"
    return "kernel"

def _depth(level: str) -> str:
    return {"L0": "\u062a\u0635\u0648\u06cc\u0631 \u0630\u0647\u0646\u06cc", "L1": "\u0645\u062b\u0627\u0644+Lab", "L2": "\u062f\u0633\u062a\u0648\u0631 \u0627\u062f\u0645\u06cc\u0646", "L3": "\u062a\u062d\u0644\u06cc\u0644", "L4": "\u0633\u0627\u0632\u0645\u0627\u0646\u06cc"}.get(level, "")

def _kernel(topic, level):
    summary = f"\u00ab{topic}\u00bb: Kernel \u0648\u0627\u0633\u0637 \u0633\u062e\u062a\u200c\u0627\u0641\u0632\u0627\u0631 \u0648 \u0628\u0631\u0646\u0627\u0645\u0647\u200c\u0647\u0627\u0633\u062a."
    full = f"""# {topic}

**\u0633\u0637\u062d:** {level} \u2014 {_depth(level)}

## \u062a\u0634\u0628\u06cc\u0647
\u0628\u0631\u0646\u0627\u0645\u0647 = \u0645\u0634\u062a\u0631\u06cc | Kernel = \u0622\u0634\u067e\u0632\u062e\u0627\u0646\u0647 | \u0633\u062e\u062a\u200c\u0627\u0641\u0632\u0627\u0631 = \u0627\u062c\u0627\u0642

## User Mode \u062f\u0631 \u0628\u0631\u0627\u0628\u0631 Kernel Mode
User: \u0628\u0631\u0646\u0627\u0645\u0647\u200c\u0647\u0627\u06cc \u0639\u0627\u062f\u06cc | Kernel: \u0647\u0633\u062a\u0647 \u0648 \u062f\u0631\u0627\u06cc\u0648\u0631

## Process \u0648 Thread
Process = \u0628\u0631\u0646\u0627\u0645\u0647 \u062f\u0631 \u062d\u0627\u0644 \u0627\u062c\u0631\u0627 | Thread = \u0645\u0633\u06cc\u0631 \u0627\u062c\u0631\u0627 \u062f\u0627\u062e\u0644 \u0647\u0645\u0627\u0646 process

## \u0641\u0631\u06cc\u0645\u200c\u0628\u0647\u200c\u0641\u0631\u06cc\u0645 read \u0641\u0627\u06cc\u0644
1) read \u062f\u0631 User 2) Syscall 3) \u0645\u062c\u0648\u0632 Kernel 4) Cache \u06cc\u0627 \u062f\u06cc\u0633\u06a9 5) \u0628\u0631\u06af\u0634\u062a \u0628\u0647 User

## Scheduler \u0648 \u062d\u0627\u0641\u0638\u0647 \u0645\u062c\u0627\u0632\u06cc
\u0646\u0648\u0628\u062a\u200c\u062f\u0647\u06cc CPU | Page \u0628\u0647 RAM \u06cc\u0627 swap
"""
    commands = """```\ntasklist\n```\n```\nGet-Process | Sort-Object CPU -Descending | Select -First 10\n```\n```\nps aux --sort=-%cpu | head\n```\n```\nfree -h\n```\n```\nuname -r\n```\n"""
    lab = """# Lab Kernel\nTask Manager / ps \u0631\u0627 \u0628\u0628\u06cc\u0646. \u0628\u0627\u0631 \u0628\u062f\u0647 \u0648 process \u067e\u0631\u0645\u0635\u0631\u0641 \u0631\u0627 \u067e\u06cc\u062f\u0627 \u06a9\u0646.\n"""
    return summary, full, commands, lab

def _windows(topic, level):
    summary = f"\u00ab{topic}\u00bb: \u0648\u06cc\u0646\u062f\u0648\u0632 \u0627\u062f\u0645\u06cc\u0646 = Services + Event Log + Registry(\u0628\u0627 \u0627\u062d\u062a\u06cc\u0627\u0637) + PowerShell."
    full = f"""# {topic}

**\u0633\u0637\u062d:** {level} \u2014 {_depth(level)}

## Registry
HKLM = \u0633\u06cc\u0633\u062a\u0645 | HKCU = \u06a9\u0627\u0631\u0628\u0631. \u0642\u0628\u0644 \u0627\u0632 \u062a\u063a\u06cc\u06cc\u0631 Export/\u0628\u06a9\u0627\u067e.

## Services \u0648 Event Viewer
\u0633\u0631\u0648\u06cc\u0633\u200c\u0647\u0627\u06cc \u067e\u0633\u200c\u0632\u0645\u06cc\u0646\u0647 | \u0644\u0627\u06af \u0628\u0631\u0627\u06cc RCA \u0632\u0645\u0627\u0646\u06cc

## NTFS \u0645\u062c\u0648\u0632
Share + NTFS \u2014 \u0633\u062e\u062a\u200c\u06af\u06cc\u0631\u0627\u0646\u0647\u200c\u062a\u0631 \u0628\u0631\u0646\u062f\u0647 \u0627\u0633\u062a.
"""
    commands = """```\nwinver\n```\n```\nsysteminfo\n```\n```\nGet-Service | Where-Object Status -ne Running | Select -First 15\n```\n```\nGet-WinEvent -LogName System -MaxEvents 15\n```\n```\nGet-Process | Sort CPU -Desc | Select -First 8\n```\n"""
    lab = """# Lab \u0648\u06cc\u0646\u062f\u0648\u0632\nwinver + systeminfo | services.msc (\u0641\u0642\u0637 \u0645\u0634\u0627\u0647\u062f\u0647) | Event Viewer \u062e\u0637\u0627\u0647\u0627\u06cc 24\u0633\u0627\u0639\u062a\n"""
    return summary, full, commands, lab

def _linux(topic, level):
    summary = f"\u00ab{topic}\u00bb: \u0644\u06cc\u0646\u0648\u06a9\u0633 = \u0641\u0627\u06cc\u0644\u200c\u0633\u06cc\u0633\u062a\u0645 + process + permission + systemd."
    full = f"""# {topic}

**\u0633\u0637\u062d:** {level} \u2014 {_depth(level)}

## FHS
/etc \u062a\u0646\u0638\u06cc\u0645\u0627\u062a | /var \u0644\u0627\u06af | /home \u06a9\u0627\u0631\u0628\u0631 | /proc \u0646\u0645\u0627\u06cc Kernel | /boot \u0628\u0648\u062a

## rwx \u0648 systemd
chmod/chown \u0628\u0627 \u0627\u062d\u062a\u06cc\u0627\u0637 | systemctl + journalctl
"""
    commands = """```\nuname -a\n```\n```\ncat /etc/os-release\n```\n```\nls /\n```\n```\ndf -h\n```\n```\nsystemctl list-units --failed\n```\n```\njournalctl -p err -n 20 --no-pager\n```\n```\nfree -h && uptime\n```\n"""
    lab = """# Lab Linux\nls /etc /var/log /proc | systemctl status | journalctl -p err\n"""
    return summary, full, commands, lab

def _resource(topic, level):
    summary = f"\u00ab{topic}\u00bb: \u06a9\u0646\u062f\u06cc = \u06a9\u062f\u0627\u0645 \u0645\u0646\u0628\u0639\u061f CPU / RAM / Disk / Network."
    full = f"""# {topic}

**\u0633\u0637\u062d:** {level} \u2014 {_depth(level)}

## \u0686\u0647\u0627\u0631 \u06af\u0644\u0648\u06af\u0627\u0647
CPU | Memory/swap | Disk I/O | Network

## \u0645\u0633\u06cc\u0631 RCA
\u0639\u0644\u0627\u0645\u062a \u2192 Scope \u2192 CPU? RAM? Disk? Net? \u2192 \u062f\u0644\u06cc\u0644 \u2192 \u0627\u0635\u0644\u0627\u062d
"""
    commands = """```\nGet-Process | Sort CPU -Desc | Select -First 10\n```\n```\nuptime\n```\n```\nmpstat 1 5\n```\n```\nfree -h\n```\n```\nvmstat 1 5\n```\n```\niostat -xz 1 5\n```\n"""
    lab = """# Lab \u0645\u0646\u0627\u0628\u0639\nBaseline \u2192 \u0628\u0627\u0631 \u2192 \u0645\u0642\u0627\u06cc\u0633\u0647 CPU/RAM/Disk \u2192 \u06cc\u06a9 \u062c\u0645\u0644\u0647 RCA\n"""
    return summary, full, commands, lab

_BUILDERS = {"kernel": _kernel, "windows": _windows, "linux": _linux, "resource": _resource}

def build_chapter04_lesson(title_fa: str, title_en: str = "") -> Dict[str, Any] | None:
    topic, level = _topic(title_fa), _level(title_fa)
    b = _bucket(topic)
    summary, full, commands, lab = _BUILDERS[b](topic, level)
    return {
        "summary": summary, "full_content": full, "commands": commands,
        "examples": lab, "notes": f"\u0641\u0635\u0644\u06f0\u06f4 \u00b7 {b} \u00b7 {level}", "lab": lab,
        "level": level, "topic": topic, "category": b, "chapter": 4,
    }
