# -*- coding: utf-8 -*-
"""فصل ۱۱ — DHCP و IPAM: DORA · Options · Relay · IPAM"""
from __future__ import annotations
import re
from typing import Any, Dict, Tuple

def _level(title: str) -> str:
    m = re.match(r"\[(L[0-4])\]", title or "")
    return m.group(1) if m else "L0"

def _topic(title: str) -> str:
    t = re.sub(r"^\[L[0-4]\]\s*", "", title or "")
    t = re.sub(r"\s*[—\-]\s*(آشنایی|مقدماتی|ادمین|مهندس|خبره|Intro|Junior|Admin|Senior|Architect).*$", "", t, flags=re.I)
    return t.strip()

def _bucket(topic: str) -> str:
    t = (topic or "").lower()
    if any(k in t for k in ("ipam", "مفهوم ipam", "inventory", "address management")):
        return "ipam"
    if any(k in t for k in ("relay", "helper", "failover", "scope", "reservation", "سازمان", "split scope")):
        return "enterprise"
    if any(k in t for k in ("option", "router option", "dns option", "lease", "ntp", "pxe", "option 43", "option 66", "option 67")):
        return "options"
    if any(k in t for k in ("dora", "discover", "offer", "request", "ack", "dhcp", "renew", "rebind", "nak")):
        return "dora"
    return "dora"

def _depth(level: str) -> str:
    return {"L0": "تصویر ذهنی", "L1": "فریم‌به‌فریم+Lab", "L2": "دستور ادمین", "L3": "طراحی", "L4": "HA و IPAM"}.get(level, "")

def _dora(topic, level):
    summary = f"«{topic}»: DHCP با DORA آدرس می‌دهد: Discover → Offer → Request → Ack."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## تشبیه هتل
Discover جای خالی | Offer پیشنهاد | Request انتخاب | Ack کلید

## فریم‌به‌فریم
1) Discover پخش 2) Offer 3) Request 4) Ack — بدون Ack هنوز مستأجر نیستی. NAK = از نو.

## Lease
Renew حدود نیمه عمر | Rebind اگر renew شکست

## پورت
UDP 67 سرور | UDP 68 کلاینت

## عیب‌یابی
169.254 = APIPA | IP می‌گیرد اینترنت نه = Option بد
"""
    commands = """```
ipconfig /all
```
```
ipconfig /release
ipconfig /renew
```
```
ip addr
```
```
nmcli device show
```
"""
    lab = """# Lab DORA
Lease و DHCP Server را از ipconfig بخوان. اگر 169.254 دیدی سه فرضیه بنویس.
"""
    return summary, full, commands, lab

def _options(topic, level):
    summary = f"«{topic}»: Optionها Gateway، DNS، دامنه، NTP، PXE را همراه IP می‌آورند."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## حیاتی
Router/GW | DNS | Domain | Lease Time | NTP | PXE (66/67)

## بعد از Ack
IP + مسیر پیش‌فرض + resolver تنظیم می‌شود

## اشتباه
DNS غلط → نام داخلی fail | GW غلط → فقط LAN
"""
    commands = """```
ipconfig /all
```
```
Get-DhcpServerv4OptionValue -ScopeId 192.168.1.0
```
"""
    lab = """# Lab Options
جدول IP/Mask/GW/DNS/DHCP Server را پر کن. کدام از DHCP آمده؟
"""
    return summary, full, commands, lab

def _enterprise(topic, level):
    summary = f"«{topic}»: Relay (helper) Discover را از VLAN به سرور DHCP مرکزی می‌رساند."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## چرا Relay؟
Broadcast از روتر رد نمی‌شود؛ helper unicast به سرور می‌فرستد.

## Scope / Reservation / Exclusion
استخر ساب‌نت | IP ثابت برای MAC | آدرس‌های خارج از pool (GW/سرور)

## Failover
دو سرور با همگام lease برای HA

## عیب‌یابی
یک VLAN fail → helper روی SVI؟ | همه fail → سرویس DHCP
"""
    commands = """```
show running-config | include helper
```
```
Get-DhcpServerv4Scope
```
```
Get-DhcpServerv4Lease -ScopeId 10.10.10.0
```
"""
    lab = """# Lab Relay
سه VLAN: کجا helper و کجا scope؟ reservation برای پرینتر را توضیح بده.
"""
    return summary, full, commands, lab

def _ipam(topic, level):
    summary = f"«{topic}»: IPAM موجودی آدرس‌ها — کی چه ساب‌نتی دارد و کجا تداخل است."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## چرا
بدون IPAM: IP تکراری و اکسل مرده. با IPAM: نقشه، گزارش، اتصال به DNS/DHCP در ابزارهای پیشرفته.

## حداقل ستون‌ها
Prefix | VLAN | هدف | GW | DHCP range | Static | مالک

## تخصیص جدید
درخواست → پیدا کردن بلوک → VLAN/فایروال → ثبت DHCP/static → مستند همان روز
"""
    commands = """```
ip -br addr
```
```
Get-DhcpServerv4Scope
```
"""
    lab = """# Lab IPAM
دفتر ۲۰ نفره: Users/24، Servers/28، Mgmt/28. چرا GW را exclusion می‌کنی؟
"""
    return summary, full, commands, lab

_BUILDERS = {"dora": _dora, "options": _options, "enterprise": _enterprise, "ipam": _ipam}

def build_chapter11_lesson(title_fa: str, title_en: str = "") -> Dict[str, Any] | None:
    topic, level = _topic(title_fa), _level(title_fa)
    b = _bucket(topic)
    summary, full, commands, lab = _BUILDERS[b](topic, level)
    return {
        "summary": summary, "full_content": full, "commands": commands,
        "examples": lab, "notes": f"فصل۱۱ · {b} · {level}", "lab": lab,
        "level": level, "topic": topic, "category": b, "chapter": 11,
    }
