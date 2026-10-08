# -*- coding: utf-8 -*-
"""فصل ۱۳ — سوییچینگ سیسکو: VLAN · STP · EtherChannel · L2 Security · 802.1X"""
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
    if any(k in t for k in ("802.1x", "eap", "radius", "mab", "dot1x")):
        return "dot1x"
    if any(k in t for k in ("port security", "dhcp snooping", "dai", "storm control", "bpdu guard", "root guard", "امنیت")):
        return "l2sec"
    if any(k in t for k in ("etherchannel", "lacp", "pagp", "port-channel", "lag")):
        return "etherchannel"
    if any(k in t for k in ("stp", "rstp", "mst", "loop", "root bridge", "bpdu", "spanning", "مشکل loop")):
        return "stp"
    if any(k in t for k in ("vlan", "trunk", "access", "802.1q", "native", "svi", "مفهوم vlan")):
        return "vlan"
    return "vlan"

def _depth(level: str) -> str:
    return {"L0": "تصویر ذهنی", "L1": "فریم‌به‌فریم+Lab", "L2": "دستور IOS", "L3": "طراحی", "L4": "سازمانی"}.get(level, "")

def _vlan(topic, level):
    summary = f"«{topic}»: VLAN شبکه منطقی روی سوییچ است؛ بین VLANها بدون L3 راه نیست."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## تشبیه
طبقات جدا در یک ساختمان سوییچ.

## Access / Trunk
Access = یک VLAN | Trunk = چند VLAN با تگ 802.1Q | Native بدون تگ

## فریم روی Trunk
Access VLAN10 → تگ روی trunk → سوییچ مقابل به access همان VLAN

## SVI
interface Vlan10 برای gateway لایه ۳ همان VLAN

## عیب‌یابی
پینگ داخل VLAN نه → access/VLAN | بین سوییچ نه → trunk/allowed | بین VLAN نه → L3
"""
    commands = """```
show vlan brief
```
```
show interfaces trunk
```
```
interface Gi0/1
 switchport mode access
 switchport access vlan 10
```
```
interface Gi0/24
 switchport mode trunk
```
```
interface Vlan10
 ip address 10.10.10.1 255.255.255.0
```
"""
    lab = """# Lab VLAN
show vlan brief | دو پورت access یک VLAN پینگ | VLAN جدا بدون L3 نباید برسد.
"""
    return summary, full, commands, lab

def _stp(topic, level):
    summary = f"«{topic}»: STP جلوی loop لایه ۲ را می‌گیرد؛ یک مسیر Forward بقیه Block."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## مشکل Loop
Broadcast می‌چرخد و شبکه می‌میرد.

## ایده
Root Bridge → پورت Root → پورت‌های اضافی Blocking | RSTP سریع‌تر

## BPDU Guard
روی access کاربر؛ BPDU غیرمنتظره → err-disable

## عیب‌یابی
blocking طبیعی است | root ناپایدار = اولویت/لینک
"""
    commands = """```
show spanning-tree
```
```
show spanning-tree vlan 10
```
```
spanning-tree mode rapid-pvst
```
```
interface Gi0/1
 spanning-tree portfast
 spanning-tree bpduguard enable
```
"""
    lab = """# Lab STP
Root کیست؟ کدام پورت Blocked؟ PortFast فقط روی کاربر نه uplink.
"""
    return summary, full, commands, lab

def _etherchannel(topic, level):
    summary = f"«{topic}»: EtherChannel چند لینک را یک Port-Channel منطقی می‌کند (LACP)."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## چرا
پهنای بیشتر + افزونگی؛ STP کل باندل را یک پورت می‌بیند.

## شرط
سرعت/duplex/حالت trunk دو طرف یکسان | LACP mode active

## عیب‌یابی
باندل نه → تنظیمات جفت نیست | یک عضو down → کابل همان عضو
"""
    commands = """```
show etherchannel summary
```
```
interface range Gi0/1-2
 channel-group 1 mode active
```
```
interface Port-channel1
 switchport mode trunk
```
"""
    lab = """# Lab EtherChannel
show etherchannel summary: وضعیت P؟ اگر یک لینک قطع شود چه می‌شود؟
"""
    return summary, full, commands, lab

def _l2sec(topic, level):
    summary = f"«{topic}»: Port Security، DHCP Snooping، DAI و BPDU Guard لبه را محکم می‌کنند."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## ابزارها
Port-sec = سقف MAC | DHCP Snooping = فقط trust Offer بدهد | DAI = ARP با binding | BPDU Guard روی access

## خلاصه
لبه را قفل کن؛ هسته را ساده نگه دار.
"""
    commands = """```
switchport port-security
switchport port-security maximum 2
```
```
ip dhcp snooping
ip dhcp snooping vlan 10
```
```
show port-security
```
"""
    lab = """# Lab L2 Security
maximum 1 روی Lab؛ پورت trust DHCP کدام است؟
"""
    return summary, full, commands, lab

def _dot1x(topic, level):
    summary = f"«{topic}»: 802.1X با EAP و RADIUS قبل از دسترسی کامل به LAN احراز می‌کند."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## نقش‌ها
Supplicant (کلاینت) | Authenticator (سوییچ) | RADIUS

## فریم
پورت محدود → EAP → RADIUS → در صورت موفقیت VLAN/سیاست

## MAB
برای دستگاه بدون 802.1X؛ ضعیف‌تر — با احتیاط
"""
    commands = """```
show dot1x all
```
```
show authentication sessions
```
"""
    lab = """# Lab 802.1X
سه نقش را روی طرح دفتر بنویس. show authentication sessions اگر فعال است.
"""
    return summary, full, commands, lab

_BUILDERS = {"vlan": _vlan, "stp": _stp, "etherchannel": _etherchannel, "l2sec": _l2sec, "dot1x": _dot1x}

def build_chapter13_lesson(title_fa: str, title_en: str = "") -> Dict[str, Any] | None:
    topic, level = _topic(title_fa), _level(title_fa)
    b = _bucket(topic)
    summary, full, commands, lab = _BUILDERS[b](topic, level)
    return {
        "summary": summary, "full_content": full, "commands": commands,
        "examples": lab, "notes": f"فصل۱۳ · {b} · {level}", "lab": lab,
        "level": level, "topic": topic, "category": b, "chapter": 13,
    }
