# -*- coding: utf-8 -*-
"""فصل ۱۶ — Multicast: مبانی · PIM · IPTV"""
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
    if any(k in t for k in ("iptv", "کاربرد", "streaming", "ssm", "asm", "anycast rp", "msdp")):
        return "use"
    if any(k in t for k in ("pim", "dense", "sparse", "rp", "rendezvous", "igmp", "mld", "مسیریابی", "join", "prune")):
        return "pim"
    if any(k in t for k in ("multicast", "چرا", "broadcast", "group", "224", "آدرس گروهی", "مبانی")):
        return "basics"
    return "basics"

def _depth(level: str) -> str:
    return {"L0": "تصویر ذهنی", "L1": "فریم‌به‌فریم+Lab", "L2": "دستور IOS", "L3": "طراحی Sparse/SSM", "L4": "IPTV"}.get(level, "")

def _basics(topic, level):
    summary = f"«{topic}»: Multicast یک‌بار ارسال و چند گیرندهٔ عضو گروه — نه Unicast و نه Broadcast."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## تشبیه
سخنرانی در سالن: فقط اعضای گروه می‌شنوند.

## سه مدل
Unicast یک‌به‌یک | Broadcast همه دامنه | Multicast اعضای گروه (IGMP+PIM)

## آدرس
224.0.0.0/4 برای IPv4 multicast

## فریم عضویت
IGMP Join → ثبت لبه → ترافیک فقط به شاخه‌های عضو

## عیب‌یابی
هیچ‌کس نمی‌گیرد → IGMP/PIM/ACL | همه پورت‌ها → بدون IGMP snooping
"""
    commands = """```
show ip igmp groups
```
```
ip maddr
```
```
show ip multicast
```
"""
    lab = """# Lab مبانی
show ip igmp groups | فرق پهنا ۱۰۰۰ کلاینت Unicast در برابر Multicast
"""
    return summary, full, commands, lab

def _pim(topic, level):
    summary = f"«{topic}»: PIM بین روترها؛ Sparse+RP رایج‌تر از Dense در شبکه بزرگ."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## Dense vs Sparse
Dense=اول همه بعد Prune | Sparse=فقط Join با RP

## RP
Rendezvous Point نقطه ملاقات منبع و علاقه‌مندان

## فریم Join
IGMP → روتر لبه Join → درخت PIM → ترافیک روی شاخه عضو

## عیب‌یابی
PIM neighbor؟ mroute؟ unicast تا RP؟
"""
    commands = """```
show ip pim neighbor
```
```
show ip pim rp mapping
```
```
show ip mroute
```
```
interface Gi0/0
 ip pim sparse-mode
```
```
ip pim rp-address 10.0.0.1
```
"""
    lab = """# Lab PIM
neighbor و mroute را ببین. چرا Sparse برای WAN بهتر است؟
"""
    return summary, full, commands, lab

def _use(topic, level):
    summary = f"«{topic}»: IPTV/دوربین؛ IGMP snooping در لبه و PIM در هسته الزامی است."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## IPTV
headend → هسته PIM → لبه IGMP → snooping روی سوییچ دسترسی

## SSM
Source-Specific (S,G) برای ویدیو تمیزتر

## خطا
بدون snooping = flood روی همه پورت‌های VLAN
"""
    commands = """```
show ip igmp snooping groups
```
```
show ip mroute
```
"""
    lab = """# Lab کاربرد
۲۰ دوربین + ۳ مانیتور: Multicast چه کمکی می‌کند؟ چک‌لیست snooping/PIM/ظرفیت
"""
    return summary, full, commands, lab

_BUILDERS = {"basics": _basics, "pim": _pim, "use": _use}

def build_chapter16_lesson(title_fa: str, title_en: str = "") -> Dict[str, Any] | None:
    topic, level = _topic(title_fa), _level(title_fa)
    b = _bucket(topic)
    summary, full, commands, lab = _BUILDERS[b](topic, level)
    return {
        "summary": summary, "full_content": full, "commands": commands,
        "examples": lab, "notes": f"فصل۱۶ · {b} · {level}", "lab": lab,
        "level": level, "topic": topic, "category": b, "chapter": 16,
    }
