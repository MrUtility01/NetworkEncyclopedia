# -*- coding: utf-8 -*-
"""فصل ۰۷ — اترنت و سوییچینگ: فریم · MAC Table · سوییچ · سرعت"""
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
    if any(k in t for k in ("100m", "1g", "10g", "سرعت", "استاندارد", "gigabit", "duplex", "autoneg", "mtu", "jumbo", "sfp")):
        return "speed"
    if any(k in t for k in ("store", "forward", "cut-through", "سوییچ", "switch", "collision", "broadcast domain", "cam")):
        return "switch"
    if any(k in t for k in ("mac table", "learning", "aging", "flood", "unknown unicast", "mac address table")):
        return "mactable"
    if any(k in t for k in ("فریم", "frame", "ethertype", "fcs", "crc", "preamble", "ethernet", "اترنت")):
        return "frame"
    return "frame"

def _depth(level: str) -> str:
    return {"L0": "تصویر ذهنی", "L1": "مثال+Lab", "L2": "دستور ادمین", "L3": "تحلیل", "L4": "طراحی"}.get(level, "")

def _frame(topic, level):
    summary = f"«{topic}»: فریم اترنت بسته لایه ۲ با MAC مبدأ/مقصد است؛ سوییچ روی پاکت را می‌خواند."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## تشبیه
فریم = پاکت نامه داخل ساختمان با آدرس اتاق (MAC).

## ساختار مفهومی
| بخش | نقش |
|-----|-----|
| Dest/Src MAC | مقصد و مبدأ لایه ۲ |
| EtherType | نوع payload (مثلاً IPv4) |
| Payload | اغلب پکت IP |
| FCS (CRC) | تشخیص خرابی |

## فریم‌به‌فریم
IP آماده → ARP برای MAC → فریم روی پورت → سوییچ FCS و جدول MAC → خروج از پورت درست

## خلاصه
فریم زبان سوییچ است؛ IP داخل payload است.
"""
    commands = """```
ip link show
```
```
ipconfig /all
```
```
show interfaces GigabitEthernet0/1
```
```
show interfaces counters errors
```
"""
    lab = """# Lab فریم
MAC خودت را بخوان. پینگ به GW: MAC مقصد فریم کیست؟ CRC اینترفیس نزدیک صفر باشد.
"""
    return summary, full, commands, lab

def _mactable(topic, level):
    summary = f"«{topic}»: سوییچ از Src MAC یاد می‌گیرد؛ Dest ناشناس را flood می‌کند."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## Learning
فریم ورودی → ثبت Src MAC → پورت + aging

## Forwarding
Dest معلوم → unicast همان پورت | Dest نامعلوم → flood در VLAN | Broadcast → پخش

## فریم‌به‌فریم
A می‌فرستد → یادگرفتن MAC-A → اگر B ناشناس flood → جواب B → یادگیری MAC-B

## مشکلات
حلقه بدون STP → جدول ناپایدار | MAC جابه‌جا → کابل/VM/spoof
"""
    commands = """```
show mac address-table
```
```
show mac address-table dynamic
```
```
bridge fdb show
```
```
ip neigh
```
"""
    lab = """# Lab MAC Table
قبل/بعد پینگ show mac address-table را مقایسه کن. بدون سوییچ: arp -a ایده یادگیری را نشان می‌دهد.
"""
    return summary, full, commands, lab

def _switch(topic, level):
    summary = f"«{topic}»: سوییچ لایه ۲؛ Store-and-Forward فریم را چک می‌کند بعد می‌فرستد."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## Hub در برابر Switch
Hub همه را یکجا | Switch جدول MAC و پورت جدا

## Store-and-Forward در برابر Cut-Through
Store: کل فریم + FCS سپس ارسال | Cut: زودتر با Dest MAC — تأخیر کمتر، ریسک فریم خراب

## Collision و Broadcast
هر پورت full-duplex معمولاً collision جدا | یک VLAN = یک broadcast domain تا L3 جدا کند

## فریم‌به‌فریم عبور
ورود → Learning → Lookup → خروج یا flood
"""
    commands = """```
show interfaces status
```
```
show vlan brief
```
```
show spanning-tree summary
```
```
Get-NetAdapter
```
"""
    lab = """# Lab سوییچ
show interfaces status: connected و سرعت؟ دو PC یک VLAN باید ping شوند؛ VLAN جدا بدون روتر نه.
"""
    return summary, full, commands, lab

def _speed(topic, level):
    summary = f"«{topic}»: 100M/1G/10G و duplex دو طرف باید هم‌خوان باشند؛ mismatch → CRC و کندی."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## سرعت رایج
100M (Fast) | 1G (Cat5e/6) | 10G (Cat6a/فیبر/SFP+)

## Autonegotiation
بهترین سرعت مشترک. دستی اشتباه در یک طرف → duplex mismatch

## MTU
پیش‌فرض ~1500؛ Jumbo فقط end-to-end هماهنگ

## فریم لینک Up
لینک فیزیکی → negotiation → Learning → ترافیک
"""
    commands = """```
ethtool eth0
```
```
Get-NetAdapter | Format-Table Name, LinkSpeed, FullDuplex, Status
```
```
show interfaces status
```
```
show interfaces Gi0/1 | include duplex|rate|error
```
"""
    lab = """# Lab سرعت
LinkSpeed روی PC و سوییچ یکی است؟ CRC بالا → کابل/duplex. یک طرف 100 Full دستی و طرف Auto = ریسک mismatch.
"""
    return summary, full, commands, lab

_BUILDERS = {"frame": _frame, "mactable": _mactable, "switch": _switch, "speed": _speed}

def build_chapter07_lesson(title_fa: str, title_en: str = "") -> Dict[str, Any] | None:
    topic, level = _topic(title_fa), _level(title_fa)
    b = _bucket(topic)
    summary, full, commands, lab = _BUILDERS[b](topic, level)
    return {
        "summary": summary, "full_content": full, "commands": commands,
        "examples": lab, "notes": f"فصل۰۷ · {b} · {level}", "lab": lab,
        "level": level, "topic": topic, "category": b, "chapter": 7,
    }
