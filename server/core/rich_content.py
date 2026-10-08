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
        from core.chapter10_teacher import build_chapter10_lesson
        if any(k in (title_fa or "") for k in ("DNS", "Resolver", "AAAA", "CNAME", "MX", "TXT", "SOA", "PTR", "SRV", "Split-Horizon", "Forwarder", "DNSSEC", "رکورد", "Zone Transfer", "TTL", "Recursive", "Authoritative", "DoH", "DoT", "A AAAA", "Conditional", "nslookup")):
            c = build_chapter10_lesson(title_fa, title_en)
            if c: return c
    except Exception:
        pass
    try:
        from core.chapter09_teacher import build_chapter09_lesson
        if any(k in (title_fa or "") for k in ("ARP", "Request Reply", "ICMP", "Echo", "Three-way", "Handshake", "TCP", "UDP", "Sequence", "Window", "SYN", "FIN", "RST", "Gratuitous", "traceroute", "Time Exceeded", "Destination Unreachable", "datagram", "بدون اتصال", "اتصال‌گرا", "سه دست", "ویژگی‌ها")):
            c = build_chapter09_lesson(title_fa, title_en)
            if c: return c
    except Exception:
        pass
    try:
        from core.chapter08_teacher import build_chapter08_lesson
        if any(k in (title_fa or "") for k in ("IPv4", "IPv6", "Subnet", "ساب‌نت", "ماسک", "Mask", "CIDR", "VLSM", "ساختار آدرس", "128 بیتی", "SLAAC", "fe80", "NDP", "سگمنت", "RFC1918", "طرح سازمانی", "Users", "DMZ", "اکتت", "128")):
            c = build_chapter08_lesson(title_fa, title_en)
            if c: return c
    except Exception:
        pass
    try:
        from core.chapter07_teacher import build_chapter07_lesson
        if any(k in (title_fa or "") for k in ("فریم", "Frame", "اترنت", "Ethernet", "MAC Table", "Learning", "Store-and-Forward", "سوییچ", "Switch", "100M", "1G", "10G", "Duplex", "FCS", "CRC", "Flood", "CAM", "MTU", "SFP")):
            c = build_chapter07_lesson(title_fa, title_en)
            if c: return c
    except Exception:
        pass
    try:
        from core.chapter06_teacher import build_chapter06_lesson
        if any(k in (title_fa or "") for k in ("LAN", "WAN", "WLAN", "OSI", "لایه فیزیکی", "TCP/IP", "مدل چهار", "Packet", "مسیر بسته", "Encapsulation", "توپولوژی", "Broadcast", "Unicast", "Gateway", "مبانی شبکه", "دیتا لینک", "MAC Address")):
            if not any(k in (title_fa or "") for k in ("IPv4", "IPv6", "Subnet", "ARP", "ICMP", "DNS", "Three-way")):
                c = build_chapter06_lesson(title_fa, title_en)
                if c: return c
    except Exception:
        pass
    try:
        from core.chapter03_teacher import build_chapter03_lesson
        if any(k in (title_fa or "") for k in ("BIOS", "UEFI", "بوت", "Boot", "Secure Boot", "TPM", "CMOS", "GRUB", "BOOTMGR", "زنجیره", "فیرمور", "ESP", "PXE", "BCD", "Setup")):
            c = build_chapter03_lesson(title_fa, title_en)
            if c: return c
    except Exception:
        pass
    try:
        from core.chapter05_teacher import build_chapter05_lesson
        if any(k in (title_fa or "") for k in ("FAT", "exFAT", "NTFS", "ext4", "XFS", "MBR", "GPT", "پارتیشن", "RAID", "Mirror", "fsck", "fstab", "mount", "mdadm")):
            c = build_chapter05_lesson(title_fa, title_en)
            if c: return c
    except Exception:
        pass
    try:
        from core.chapter04_teacher import build_chapter04_lesson
        if any(k in (title_fa or "") for k in ("Kernel", "هسته", "Registry", "ویندوز", "Windows", "لینوکس", "Linux", "سلسله‌مراتب", "systemd", "CPU بالا", "منابع", "Process", "Syscall", "Event Viewer", "Services", "FHS", "swap", "گلوگاه", "Task Manager", "PowerShell")):
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
            if not any(k in (title_fa or "") for k in ("BIOS", "UEFI", "Boot", "CPU بالا", "RAID", "LAN", "فریم", "IPv4", "TCP", "DNS")):
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
