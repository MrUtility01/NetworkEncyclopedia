# -*- coding: utf-8 -*-
"""فصل‌های ۱۸–۲۵ — SDN/SD-WAN · MikroTik · Wireless · FortiGate · pfSense فوق‌عمیق"""
from __future__ import annotations
import re
from typing import Any, Dict, Optional

def _level(title: str) -> str:
    m = re.match(r"\[(L[0-4])\]", title or "")
    return m.group(1) if m else "L0"

def _topic(title: str) -> str:
    t = re.sub(r"^\[L[0-4]\]\s*", "", title or "")
    t = re.sub(r"\s*[—\-]\s*(آشنایی|مقدماتی|ادمین|مهندس|خبره|Intro|Junior|Admin|Senior|Architect).*$", "", t, flags=re.I)
    return t.strip() or (title or "موضوع")

def _depth(level: str) -> str:
    return {"L0": "تصویر ذهنی + واژگان", "L1": "Lab پایه + Verify", "L2": "پیکربندی عملی + Troubleshooting",
            "L3": "طراحی + HA + RCA", "L4": "معماری سازمانی + Scale"}.get(level, "عملی")

def _detect(topic: str, title: str) -> str:
    t = (topic + " " + title).lower()
    if any(k in t for k in ("fortigate", "fortinet", "fortios", "fg-", "utm", "ssl inspection", "web filter")):
        return "forti"
    if any(k in t for k in ("pfsense", "opnsense", "sophos", "netgate", "suricata", "carp", "multi-wan")):
        return "pfsense"
    if any(k in t for k in ("sdn", "sd-wan", "sase", "vmanage", "viptela", "intent-based")):
        return "sdn"
    if any(k in t for k in ("mikrotik", "routeros", "winbox", "ros ", "chr", "rb5", "rb4", "rb7", "hap ", "ccr", "crs")):
        if any(k in t for k in ("qos", "queue", "mangle", "pcq", "htb", "priority", "vpn", "ipsec", "l2tp", "sstp", "ovpn", "wireguard", "ha", "vrrp", "bonding")):
            return "mt_adv"
        if any(k in t for k in ("route", "ospf", "bgp", "firewall", "filter", "nat", "src-nat", "dst-nat", "masquerade", "address-list")):
            return "mt_route"
        return "mt_base"
    if any(k in t for k in ("wireless", "wifi", "وایرلس", "ssid", "wpa", "802.11", "ap ", "capwap", "roaming", "band", "channel", "rf ")) or "بی‌سیم" in t or "بی سیم" in t:
        return "wifi"
    if any(k in t for k in ("ptp", "ptmp", "point-to-point", "point to point", "airmax", "ubiquiti", "nv2", "nstream")):
        return "ptp"
    return "generic"

def _pack(summary, full, commands, examples, notes, level, topic, cat) -> Dict[str, Any]:
    return {"summary": summary, "full_content": full, "commands": commands, "examples": examples, "notes": notes, "level": level, "topic": topic, "category": cat}

def _sdn(topic: str, level: str) -> Dict[str, Any]:
    summary = f"«{topic}»: جداسازی Control Plane از Data Plane؛ کنترلر مرکزی intent را به underlay/overlay تبدیل می‌کند."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## چرا SDN / SD-WAN / SASE؟
شبکه‌های سنتی box-by-box پیچیده و کند تغییر می‌کنند. SDN کنترل را متمرکز می‌کند؛ SD-WAN ترافیک را روی چند WAN هوشمند هدایت می‌کند؛ SASE امنیت cloud-delivered را با شبکه ترکیب می‌کند.

## واژگان کلیدی
| واژه | معنی |
|------|------|
| Control Plane | تصمیم‌گیری مسیر/سیاست |
| Data Plane | ارسال واقعی پکت |
| Underlay | شبکه فیزیکی/IP واقعی |
| Overlay | تونل‌های منطقی |
| Intent | «چه می‌خواهم» |
| SASE | Secure Access Service Edge |

## معماری ساده SD-WAN
1. Edge در شعب 2. Controller 3. Underlay (Internet/MPLS/LTE) 4. Overlay IPsec 5. Policy بر اساس SLA

## شکست‌های رایج
Control down | Certificate | SLA flapping | MTU/NAT

## چک‌لیست
- [ ] Control سبز - [ ] Overlay up - [ ] Policy - [ ] Failover تست
"""
    commands = """```
show control connections
show bfd sessions
show app-route stats
show omp peers
```"""
    examples = f"## Lab — {topic}\nدو edge + کنترلر؛ دو underlay؛ policy؛ قطع لینک و failover."
    notes = "اول underlay و identity، بعد overlay، بعد policy."
    return _pack(summary, full, commands, examples, notes, level, topic, "sdn")

def _mt_base(topic: str, level: str) -> Dict[str, Any]:
    summary = f"«{topic}»: مبانی RouterOS — منوها، interface، bridge، identity و امنیت پایه."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## RouterOS
سیستم‌عامل MikroTik. Winbox / WebFig / CLI / API.

## منوهای کلیدی
Interfaces | Bridge | IP Addresses | Routes | Firewall | System Identity

## اصول طلایی
1. Identity و password قوی 2. بستن telnet/ftp 3. Winbox فقط LAN/VPN 4. /export قبل از تغییر 5. Safe Mode
"""
    commands = """```
/system identity set name=Branch-R1
/system identity print
```
```
/interface print
/ip address print
/ip route print
```
```
/ip service print
/ip service disable telnet,ftp
```
```
/user print
/export file=backup-before-change
```
```
/ping 8.8.8.8 count=5
/ip arp print
```"""
    examples = f"## Lab — {topic}\nCHR؛ WAN+LAN؛ bridge؛ IP روی bridge؛ export."
    notes = "همیشه Safe Mode و export قبل از تغییرات خطرناک."
    return _pack(summary, full, commands, examples, notes, level, topic, "mikrotik")

def _mt_route(topic: str, level: str) -> Dict[str, Any]:
    summary = f"«{topic}»: مسیریابی و فایروال RouterOS — route، filter/nat و address-list."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## فایروال
filter input/forward/output | nat srcnat/dstnat | mangle | raw

## ترتیب طلایی Filter
1. Accept established/related 2. Drop invalid 3. Accept management از LAN 4. Drop بقیه

## Address-list
بهترین ابزار گروه‌بندی IP.
"""
    commands = """```
/ip firewall filter add chain=input connection-state=established,related action=accept
/ip firewall filter add chain=input connection-state=invalid action=drop
/ip firewall filter add chain=input in-interface-list=WAN protocol=tcp dst-port=22,8291 action=accept comment=mgmt
/ip firewall filter add chain=input in-interface-list=WAN action=drop
```
```
/ip firewall filter add chain=forward connection-state=established,related action=accept
/ip firewall filter add chain=forward connection-state=invalid action=drop
/ip firewall filter add chain=forward in-interface-list=LAN out-interface-list=WAN action=accept
```
```
/ip firewall nat add chain=srcnat out-interface-list=WAN action=masquerade
/ip firewall nat print
/ip firewall filter print stats
```
```
/ip route print
/ip dns set servers=1.1.1.1,8.8.8.8 allow-remote-requests=yes
```"""
    examples = f"## Lab — {topic}\nدو روتر؛ masquerade؛ filter فقط established + management."
    notes = "Counters بهترین دوست troubleshooting هستند."
    return _pack(summary, full, commands, examples, notes, level, topic, "mikrotik")

def _mt_adv(topic: str, level: str) -> Dict[str, Any]:
    summary = f"«{topic}»: QoS، VPN و HA در MikroTik — queue tree، WireGuard، VRRP."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## QoS
اول mark (mangle) بعد queue. FastTrack را برای marked غیرفعال نگه دار.

## VPN
WireGuard (ترجیح) | IPsec IKEv2 | L2TP/IPsec

## HA
VRRP | Netwatch + script | recursive routing برای dual-ISP
"""
    commands = """```
/interface wireguard add listen-port=13231 name=wg-office
/interface wireguard peers add interface=wg-office public-key="PEER_KEY" endpoint-address=1.2.3.4 endpoint-port=13231 allowed-address=10.20.0.0/24
/ip address add address=10.10.10.1/24 interface=wg-office
```
```
/ip firewall mangle add chain=prerouting src-address=10.10.10.0/24 action=mark-connection new-connection-mark=vip
/queue tree add name=vip parent=global packet-mark=vip max-limit=20M
```
```
/interface vrrp add interface=ether2 vrid=10 priority=200
/ip address add address=10.10.10.254/24 interface=vrrp1
```
```
/ip ipsec identity print
/ip ipsec active-peers print
/log print where topics~"ipsec"
```"""
    examples = f"## Lab — {topic}\nMark VIP؛ Queue Tree؛ WireGuard site-to-site؛ VRRP."
    notes = "QoS بدون اندازه‌گیری حدس است."
    return _pack(summary, full, commands, examples, notes, level, topic, "mikrotik")

def _wifi(topic: str, level: str) -> Dict[str, Any]:
    summary = f"«{topic}»: وایرلس سازمانی — SSID، کنترلر، Roaming، RF و WPA3/802.1X."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## معماری
Autonomous AP | Controller (CAPWAP) | Cloud-managed

## RF و امنیت
Channel plan | Power کمتر اغلب بهتر | WPA3-Enterprise + 802.1X | Guest isolation
"""
    commands = """```
/interface wireless registration-table print
/interface wireless scan 0
/interface wireless monitor 0
```"""
    examples = f"## Lab — {topic}\nدو AP؛ SSID سازمانی + Guest؛ تست roaming."
    notes = "بدون site survey طراحی وایرلس حدس است."
    return _pack(summary, full, commands, examples, notes, level, topic, "wireless")

def _ptp(topic: str, level: str) -> Dict[str, Any]:
    summary = f"«{topic}»: لینک PtP/PtMP — Fresnel، alignment، capacity."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## PtP vs PtMP
PtP حداکثر ظرفیت. PtMP یک Base به چند Station.

## عوامل
فاصله | فرکانس | Gain | Fresnel حداقل ۶۰٪ | LOS واقعی
"""
    commands = """```
/tool bandwidth-test address=x.x.x.x direction=both
iperf3 -c <peer> -t 30 -P 4
```"""
    examples = f"## Lab — {topic}\nدو رادیو؛ alignment؛ bandwidth test دو طرفه."
    notes = "لینک بدون مانیتورینگ مداوم خطرناک است."
    return _pack(summary, full, commands, examples, notes, level, topic, "wireless")

def _forti(topic: str, level: str) -> Dict[str, Any]:
    summary = f"«{topic}»: FortiGate — policy، UTM، SD-WAN و diagnose debug flow."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## فلسفه
Object تمیز + Policy top-down. UTM: AV, Web Filter, IPS, App Control.

## SD-WAN
Member + Performance SLA + Rule

## شکست‌های رایج
Policy order | SSL inspection بدون cert | Asymmetric routing
"""
    commands = """```
get system status
get system interface physical
execute ping 8.8.8.8
```
```
show firewall policy
show firewall vip
show firewall ippool
get router info routing-table all
```
```
diagnose sys session filter src 10.10.10.50
diagnose sys session list
diagnose firewall iprope lookup 10.10.10.50 8.8.8.8 1 443
```
```
diagnose debug flow filter saddr 10.10.10.50
diagnose debug flow show console enable
diagnose debug enable
diagnose debug flow trace start 20
# diagnose debug disable
```
```
execute log filter category 0
execute log display
```"""
    examples = f"## Lab — {topic}\nLAN/WAN؛ policy با NAT + Web Filter؛ debug flow."
    notes = "بدون debug flow troubleshooting حدس است."
    return _pack(summary, full, commands, examples, notes, level, topic, "fortigate")

def _pfsense(topic: str, level: str) -> Dict[str, Any]:
    summary = f"«{topic}»: pfSense / OPNsense / Sophos — multi-WAN، package و HA."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## خانواده
pfSense | OPNsense | Sophos

## مفاهیم
Alias | Gateway Group | CARP/HA | Packages (Suricata, HAProxy, WireGuard)
"""
    commands = """```
pfctl -sr | head
netstat -rn
tcpdump -ni em0 host x.x.x.x
```"""
    examples = f"## Lab — {topic}\nدو WAN؛ Gateway Group failover؛ Rule با Alias."
    notes = "اگر rule hit نمی‌خورد، rule بالاتر یا state قدیمی را چک کن."
    return _pack(summary, full, commands, examples, notes, level, topic, "pfsense")

def _generic(topic: str, level: str) -> Dict[str, Any]:
    summary = f"«{topic}»: مفهوم کلیدی فصل‌های ۱۸–۲۵."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

موضوع در محدوده SDN / MikroTik / Wireless / FortiGate / pfSense.
"""
    commands = "```\n# ابزار بومی همان پلتفرم\n```"
    examples = f"Lab مرتبط با «{topic}» را انجام بده."
    notes = "تمرکز روی یک پلتفرم بهتر از پراکندگی است."
    return _pack(summary, full, commands, examples, notes, level, topic, "generic")

def build_chapter18_25_lesson(title_fa: str, title_en: str = "") -> Optional[Dict[str, Any]]:
    level = _level(title_fa)
    topic = _topic(title_fa)
    kind = _detect(topic, title_fa or "")
    builders = {"sdn": _sdn, "mt_base": _mt_base, "mt_route": _mt_route, "mt_adv": _mt_adv,
                "wifi": _wifi, "ptp": _ptp, "forti": _forti, "pfsense": _pfsense, "generic": _generic}
    return builders.get(kind, _generic)(topic, level)
