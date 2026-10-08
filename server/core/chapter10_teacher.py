# -*- coding: utf-8 -*-
"""فصل ۱۰ — DNS: Resolver · رکوردها · سازمانی · امنیت"""
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
    if any(k in t for k in ("dnssec", "doh", "dot", "tsig", "امنیت", "spoof", "cache poison")):
        return "security"
    if any(k in t for k in ("split", "horizon", "forwarder", "conditional", "سازمان", "zone transfer", "primary", "secondary", "stub")):
        return "enterprise"
    if any(k in t for k in ("aaaa", "a aaaa", "mx", "cname", "txt", "ns", "soa", "ptr", "srv", "رکورد", "record")):
        return "records"
    if any(k in t for k in ("resolver", "recursive", "iterative", "cache", "ttl", "query", "مبانی", "root", "tld")):
        return "basics"
    if "aaaa" in t or re.search(r"\ba\b", t):
        return "records"
    return "basics"

def _depth(level: str) -> str:
    return {"L0": "تصویر ذهنی", "L1": "فریم‌به‌فریم+Lab", "L2": "دستور ادمین", "L3": "طراحی سازمانی", "L4": "امنیت"}.get(level, "")

def _basics(topic, level):
    summary = f"«{topic}»: DNS نام را به IP تبدیل می‌کند؛ Resolver می‌پرسد و اغلب cache می‌کند."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## تشبیه
دفترچه تلفن اینترنت: نام → شماره (IP)

## نقش‌ها
Client/Stub | Recursive Resolver | Authoritative NS

## فریم‌به‌فریم
نام → OS از resolver می‌پرسد → cache؟ → root/TLD/auth یا forwarder → A/AAAA + TTL

## Recursive در برابر Iterative
«کامل پیدا کن» در برابر «بعدی را بگو»

## TTL
بالا = cache طولانی‌تر؛ پایین = تغییر سریع‌تر

## عیب‌یابی
IP OK و نام نه = DNS | کندی صفحات = resolver/timeout
"""
    commands = """```
nslookup google.com
```
```
Resolve-DnsName google.com
```
```
dig google.com +short
```
```
resolvectl status
```
```
ipconfig /flushdns
```
"""
    lab = """# Lab Resolver
nslookup/dig: کدام سرور جواب داد؟ ping IP در برابر ping نام.
"""
    return summary, full, commands, lab

def _records(topic, level):
    summary = f"«{topic}»: A/AAAA آدرس، MX ایمیل، CNAME مستعار، TXT متن، NS/SOA برای zone."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## جدول رکورد
| نوع | معنی |
|-----|------|
| A | IPv4 |
| AAAA | IPv6 |
| CNAME | alias |
| MX | ایمیل + اولویت |
| TXT | SPF و متن |
| NS/SOA | سرور و شروع zone |
| PTR | IP به نام |
| SRV | سرویس |

## فریم query نوع A
سؤال نام → جواب IP + TTL → اتصال جدا روی TCP/TLS
"""
    commands = """```
dig example.com A +short
```
```
dig example.com MX
```
```
dig example.com NS
```
```
nslookup -type=MX example.com
```
"""
    lab = """# Lab رکورد
برای یک دامنه A، AAAA، MX، NS را بگیر. اگر فقط CNAME بود قدم بعدی چیست؟
"""
    return summary, full, commands, lab

def _enterprise(topic, level):
    summary = f"«{topic}»: Split-Horizon دو نمای داخلی/خارجی؛ forwarder و DNS+AD ستون سازمان."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## Split-Horizon
داخل: IP خصوصی سرور | بیرون: IP لبه/CDN

## Forwarder / Conditional
سؤالات ناشناس به بالادست؛ دامنه خاص به سرور مشخص

## AD و DNS
SRV برای DC؛ خراب شدن DNS → لاگین و GPO آسیب

## Primary/Secondary
Transfer فقط به secondary مجاز؛ باز روی اینترنت ممنوع
"""
    commands = """```
ipconfig /all
```
```
nslookup intranet.company.local
```
```
Get-DnsServerForwarder
```
"""
    lab = """# Lab سازمانی
DNS کلاینت تو چیست؟ برای mail.company.com دو جواب داخل/خارج فرضی بنویس.
"""
    return summary, full, commands, lab

def _security(topic, level):
    summary = f"«{topic}»: DNSSEC اصالت رکورد؛ DoT/DoH رمز مسیر؛ بستن open resolver و AXFR."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## تهدید
Cache poison | Spoof | Zone transfer باز | Phishing DNS

## DNSSEC
امضای رکورد برای اصالت — نه رمز کامل ترافیک

## DoT / DoH
رمز کردن query تا resolver

## اقدامات
بستن recursion خارجی | محدود AXFR | مانیتور تغییر رکورد حساس
"""
    commands = """```
dig example.com +dnssec
```
"""
    lab = """# Lab امنیت DNS
سه کنترل سخت‌سازی DNS داخلی بنویس. فرق DNSSEC و DoH یک جمله.
"""
    return summary, full, commands, lab

_BUILDERS = {"basics": _basics, "records": _records, "enterprise": _enterprise, "security": _security}

def build_chapter10_lesson(title_fa: str, title_en: str = "") -> Dict[str, Any] | None:
    topic, level = _topic(title_fa), _level(title_fa)
    b = _bucket(topic)
    summary, full, commands, lab = _BUILDERS[b](topic, level)
    return {
        "summary": summary, "full_content": full, "commands": commands,
        "examples": lab, "notes": f"فصل۱۰ · {b} · {level}", "lab": lab,
        "level": level, "topic": topic, "category": b, "chapter": 10,
    }
