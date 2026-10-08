# -*- coding: utf-8 -*-
"""فصل ۰۸ — IPv4 · ساب‌نتینگ · IPv6 · طرح سازمانی"""
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
    if any(k in t for k in ("سگمنت", "segment", "طرح", "سازمان", "users", "servers", "dmz", "address plan", "ip plan")):
        return "design"
    if any(k in t for k in ("ipv6", "128", "lla", "gua", "slaac", "link-local", "fe80", "ndp")):
        return "ipv6"
    if any(k in t for k in ("subnet", "ساب‌نت", "ساب نت", "mask", "ماسک", "cidr", "prefix", "vlsm", "wildcard")):
        return "subnet"
    if any(k in t for k in ("ipv4", "ساختار آدرس", "کلاس", "private", "public", "rfc1918", "اکتت")):
        return "ipv4"
    return "ipv4"

def _depth(level: str) -> str:
    return {"L0": "تصویر ذهنی", "L1": "مثال عددی+Lab", "L2": "دستور ادمین", "L3": "VLSM", "L4": "طرح سازمانی"}.get(level, "")

def _ipv4(topic, level):
    summary = f"«{topic}»: IPv4 آدرس ۳۲بیتی لایه ۳ است؛ مثل 192.168.1.10 با ماسک معنی شبکه می‌گیرد."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## تشبیه
MAC = سریال روی جعبه | IP = آدرس روی نقشه مسیر

## ساختار
۳۲ بیت → A.B.C.D | همراه ماسک یا CIDR (مثل /24)

## خصوصی RFC1918
10.0.0.0/8 | 172.16.0.0/12 | 192.168.0.0/16 — در اینترنت route نمی‌شوند؛ معمولاً NAT

## ویژه
127.0.0.1 loopback | آدرس شبکه و broadcast میزبان نیستند

## فریم به خارج LAN
مقصد خارج ساب‌نت → Default Gateway → MAC گیت‌وی روی فریم → روتر
"""
    commands = """```
ipconfig /all
```
```
route print
```
```
ip addr
```
```
ip route
```
"""
    lab = """# Lab IPv4
IP/ماسک/GW/DNS را بنویس. خصوصی است؟ ping 127.0.0.1 باید OK باشد.
"""
    return summary, full, commands, lab

def _subnet(topic, level):
    summary = f"«{topic}»: ساب‌نتینگ بلوک بزرگ را با ماسک/پیشوند به شبکه‌های کوچک‌تر تقسیم می‌کند."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## ایده
ماسک: بیت شبکه در برابر بیت میزبان. /24 = 255.255.255.0

## جدول تقریبی
| Prefix | میزبان مفید تقریبی |
|--------|---------------------|
| /24 | 254 |
| /25 | 126 |
| /30 | 2 |

فرمول: 2 به توان بیت host منهای 2 (شبکه و broadcast).

## مثال /24 → دو /25
192.168.1.0/25 و 192.168.1.128/25

## VLSM
ماسک متفاوت برای سرور/کاربر/لینک.

## هم‌ساب‌نت؟
IP AND ماسک برای خود و مقصد — یکی → ARP مستقیم؛ وگرنه gateway.
"""
    commands = """```
python3 -c "import ipaddress; n=ipaddress.ip_network('192.168.1.0/26'); print(n, n.num_addresses)"
```
```
ip addr
```
```
ipconfig
```
"""
    lab = """# Lab ساب‌نت
10.0.0.0/24 را به دو /25 بشکن. آیا 192.168.1.10/25 و 192.168.1.200/25 هم‌شبکه‌اند؟
"""
    return summary, full, commands, lab

def _ipv6(topic, level):
    summary = f"«{topic}»: IPv6 آدرس ۱۲۸بیتی هگز با : و فشرده‌سازی :: است."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## نوشتار
2001:db8::1 | :: یک‌بار برای صفرهای متوالی | fe80:: link-local

## انواع
Link-Local | GUA | ULA | Multicast (به‌جای broadcast کلاسیک)

## NDP
جایگزین ARP روی لینک؛ RA برای پیشوند.

## SLAAC / DHCPv6
ساخت آدرس از پیشوند روتر یا تخصیص متمرکز.
"""
    commands = """```
ip -6 addr
```
```
ip -6 route
```
```
ip -6 neigh
```
```
netsh interface ipv6 show address
```
"""
    lab = """# Lab IPv6
ip -6 addr: fe80 داری؟ اگر GUA دیدی پیشوند چیست؟ NDP در برابر ARP یک جمله.
"""
    return summary, full, commands, lab

def _design(topic, level):
    summary = f"«{topic}»: طرح آدرس = Users/Servers/DMZ/Mgmt هر کدام بلوک خود برای رشد و فایروال."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## اصول
جداسازی منطقی | اندازه مناسب | قابل summarize | مستند IPAM

## نمونه اسکلت
| سگمنت | مثال |
|--------|------|
| Users | 10.10.10.0/24 |
| Servers | 10.10.20.0/24 |
| DMZ | 10.10.30.0/24 |
| Mgmt | 10.10.99.0/24 |

## اشتباه
یک /16 تخت برای همه | Guest قاطی Servers | فراموش Management
"""
    commands = """```
ip -br addr
```
```
ip route
```
```
show ip interface brief
```
"""
    lab = """# Lab طرح
شرکت ۱۰۰ نفره + ۲۰ سرور + Guest: سه ساب‌نت با /x و هدف بنویس. چرا Mgmt جدا؟
"""
    return summary, full, commands, lab

_BUILDERS = {"ipv4": _ipv4, "subnet": _subnet, "ipv6": _ipv6, "design": _design}

def build_chapter08_lesson(title_fa: str, title_en: str = "") -> Dict[str, Any] | None:
    topic, level = _topic(title_fa), _level(title_fa)
    b = _bucket(topic)
    summary, full, commands, lab = _BUILDERS[b](topic, level)
    return {
        "summary": summary, "full_content": full, "commands": commands,
        "examples": lab, "notes": f"فصل۰۸ · {b} · {level}", "lab": lab,
        "level": level, "topic": topic, "category": b, "chapter": 8,
    }
