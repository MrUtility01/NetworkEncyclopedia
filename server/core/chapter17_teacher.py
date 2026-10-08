# -*- coding: utf-8 -*-
"""فصل ۱۷ — EVPN · VXLAN · Leaf-Spine فوق‌عمیق"""
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
    if any(k in t for k in ("leaf", "spine", "underlay", "anycast", "gateway", "ecmp", "fabric")):
        return "fabric"
    if any(k in t for k in ("evpn", "control plane", "route type", "rt-2", "rt-3", "rt-5", "type 2", "type 3", "type 5", "mac-ip", "imet")):
        return "evpn"
    if any(k in t for k in ("vxlan", "overlay", "vni", "vtep", "4789", "encapsulation")):
        return "vxlan"
    return "vxlan"

def _depth_line(level: str) -> str:
    return {"L0": "تصویر ذهنی", "L1": "فریم‌به‌فریم+Lab", "L2": "پیکربندی+Verify", "L3": "RCA و multi-tenant", "L4": "مقیاس DC"}.get(level, "")

def _vxlan(topic, level):
    summary = f"«{topic}»: VXLAN overlay L2 روی underlay L3؛ VNI ۲۴بیتی و VTEP با UDP 4789."
    full = f"""# {topic}

**سطح:** {level} — {_depth_line(level)}

## چرا VXLAN؟
VLAN ~4094 سگمنت؛ VXLAN با VNI ۲۴بیتی ~۱۶M سگمنت برای DC چندمستأجره.

## تشبیه
Underlay=مترو IP؛ VNI=خطوط منطقی مسافر L2.

## واژگان
| واژه | معنی |
|------|------|
| Underlay | شبکه IP واقعی ECMP |
| Overlay | VXLAN منطقی |
| VTEP | ورود/خروج تونل |
| VNI | شناسه سگمنت ۲۴بیت |

## فریم‌به‌فریم Unicast
1. VM فریم می‌فرستد 2. Leaf MAC→VTEP 3. VXLAN+UDP4789+IP 4. Spine فقط underlay 5. Leaf مقصد decap

## MTU
سربار ~50 بایت؛ underlay باید بزرگ‌تر باشد و end-to-end تست شود.

## Multi-tenant
VLAN محلی یکسان می‌تواند VNI متفاوت داشته باشد — قاطی ممنوع.

## شکست‌های رایج
VTEP unreachable | VNI map غلط | MTU | EVPN down | Anycast ناهماهنگ

## امنیت
ایزولیشن با VNI+policy؛ مدیریت جدا؛ مانیتور decap error

## چک‌لیست
- [ ] ping VTEP-to-VTEP  - [ ] MTU  - [ ] map مستند  - [ ] EVPN verify  - [ ] leaf/spine fail drill

## جمع‌بندی
اول underlay سالم، بعد VNI، بعد EVPN. Overlay روی underlay بیمار نمی‌رقصد.
"""
    commands = """```
show nve peers
```
```
show nve vni
```
```
show nve interface
```
```
show mac address-table
```
```
show l2route mac all
```
```
ping <vtep-ip>
```
```
show ip route <vtep-ip>
```
```
vlan 10
  vn-segment 10010
```
```
interface nve1
  source-interface loopback1
  member vni 10010
```
```
tcpdump -ni any udp port 4789 -c 20
```
```
ip -d link show type vxlan
```
```
show logging | include NVE|VXLAN|BGP
```
"""
    lab = """# Lab VXLAN
1) واژگان روی کاغذ 2) ping VTEP قبل overlay 3) show nve peers 4) VLAN→VNI map 5) capture 4789 6) تست MTU 7) قطع ECMP 8) map غلط+rollback 9) جدول Leaf|VTEP|VNI 10) توضیح ۹۰ثانیه‌ای
"""
    return summary, full, commands, lab

def _evpn(topic, level):
    summary = f"«{topic}»: EVPN کنترل‌پلین BGP برای MAC/IP؛ RT-2/3/5 هسته عملیاتی."
    full = f"""# {topic}

**سطح:** {level} — {_depth_line(level)}

## چرا EVPN؟
VXLAN کپسوله‌می‌کند؛ EVPN می‌گوید هر MAC کجاست بدون flood کور.

## تشبیه
VXLAN=تونل؛ EVPN=دفترچه تلفن VTEP.

## Route Types
| Type | محتوا | کاربرد |
|------|-------|--------|
| RT-2 | MAC/IP | میزبان و mobility |
| RT-3 | IMET | BUM عضویت VNI |
| RT-5 | IP Prefix | L3 overlay |

## فریم RT-2
Learn محلی → Advertise Type-2 → Import RT در leaf دور → encapsulate بدون flood

## RD vs RT
RD تمایز کنترل‌پلین؛ RT سیاست import/export tenant/VNI

## Anycast GW
چند leaf یک GW IP/MAC؛ EVPN همگرایی host/MAC-IP را نگه می‌دارد

## RCA سریع
MAC نیست→Type-2/RT | BUM بد→Type-3 | L3 نیست→Type-5 | tenant قاطی→RT اشتباه

## امنیت
RT سخت‌گیرانه؛ BGP auth؛ مانیتور جهش route count

## جمع‌بندی
RT-2 محل MAC؛ RT-3 عضو BUM؛ RT-5 پیشوند L3. قاطی نکن.
"""
    commands = """```
show bgp l2vpn evpn summary
```
```
show bgp l2vpn evpn
```
```
show bgp l2vpn evpn route-type 2
```
```
show bgp l2vpn evpn route-type 3
```
```
show bgp l2vpn evpn route-type 5
```
```
show nve peers
```
```
show l2route mac all
```
```
show mac address-table dynamic
```
```
show ip route vrf TENANT-A
```
```
router bgp 65000
  address-family l2vpn evpn
    neighbor 10.0.0.100 activate
```
```
show logging | include BGP|EVPN|NVE
```
"""
    lab = """# Lab EVPN
1) summary Established 2) Type-2 برای host جدید 3) قطع BGP در lab 4) Type-3 و BUM 5) RT غلط+rollback 6) mobility و همگرایی 7) جدول Typeها 8) توضیح ۹۰ثانیه
"""
    return summary, full, commands, lab

def _fabric(topic, level):
    summary = f"«{topic}»: Leaf-Spine underlay ECMP؛ Anycast GW در leaf برای first-hop محلی."
    full = f"""# {topic}

**سطح:** {level} — {_depth_line(level)}

## چرا Leaf-Spine؟
STP بلاک و L2 پهن جای خود را به L3 ECMP و overlay می‌دهد.

## نقش‌ها
Leaf=دسترسی+VTEP+GW | Spine=ECMP fabric | Border=خروج DC

## Underlay
L3 تا spine، loopback VTEP reachable، MTU یکنواخت، failure domain=برگ

## Anycast GW
یک IP/MAC GW روی چند leaf؛ ARP محلی؛ بدون flap اگر هماهنگ باشد

## Failure
لینک/spine واحد نباید کل east-west را بکشد؛ leaf down فقط میزبان همان leaf

## Anti-pattern
L2 بین leafها برای راحتی | MTU فراموشی | RR تکی | VNI بدون سند

## جمع‌بندی
اول ECMP و loopback، بعد VXLAN، بعد EVPN، بعد Anycast.
"""
    commands = """```
show ip route
```
```
show ip ospf neighbor
```
```
show bgp summary
```
```
show ip route <vtep-loopback>
```
```
show nve peers
```
```
show nve vni
```
```
ping <leaf-loopback>
```
```
traceroute <leaf-loopback>
```
```
show logging | include LINK|BGP|NVE
```
"""
    lab = """# Lab Fabric
1) نقشه leaf-spine 2) ECMP به loopback 3) قطع spine 4) Anycast ARP 5) leaf down 6) سند Loopback/VNI 7) مقایسه با L2 پهن 8) ارائه ۲دقیقه‌ای برای مدیر
"""
    return summary, full, commands, lab

_BUILDERS = {"vxlan": _vxlan, "evpn": _evpn, "fabric": _fabric}

def build_chapter17_lesson(title_fa: str, title_en: str = "") -> Dict[str, Any] | None:
    topic, level = _topic(title_fa), _level(title_fa)
    b = _bucket(topic)
    summary, full, commands, lab = _BUILDERS[b](topic, level)
    if level in ("L3", "L4"):
        full += f"\n\n## پیوست {level}\nRCA یک‌طرفه بودن east-west: underlay→nve peers→Type-2→VNI member→ACL→MTU. فقط با evidence تغییر بده.\n"
        lab += f"\n## Lab {level}\nRunbook یک‌صفحه برای قطع VNI X با ترتیب دستور production.\n"
    return {
        "summary": summary, "full_content": full, "commands": commands,
        "examples": lab, "notes": f"فصل۱۷ · {b} · {level}", "lab": lab,
        "level": level, "topic": topic, "category": b, "chapter": 17,
    }
