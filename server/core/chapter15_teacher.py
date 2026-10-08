# -*- coding: utf-8 -*-
"""فصل ۱۵ — VRF · MPLS · L3VPN"""
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
    if any(k in t for k in ("l3vpn", "pe p ce", "vpnv4", "route target", "route distinguisher", "rd ", "rt ")):
        return "l3vpn"
    if any(k in t for k in ("mpls", "label", "ldp", "lsp", "label switching", "push", "swap", "pop", "php")):
        return "mpls"
    if any(k in t for k in ("vrf", "vrf مفهوم", "routing instance")):
        return "vrf"
    return "vrf"

def _depth(level: str) -> str:
    return {"L0": "تصویر ذهنی", "L1": "فریم‌به‌فریم+Lab", "L2": "دستور IOS", "L3": "طراحی PE-CE", "L4": "مقیاس"}.get(level, "")

def _vrf(topic, level):
    summary = f"«{topic}»: VRF چند جدول مسیر جدا روی یک روتر — چند مستأجر بدون قاطی شدن."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## تشبیه
چند دفترچه مسیر جدا در یک ساختمان روتر.

## چرا
جداسازی مشتری | آدرس همپوشان | پایه L3VPN

## فریم
پکت از اینترفیس VRF-A → lookup فقط جدول A → خروج مجاز همان VRF

## عیب‌یابی
پینگ ناخواسته بین مشتری = VRF/اینترفیس اشتباه
"""
    commands = """```
show vrf
```
```
show ip route vrf CUST-A
```
```
interface Gi0/1
 vrf forwarding CUST-A
 ip address 10.1.1.1 255.255.255.0
```
"""
    lab = """# Lab VRF
show vrf | دو مشتری با 10.0.0.0/24 بدون و با VRF چه فرقی دارد؟
"""
    return summary, full, commands, lab

def _mpls(topic, level):
    summary = f"«{topic}»: MPLS با برچسب Push/Swap/Pop سوییچ می‌کند؛ هسته لزوماً full IP lookup نمی‌کند."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## عمل‌ها
Push چسباندن | Swap عوض کردن | Pop برداشتن | PHP یک‌قدم زودتر

## LSP / LDP
مسیر برچسب‌گذاری‌شده | توزیع برچسب در هسته

## فریم هسته
PE ورودی برچسب می‌زند → P فقط transport را swap → PE خروجی به CE
"""
    commands = """```
show mpls ldp neighbor
```
```
show mpls forwarding-table
```
```
interface Gi0/0
 mpls ip
```
"""
    lab = """# Lab MPLS
LDP neighbor؟ فرق Push و Swap با تشبیه چمدان.
"""
    return summary, full, commands, lab

def _l3vpn(topic, level):
    summary = f"«{topic}»: CE مشتری، PE لبه با VRF، P هسته؛ RD متمایز می‌کند و RT مسیر را share می‌کند."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## نقش‌ها
CE | PE (VRF+MPLS) | P (حمل برچسب)

## RD / RT
RD تمایز کنترل‌پلن | RT import/export کدام VRF مسیر را بگیرد

## فریم مشتری
CE→PE lookup VRF → برچسب VPN+حمل → Pها swap → PE مقابل → CE

## عیب‌یابی
سایت به سایت نه → RT، PE-CE، LDP بین PE
"""
    commands = """```
show ip route vrf CUST-A
```
```
show bgp vpnv4 unicast all summary
```
```
show mpls forwarding-table
```
"""
    lab = """# Lab L3VPN
دو سایت یک RD/RT مشترک طراحی کن. روی طرح CE/PE/P را علامت بزن.
"""
    return summary, full, commands, lab

_BUILDERS = {"vrf": _vrf, "mpls": _mpls, "l3vpn": _l3vpn}

def build_chapter15_lesson(title_fa: str, title_en: str = "") -> Dict[str, Any] | None:
    topic, level = _topic(title_fa), _level(title_fa)
    b = _bucket(topic)
    summary, full, commands, lab = _BUILDERS[b](topic, level)
    return {
        "summary": summary, "full_content": full, "commands": commands,
        "examples": lab, "notes": f"فصل۱۵ · {b} · {level}", "lab": lab,
        "level": level, "topic": topic, "category": b, "chapter": 15,
    }
