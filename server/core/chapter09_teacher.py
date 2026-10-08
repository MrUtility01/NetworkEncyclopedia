# -*- coding: utf-8 -*-
"""فصل ۰۹ — ARP · ICMP · TCP · UDP"""
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
    if any(k in t for k in ("udp", "ویژگی", "ویژگی‌ها", "datagram", "connectionless", "بدون اتصال")):
        return "udp"
    if any(k in t for k in ("tcp", "handshake", "three-way", "سه دست", "sequence", "window", "syn", "fin", "rst", "اتصال‌گرا")):
        return "tcp"
    if any(k in t for k in ("icmp", "echo", "ping", "unreachable", "ttl", "time exceeded")):
        return "icmp"
    if any(k in t for k in ("arp", "request", "reply", "gratuitous", "proxy arp")):
        return "arp"
    return "arp"

def _depth(level: str) -> str:
    return {"L0": "تصویر ذهنی", "L1": "فریم‌به‌فریم+Lab", "L2": "دستور و عیب‌یابی", "L3": "تحلیل پکت", "L4": "امنیت"}.get(level, "")

def _arp(topic, level):
    summary = f"«{topic}»: ARP می‌پرسد این IP کدام MAC است تا فریم Ethernet ساخته شود."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## تشبیه
پرسیدن در راهرو: کی IP 192.168.1.10 را دارد؟

## Request / Reply
1) Request پخش (broadcast)
2) Reply با MAC (unicast)
3) کش ARP به‌روز می‌شود

## فریم‌به‌فریم قبل از ping
هم‌ساب‌نت؟ → کش خالی؟ → Request → Reply → فریم با Dest MAC

## خاص
Gratuitous ARP | Proxy ARP | Incomplete

## عیب‌یابی
ping LAN fail → ARP/VLAN/کابل | MAC اشتباه → تداخل IP/spoof
"""
    commands = """```
arp -a
```
```
ip neigh
```
```
ping -c 1 <gw>
ip neigh
```
"""
    lab = """# Lab ARP
قبل/بعد پینگ به GW جدول arp/neigh را ببین. IP خاموش → incomplete؟
"""
    return summary, full, commands, lab

def _icmp(topic, level):
    summary = f"«{topic}»: ICMP پیام کنترل/خطای لایه ۳ است؛ ping فقط Echo است."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## Echo
Request → Reply | نبودن Reply ≠ همیشه میزبان مرده (فیلتر ICMP)

## پیام‌های رایج
Destination Unreachable | Time Exceeded (traceroute)

## فریم traceroute
TTL=1 → روتر اول Time Exceeded → TTL=2 → ...

## تفسیر ping
GW OK → LAN زنده | 8.8.8.8 OK → مسیر عمومی | IP OK نام نه → DNS
"""
    commands = """```
ping -c 4 8.8.8.8
```
```
ping -n 4 <gateway>
```
```
traceroute -n 8.8.8.8
```
```
tracert -d 8.8.8.8
```
"""
    lab = """# Lab ICMP
پینگ 127.0.0.1 و GW و 8.8.8.8 — جدول OK/Fail. traceroute کجا ستاره می‌دهد؟
"""
    return summary, full, commands, lab

def _tcp(topic, level):
    summary = f"«{topic}»: TCP اتصال‌گرا؛ سه دست‌دهی SYN → SYN-ACK → ACK جلسه را باز می‌کند."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## سه دست‌دهی
Client SYN → Server SYN+ACK → Client ACK

## FIN / RST
پایان مرتب در برابر قطع ناگهانی

## Sequence و Window
شماره‌گذاری بایت‌ها + کنترل جریان؛ از دست رفتن → retransmit

## عیب‌یابی
SYN بدون جواب → فایروال/سرویس | RST → پورت بسته | retransmit زیاد → loss
"""
    commands = """```
ss -tan
```
```
Test-NetConnection <host> -Port 443
```
```
nc -vz <host> 443
```
"""
    lab = """# Lab TCP
ss -tuln پورت‌های LISTEN. Test-NetConnection به 443. اگر SYN-ACK نیاید سه فرضیه بنویس.
"""
    return summary, full, commands, lab

def _udp(topic, level):
    summary = f"«{topic}»: UDP بدون اتصال و سبک؛ DNS و VoIP؛ بدون تضمین رسیدن/ترتیب."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## در برابر TCP
بدون دست‌دهی | سربار کم | مسئولیت با لایه بالاتر

## فریم DNS
UDP query به پورت 53 → جواب؛ اگر نرسید client دوباره می‌فرستد

## عیب‌یابی
TCP OK و UDP نه → ACL روی UDP | VoIP تقطیع → loss/jitter
"""
    commands = """```
ss -uln
```
```
nslookup google.com
```
```
Resolve-DnsName google.com
```
"""
    lab = """# Lab UDP
ss -uln | DNS resolve یک‌بار | چرا بازارسال TCP برای صوت زنده بد است؟
"""
    return summary, full, commands, lab

_BUILDERS = {"arp": _arp, "icmp": _icmp, "tcp": _tcp, "udp": _udp}

def build_chapter09_lesson(title_fa: str, title_en: str = "") -> Dict[str, Any] | None:
    topic, level = _topic(title_fa), _level(title_fa)
    b = _bucket(topic)
    summary, full, commands, lab = _BUILDERS[b](topic, level)
    return {
        "summary": summary, "full_content": full, "commands": commands,
        "examples": lab, "notes": f"فصل۰۹ · {b} · {level}", "lab": lab,
        "level": level, "topic": topic, "category": b, "chapter": 9,
    }
