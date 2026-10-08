# -*- coding: utf-8 -*-
"""فصل ۰۶ — مبانی شبکه: LAN/WAN · OSI · TCP/IP · MAC/IP · مسیر بسته"""
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
    if any(k in t for k in ("packet", "مسیر بسته", "journey", "encapsulation", "کپسول", "از app", "app تا")):
        return "journey"
    if any(k in t for k in ("mac", "آدرس", "ipv4", "ipv6", "arp", "ترافیک", "unicast", "broadcast", "multicast")):
        return "addr"
    if any(k in t for k in ("tcp/ip", "tcpip", "چهار لایه", "مدل چهار", "udp", "tcp ")):
        return "tcpip"
    if any(k in t for k in ("osi", "لایه", "layer", "فیزیکی", "دیتا لینک", "transport", "application", "لایه ۷", "لایه 7")):
        return "osi"
    if any(k in t for k in ("lan", "wan", "man", "wlan", "انواع شبکه", "topology", "توپولوژی")):
        return "types"
    return "types"

def _depth(level: str) -> str:
    return {"L0": "تصویر ذهنی", "L1": "مثال+Lab", "L2": "دستور ادمین", "L3": "تحلیل مسیر", "L4": "طراحی"}.get(level, "")

def _types(topic, level):
    summary = f"«{topic}»: LAN نزدیک و سریع؛ WAN گسترده. شبکه = دستگاه‌هایی که داده رد و بدل می‌کنند."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## تشبیه
LAN = حرف داخل ساختمان | WAN = تماس بین شهرها | WLAN = LAN بی‌سیم

## مقایسه
| نوع | محدوده | نکته |
|-----|--------|------|
| LAN | ساختمان | سوییچ، بعداً VLAN |
| WLAN | همان با Wi-Fi | تداخل و امنیت |
| WAN | بین سایت‌ها | تأخیر و SLA |

## Client–Server
درخواست به سرور مرکزی در برابر Peer هم‌سطح.

## خلاصه
اول کجا (LAN/WAN)، بعد آدرس، بعد پروتکل.
"""
    commands = """```
ipconfig /all
```
```
Get-NetAdapter | Format-Table Name, Status, LinkSpeed, MacAddress
```
```
ip -br link
```
```
ip -br addr
```
"""
    lab = """# Lab انواع شبکه
ipconfig یا ip addr: خصوصی است یا عمومی؟ Gateway چیست؟ کدام کارت Up است؟
"""
    return summary, full, commands, lab

def _osi(topic, level):
    summary = f"«{topic}»: OSI هفت لایه = زبان مشترک عیب‌یابی؛ از کابل تا اپلیکیشن."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## هفت لایه
| # | لایه | کار | مثال |
|---|------|-----|------|
| 1 | Physical | سیگنال/کابل | فیبر، Wi-Fi PHY |
| 2 | Data Link | فریم/MAC | Ethernet |
| 3 | Network | مسیر | IP، روتر |
| 4 | Transport | پورت/قابلیت اطمینان | TCP، UDP |
| 5–7 | بالا | نشست تا اپ | HTTP، DNS، SSH |

## چرا مهم؟
«اینترنت ندارم» را لایه‌لایه بشکن: لینک؟ IP؟ پورت؟ DNS؟

## فریم درخواست وب
مرورگر (۷) → TCP (۴) → IP (۳) → Ethernet (۲/۱)
"""
    commands = """```
ip link show
```
```
ip addr
```
```
ip route
```
```
ipconfig /all
```
```
ss -tuln
```
"""
    lab = """# Lab OSI
کابل شل→۱ | ARP عجیب→۲ | ping GW fail→۳ | IP OK وب نه→۴/۷ | نام resolve نه→DNS
ping 8.8.8.8 OK و google.com نه = کدام لایه/سرویس؟
"""
    return summary, full, commands, lab

def _tcpip(topic, level):
    summary = f"«{topic}»: مدل عملی اینترنت چهار لایه: Link · Internet · Transport · Application."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## چهار لایه
Application ≈ OSI 5–7 | Transport = 4 | Internet = 3 | Link = 1–2

## TCP در برابر UDP
TCP: اتصال، تأیید، بازارسال (وب، SSH)
UDP: سریع، بدون تضمین (DNS اغلب، VoIP)

## پورت
22 SSH، 53 DNS، 80/443 وب — چند سرویس روی یک IP

## سه دست‌دهی TCP
SYN → SYN-ACK → ACK
"""
    commands = """```
ss -tuln
```
```
netstat -an | findstr LISTENING
```
```
ping -c 4 8.8.8.8
```
```
traceroute -n 8.8.8.8
```
```
tracert 8.8.8.8
```
"""
    lab = """# Lab TCP/IP
ss -tuln پورت‌های آشنا را علامت بزن. ping OK ولی وب نه → پورت/DNS.
"""
    return summary, full, commands, lab

def _addr(topic, level):
    summary = f"«{topic}»: MAC لایه ۲ (سوییچ)؛ IP لایه ۳ (روتر). ARP پل IPv4 بین آن‌هاست."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## MAC
روی کارت؛ سوییچ جدول MAC→پورت می‌سازد.

## IP
منطقی و قابل تنظیم. خصوصی (10/172.16/192.168) در برابر عمومی.

## ARP
«این IP کدام MAC؟» Request پخش → Reply → کش.

## Unicast / Broadcast / Multicast
یک‌به‌یک | همه در دامنه | گروه

## فریم ping همسایه LAN
ICMP → ARP برای MAC → فریم Ethernet. خارج ساب‌نت → MAC گیت‌وی.
"""
    commands = """```
ipconfig /all
```
```
arp -a
```
```
ip link
```
```
ip addr
```
```
ip neigh
```
"""
    lab = """# Lab آدرس
MAC و IP خودت را بنویس. بعد از ping به GW جدول arp/neigh را ببین.
چرا به اینترنت MAC گیت‌وی در فریم است نه MAC گوگل؟
"""
    return summary, full, commands, lab

def _journey(topic, level):
    summary = f"«{topic}»: از کلیک تا کابل داده کپسول می‌شود؛ در مقصد باز می‌شود."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## کپسوله‌سازی
داده اپ → +Transport → +IP → +Ethernet → سیگنال
مقصد برعکس باز می‌کند.

## مسیر وب اینترنت
DNS → TCP:443 → پکت IP → فریم به MAC گیت‌وی → روترها TTL-- → NAT ممکن → سرور

## شکست کجا؟
لینک Down | VLAN | IP/GW | مسیر | پورت/فایروال | DNS | اپ
"""
    commands = """```
ping -c 3 8.8.8.8
```
```
traceroute -n 8.8.8.8
```
```
tracert 8.8.8.8
```
```
ip route
```
```
nslookup google.com
```
"""
    lab = """# Lab مسیر بسته
1) ping GW 2) ping 8.8.8.8 3) ping نام دامنه — جدول OK/Fail
traceroute ببین کجا می‌ایستد.
"""
    return summary, full, commands, lab

_BUILDERS = {"types": _types, "osi": _osi, "tcpip": _tcpip, "addr": _addr, "journey": _journey}

def build_chapter06_lesson(title_fa: str, title_en: str = "") -> Dict[str, Any] | None:
    topic, level = _topic(title_fa), _level(title_fa)
    b = _bucket(topic)
    summary, full, commands, lab = _BUILDERS[b](topic, level)
    return {
        "summary": summary, "full_content": full, "commands": commands,
        "examples": lab, "notes": f"فصل۰۶ · {b} · {level}", "lab": lab,
        "level": level, "topic": topic, "category": b, "chapter": 6,
    }
