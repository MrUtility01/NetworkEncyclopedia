# -*- coding: utf-8 -*-
"""فصل ۱۲ — کابل مسی · فیبر · رک · فیزیک DC · تست"""
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
    if any(k in t for k in ("wiremap", "certif", "fluke", "tdr", "otdr", "تست", "next", "continuity")):
        return "test"
    if any(k in t for k in ("برق", "ups", "pdu", "دو مسیر", "cooling", "خنک", "دیتاسنتر", "redundan")):
        return "dc"
    if any(k in t for k in ("رک", "rack", "واحد u", "cabinet", "patch panel", "مدیریت کابل")):
        return "rack"
    if any(k in t for k in ("om1", "om2", "om3", "om4", "om5", "os1", "os2", "فیبر", "fiber", "lc", "sc", "mpo", "smf", "mmf")):
        return "fiber"
    if any(k in t for k in ("cat5", "cat6", "cat7", "مسی", "copper", "rj45", "utp", "stp", "t568", "poe")):
        return "copper"
    return "copper"

def _depth(level: str) -> str:
    return {"L0": "تصویر ذهنی", "L1": "جدول+Lab", "L2": "چک‌لیست ادمین", "L3": "طراحی", "L4": "استاندارد DC"}.get(level, "")

def _copper(topic, level):
    summary = f"«{topic}»: Cat5e برای 1G؛ Cat6/6A برای مسیر بهتر و 10G در طراحی درست."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## رده‌ها
Cat5e ≈ 1G/100m | Cat6 1G + 10G کوتاه | Cat6A مناسب‌تر برای 10G کانال کامل

## T568A/B
دو سر یکسان = straight-through. PoE روی همان کابل برای AP/دوربین.

## فریم لینک
Autoneg → لینک Up → wiremap/CRC اگر جفت خراب باشد
"""
    commands = """```
ethtool eth0
```
```
Get-NetAdapter | Format-Table Name, LinkSpeed, Status
```
```
show interfaces status
```
"""
    lab = """# Lab مسی
برچسب Cat را بخوان. LinkSpeed با پچ دیگر عوض می‌شود؟ برای 10G رک‌مجاور Cat6 یا 6A؟
"""
    return summary, full, commands, lab

def _fiber(topic, level):
    summary = f"«{topic}»: OM مالتی‌مد فاصله کوتاه؛ OS سینگل‌مد فاصله بلند. LC رایج روی SFP."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## OM در برابر OS
هسته پهن/فاصله کوتاه در برابر باریک/فاصله بلند. OM3/OM4 در DC رایج.

## کانکتور
LC | SC | MPO برای تراکم بالا. سر فیبر را تمیز کن؛ خم تند ممنوع.

## فریم
SFP سازگار + پچ تمیز → لینک نوری / توان در محدوده
"""
    commands = """```
show interface transceiver
```
```
ethtool -m eth0 2>/dev/null
```
"""
    lab = """# Lab فیبر
کانکتور LC/SC؟ برچسب OM/OS؟ لینک ۲km بین ساختمان: OM4 یا OS2؟
"""
    return summary, full, commands, lab

def _rack(topic, level):
    summary = f"«{topic}»: رک با واحد U؛ پچ‌پنل و مدیریت کابل و PDU نظم و پایداری می‌آورند."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## U
1U ≈ 1.75 اینچ. سرور 1U/2U، سوییچ اغلب 1U.

## اجزا
ریل | پچ‌پنل | cable management | PDU | blank panel برای هوا

## نصب سوییچ
جای U در مستند → نصب → برق → uplink → برچسب
"""
    commands = """# مستند نمونه: Rack A1 | U10 SW-Access | U20 Server
```
show version
```
"""
    lab = """# Lab رک
ارتفاع رک چند U؟ PDU کجا؟ 42U با ۲ سوییچ و ۴ سرور را روی کاغذ بچین.
"""
    return summary, full, commands, lab

def _dc(topic, level):
    summary = f"«{topic}»: برق دو مسیر و راهروی سرد/گرم پایه پایداری دیتاسنتر است."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## دو مسیر
دو UPS/PDU؛ هر پاور سرور به یک مسیر. تست failover.

## سرمایش
راهروی سرد/گرم؛ blank panel؛ جلوگیری از برگشت هوای گرم.

## قطع مسیر A
اگر طراحی درست باشد پاور B بدون قطعی سرویس را نگه می‌دارد.
"""
    commands = """# iLO/iDRAC: وضعیت PSU و دما
```
sensors 2>/dev/null | head
```
"""
    lab = """# Lab DC
دو پاور سرور به کدام PDUها؟ دما idle در برابر زیر بار.
"""
    return summary, full, commands, lab

def _test(topic, level):
    summary = f"«{topic}»: Wiremap جفت‌ها را چک می‌کند؛ certification گزارش استاندارد کانال است."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## سطوح
Wiremap/پیوستگی → Qualification → Certification | OTDR برای فیبر

## عیب 100M به‌جای 1G
پچ/جفت → تعویض پچ → پورت دیگر → CRC
"""
    commands = """```
show interfaces Gi0/1 | include error|CRC
```
```
ip -s link
```
"""
    lab = """# Lab تست
پچ مشکوک را عوض کن. CRC قبل/بعد. با تستر Wiremap را یادداشت کن.
"""
    return summary, full, commands, lab

_BUILDERS = {"copper": _copper, "fiber": _fiber, "rack": _rack, "dc": _dc, "test": _test}

def build_chapter12_lesson(title_fa: str, title_en: str = "") -> Dict[str, Any] | None:
    topic, level = _topic(title_fa), _level(title_fa)
    b = _bucket(topic)
    summary, full, commands, lab = _BUILDERS[b](topic, level)
    return {
        "summary": summary, "full_content": full, "commands": commands,
        "examples": lab, "notes": f"فصل۱۲ · {b} · {level}", "lab": lab,
        "level": level, "topic": topic, "category": b, "chapter": 12,
    }
