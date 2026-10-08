# -*- coding: utf-8 -*-
"""فصل ۱۴ — مسیریابی: Static · OSPF · EIGRP · BGP · Policy"""
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
    if any(k in t for k in ("prefix-list", "route-map", "policy", "distribute", "filter", "redistribut")):
        return "policy"
    if any(k in t for k in ("bgp", "as number", "as path", "ibgp", "ebgp", "community")):
        return "bgp"
    if any(k in t for k in ("eigrp", "metric مرکب", "feasible", "successor")):
        return "eigrp"
    if any(k in t for k in ("ospf", "link-state", "lsa", "area", "dr", "bdr", "adjacency", "spf")):
        return "ospf"
    if any(k in t for k in ("static", "default route", "floating", "administrative distance", "next-hop", "null0")):
        return "static"
    return "static"

def _depth(level: str) -> str:
    return {"L0": "تصویر ذهنی", "L1": "فریم‌به‌فریم+Lab", "L2": "دستور IOS", "L3": "طراحی", "L4": "Policy"}.get(level, "")

def _static(topic, level):
    summary = f"«{topic}»: مسیر دستی؛ ساده و قابل‌پیش‌بینی برای لبه و default به‌سمت ISP."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## دستور مفهومی
ip route شبکه ماسک next-hop | default 0.0.0.0 | floating با AD بالاتر

## فریم
جدول → next-hop reachable → ارسال و TTL--

## عیب‌یابی
route نیست → تایپ | هست forward نه → next-hop/اینترفیس
"""
    commands = """```
show ip route
```
```
ip route 0.0.0.0 0.0.0.0 203.0.113.1
```
```
ip route 10.20.0.0 255.255.0.0 192.0.2.1 200
```
"""
    lab = """# Lab Static
show ip route static | default بنویس و traceroute بگیر | floating یعنی چه؟
"""
    return summary, full, commands, lab

def _ospf(topic, level):
    summary = f"«{topic}»: OSPF link-state؛ LSA + SPF؛ Area 0 ستون فقرات."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## مفاهیم
Neighbor/Adjacency | LSA | Area | DR/BDR | Cost

## فریم همگرایی
Hello → تبادل DB → Full → SPF → جدول

## عیب‌یابی
Neighbor نه → subnet/area/hello | مسیر نه → advertise
"""
    commands = """```
show ip ospf neighbor
```
```
show ip route ospf
```
```
router ospf 1
 network 10.10.0.0 0.0.255.255 area 0
```
"""
    lab = """# Lab OSPF
State FULL؟ مسیرهای O را ببین. دو area بدون 0 چه اشکالی دارد؟
"""
    return summary, full, commands, lab

def _eigrp(topic, level):
    summary = f"«{topic}»: EIGRP متریک مرکب و Successor/FS برای failover سریع."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## Successor vs FS
بهترین مسیر در برابر پشتیبان واجد شرایط

## کجا
محیط‌های سیسکو موجود؛ سبزfield اغلب OSPF
"""
    commands = """```
show ip eigrp neighbors
```
```
show ip eigrp topology
```
```
router eigrp 100
 network 10.0.0.0
```
"""
    lab = """# Lab EIGRP
Neighbor و FS را پیدا کن. فرق Successor و FS یک جمله.
"""
    return summary, full, commands, lab

def _bgp(topic, level):
    summary = f"«{topic}»: BGP بین ASها؛ eBGP اینترنت، سیاست مهم‌تر از کوتاه‌ترین مسیر خام."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## eBGP / iBGP
بین AS در برابر داخل AS

## فریم peer
TCP 179 → OPEN → UPDATE → جدول BGP

## عیب‌یابی
Idle → ACL/AS/IP | Established بدون مسیر → فیلتر/next-hop
"""
    commands = """```
show ip bgp summary
```
```
show ip bgp
```
```
router bgp 65001
 neighbor 203.0.113.1 remote-as 65002
```
"""
    lab = """# Lab BGP
show ip bgp summary: Established؟ چرا AS-Path بلندتر اغلب بدتر است؟
"""
    return summary, full, commands, lab

def _policy(topic, level):
    summary = f"«{topic}»: prefix-list و route-map برای فیلتر و set کردن صفت مسیر."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## ابزار
prefix-list = چه پیشوندی | route-map = اگر match آنگاه set

## Redistribution
بدون فیلتر = حلقه و سیاه‌چاله؛ tag و طراحی لازم است
"""
    commands = """```
ip prefix-list ALLOW-10 seq 10 permit 10.0.0.0/8 le 24
```
```
route-map SET-PREF permit 10
 match ip address prefix-list ALLOW-10
 set local-preference 200
```
"""
    lab = """# Lab Policy
فقط 10.10.0.0/16 را permit کن. چرا redistribute دوطرفه خطرناک است؟
"""
    return summary, full, commands, lab

_BUILDERS = {"static": _static, "ospf": _ospf, "eigrp": _eigrp, "bgp": _bgp, "policy": _policy}

def build_chapter14_lesson(title_fa: str, title_en: str = "") -> Dict[str, Any] | None:
    topic, level = _topic(title_fa), _level(title_fa)
    b = _bucket(topic)
    summary, full, commands, lab = _BUILDERS[b](topic, level)
    return {
        "summary": summary, "full_content": full, "commands": commands,
        "examples": lab, "notes": f"فصل۱۴ · {b} · {level}", "lab": lab,
        "level": level, "topic": topic, "category": b, "chapter": 14,
    }
