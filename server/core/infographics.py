# -*- coding: utf-8 -*-
"""کتابخانه اینفوگرافیک SVG — مسیر پکت، پروتکل‌ها، سرویس‌ها."""
from __future__ import annotations
from typing import Dict, List, Tuple


def _svg(inner: str, w: int = 720, h: int = 240, title: str = "") -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" '
        f'style="max-width:{w}px;background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;margin:12px 0">'
        f'<defs><marker id="m" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">'
        f'<path d="M0,0 L6,3 L0,6 Z" fill="#64748b"/></marker></defs>'
        f'<text x="16" y="22" font-family="Tahoma,sans-serif" font-size="13" fill="#0f172a" font-weight="bold">{title}</text>'
        f"{inner}</svg>"
    )


def _box(x, y, w, h, label, color="#2563eb"):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{color}" opacity="0.14" stroke="{color}" stroke-width="2"/>'
        f'<text x="{x+w//2}" y="{y+h//2+5}" text-anchor="middle" font-family="Tahoma,sans-serif" font-size="11" fill="#0f172a">{label}</text>'
    )


def _line(x1, y1, x2, y2, lab=""):
    s = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#64748b" stroke-width="2" marker-end="url(#m)"/>'
    if lab:
        s += f'<text x="{(x1+x2)//2}" y="{min(y1,y2)-8}" text-anchor="middle" font-family="Tahoma,sans-serif" font-size="10" fill="#64748b">{lab}</text>'
    return s


def _note(y, text):
    return f'<text x="16" y="{y}" font-family="Tahoma,sans-serif" font-size="11" fill="#475569">{text}</text>'


# ——— هسته مسیر پکت ———

def packet_path_l2_l3() -> str:
    inner = "".join([
        _box(20, 70, 100, 52, "PC", "#0ea5e9"),
        _box(150, 70, 100, 52, "سوئیچ L2", "#8b5cf6"),
        _box(280, 70, 100, 52, "روتر L3", "#2563eb"),
        _box(410, 70, 100, 52, "مودم/FW", "#f59e0b"),
        _box(540, 70, 120, 52, "ISP/اینترنت", "#16a34a"),
        _line(120, 96, 150, 96, "Eth"),
        _line(250, 96, 280, 96, "VLAN"),
        _line(380, 96, 410, 96, "IP/NAT"),
        _line(510, 96, 540, 96, "WAN"),
        _note(160, "① MAC learning  ② Route lookup  ③ NAT/Policy  ④ تحویل به ISP — بازگشت با connection tracking"),
        _note(185, "مثال: PC=10.10.10.50 → GW=10.10.10.1 → Public 203.0.113.10 → 8.8.8.8"),
    ])
    return _svg(inner, 720, 210, "مسیر پکت: کلاینت تا اینترنت")


def packet_path_wireless() -> str:
    inner = "".join([
        _box(20, 65, 110, 52, "موبایل/لپ‌تاپ", "#0ea5e9"),
        _box(160, 65, 100, 52, "AP", "#8b5cf6"),
        _box(290, 65, 100, 52, "سوئیچ", "#6366f1"),
        _box(420, 65, 110, 52, "WLC/روتر", "#2563eb"),
        _box(560, 65, 100, 52, "اینترنت", "#16a34a"),
        _line(130, 91, 160, 91, "802.11"),
        _line(260, 91, 290, 91, "Eth"),
        _line(390, 91, 420, 91, "CAPWAP"),
        _line(530, 91, 560, 91, "WAN"),
        _note(150, "Association → Auth (WPA2/3) → DHCP → Gateway → Internet | Roaming = AP جدید + همان IP"),
        _note(175, "مثال: SSID=Corp → VLAN 20 → SVI 10.20.20.1 → NAT به اینترنت"),
    ])
    return _svg(inner, 720, 200, "مسیر پکت وایرلس سازمانی")


def switch_decision() -> str:
    inner = "".join([
        _box(30, 55, 130, 48, "فریم ورودی", "#0ea5e9"),
        _box(220, 55, 150, 48, "جدول MAC؟", "#f59e0b"),
        _box(450, 30, 150, 40, "Unicast → پورت", "#16a34a"),
        _box(450, 90, 150, 40, "Unknown → Flood", "#dc2626"),
        _line(160, 79, 220, 79),
        _line(370, 70, 450, 50),
        _line(370, 88, 450, 110),
        _note(160, "Learning: Src MAC+Port | Aging | Broadcast در VLAN همیشه Flood"),
        _note(185, "مثال: PC-A در Fa0/1 → سوئیچ MAC جدول را پر می‌کند → به Fa0/5 می‌فرستد"),
    ])
    return _svg(inner, 680, 210, "تصمیم سوئیچ لایه ۲")


def router_decision() -> str:
    inner = "".join([
        _box(20, 55, 110, 48, "پکت IP", "#0ea5e9"),
        _box(170, 55, 130, 48, "Routing Table", "#2563eb"),
        _box(340, 30, 130, 40, "Longest Match", "#16a34a"),
        _box(340, 95, 130, 40, "No route→Drop", "#dc2626"),
        _box(520, 55, 120, 48, "Next-hop/ARP", "#8b5cf6"),
        _line(130, 79, 170, 79),
        _line(300, 70, 340, 50),
        _line(300, 88, 340, 115),
        _line(470, 50, 520, 79),
        _note(165, "TTL-- | ACL/NAT | هدر L2 جدید برای hop بعدی"),
        _note(190, "مثال: dst 8.8.8.8 → match 0.0.0.0/0 via 203.0.113.1 Gig0/0"),
    ])
    return _svg(inner, 700, 215, "تصمیم روتر لایه ۳")


def osi_packet_build() -> str:
    layers = [
        ("Application", "HTTP / DNS / SSH", "#0ea5e9"),
        ("Transport", "TCP/UDP + Port", "#8b5cf6"),
        ("Network", "IP Src/Dst + TTL", "#2563eb"),
        ("Data Link", "MAC + EtherType", "#f59e0b"),
        ("Physical", "بیت روی کابل/رادیو", "#16a34a"),
    ]
    parts, y = [], 40
    for name, desc, color in layers:
        parts.append(_box(80, y, 560, 28, f"{name} — {desc}", color))
        y += 32
    parts.append(_note(y + 10, "ارسال = Encapsulation از بالا به پایین | دریافت = Decapsulation از پایین به بالا"))
    return _svg("".join(parts), 720, 230, "Encapsulation لایه به لایه")


# ——— پروتکل‌ها و سرویس‌ها ———

def tcp_handshake() -> str:
    inner = "".join([
        _box(40, 50, 120, 44, "Client", "#0ea5e9"),
        _box(520, 50, 120, 44, "Server", "#16a34a"),
        _line(160, 60, 520, 60, "1. SYN"),
        _line(520, 85, 160, 85, "2. SYN-ACK"),
        _line(160, 110, 520, 110, "3. ACK"),
        _note(155, "بعد از Handshake: انتقال داده + ACK | پایان: FIN/ACK"),
        _note(180, "مثال: مرورگر → :443 سرور | اگر فقط SYN ببینی = فیلتر یا سرویس مرده"),
    ])
    return _svg(inner, 700, 210, "TCP Three-Way Handshake")


def arp_flow() -> str:
    inner = "".join([
        _box(30, 60, 120, 48, "Host A\n10.0.0.10", "#0ea5e9"),
        _box(280, 60, 140, 48, "سوئیچ (Flood)", "#8b5cf6"),
        _box(520, 60, 130, 48, "Host B\n10.0.0.20", "#16a34a"),
        _line(150, 75, 280, 75, "Who has 10.0.0.20?"),
        _line(420, 95, 150, 95, "is-at MAC-B"),
        _note(150, "ARP: IP → MAC در همان subnet | نتیجه در ARP cache"),
        _note(175, "مثال: gateway را ping کن → arp -a باید MAC گیت‌وی را نشان دهد"),
    ])
    return _svg(inner, 700, 205, "ARP Request / Reply")


def dhcp_dora() -> str:
    inner = "".join([
        _box(20, 55, 100, 44, "Client", "#0ea5e9"),
        _box(160, 55, 100, 44, "Discover", "#f59e0b"),
        _box(300, 55, 100, 44, "Offer", "#8b5cf6"),
        _box(440, 55, 100, 44, "Request", "#2563eb"),
        _box(580, 55, 100, 44, "Ack", "#16a34a"),
        _line(120, 77, 160, 77),
        _line(260, 77, 300, 77),
        _line(400, 77, 440, 77),
        _line(540, 77, 580, 77),
        _note(130, "DORA: Discover→Offer→Request→Ack | Relay اگر سرور در VLAN دیگر باشد"),
        _note(155, "مثال: ipconfig /renew | خطا: APIPA 169.254.x.x = سرور/ریلی نرسیده"),
    ])
    return _svg(inner, 720, 185, "DHCP — DORA")


def dns_resolve() -> str:
    inner = "".join([
        _box(20, 50, 100, 44, "کلاینت", "#0ea5e9"),
        _box(150, 50, 110, 44, "Resolver", "#8b5cf6"),
        _box(290, 50, 90, 44, "Root", "#f59e0b"),
        _box(410, 50, 90, 44, "TLD", "#2563eb"),
        _box(530, 50, 120, 44, "Authoritative", "#16a34a"),
        _line(120, 72, 150, 72),
        _line(260, 72, 290, 72),
        _line(380, 72, 410, 72),
        _line(500, 72, 530, 72),
        _note(130, "Cache + TTL سرعت می‌دهد | Split-Horizon: پاسخ داخل/خارج متفاوت"),
        _note(155, "مثال: dig example.com A | nslookup example.com 8.8.8.8"),
    ])
    return _svg(inner, 720, 185, "DNS Resolution")


def nat_pat() -> str:
    inner = "".join([
        _box(20, 55, 140, 48, "LAN 10.10.10.50", "#0ea5e9"),
        _box(220, 55, 160, 48, "NAT Router", "#f59e0b"),
        _box(460, 55, 180, 48, "WAN 203.0.113.10", "#16a34a"),
        _line(160, 79, 220, 79, "Src rewrite"),
        _line(380, 79, 460, 79, "to Internet"),
        _note(140, "PAT: چند داخلی با یک Public + پورت | Static NAT برای سرور"),
        _note(165, "مثال: show ip nat translations | داخل 10.10.10.50:51514 ↔ 203.0.113.10:51514"),
    ])
    return _svg(inner, 700, 195, "NAT / PAT")


def vlan_trunk() -> str:
    inner = "".join([
        _box(20, 40, 100, 40, "PC VLAN10", "#0ea5e9"),
        _box(20, 100, 100, 40, "PC VLAN20", "#8b5cf6"),
        _box(180, 60, 120, 60, "سوئیچ A", "#2563eb"),
        _box(380, 60, 120, 60, "سوئیچ B", "#2563eb"),
        _box(560, 40, 100, 40, "PC VLAN10", "#0ea5e9"),
        _box(560, 100, 100, 40, "PC VLAN20", "#8b5cf6"),
        _line(120, 60, 180, 80),
        _line(120, 120, 180, 100),
        _line(300, 90, 380, 90, "Trunk 802.1Q"),
        _line(500, 80, 560, 60),
        _line(500, 100, 560, 120),
        _note(170, "Access=یک VLAN | Trunk=چند VLAN با تگ | Native بدون تگ"),
        _note(195, "مثال: switchport mode trunk | allowed vlan 10,20"),
    ])
    return _svg(inner, 720, 220, "VLAN Access + Trunk")


def ospf_areas() -> str:
    inner = "".join([
        _box(260, 40, 140, 44, "Area 0 Backbone", "#2563eb"),
        _box(40, 120, 120, 44, "Area 1", "#0ea5e9"),
        _box(280, 120, 120, 44, "Area 2", "#8b5cf6"),
        _box(520, 120, 120, 44, "Area 3", "#f59e0b"),
        _line(160, 130, 260, 70),
        _line(340, 84, 340, 120),
        _line(460, 70, 520, 130),
        _note(190, "همه Areaها باید به Area 0 وصل شوند | LSA نوع‌ها نقش مختلف دارند"),
        _note(215, "مثال: show ip ospf neighbor | show ip route ospf"),
    ])
    return _svg(inner, 700, 240, "OSPF Areas")


def bgp_as() -> str:
    inner = "".join([
        _box(40, 60, 130, 50, "AS 65001\nISP-A", "#0ea5e9"),
        _box(280, 60, 140, 50, "AS 65000\nشرکت", "#2563eb"),
        _box(520, 60, 130, 50, "AS 65002\nISP-B", "#16a34a"),
        _line(170, 85, 280, 85, "eBGP"),
        _line(420, 85, 520, 85, "eBGP"),
        _note(150, "سیاست با prefix-list/route-map | Local Pref / AS-Path / MED"),
        _note(175, "مثال: show ip bgp summary | شبکه باید از هر دو ISP reachable باشد"),
    ])
    return _svg(inner, 700, 205, "BGP Multi-Homed")


def vpn_ipsec() -> str:
    inner = "".join([
        _box(20, 55, 130, 48, "Site A LAN", "#0ea5e9"),
        _box(180, 55, 120, 48, "GW-A IPsec", "#2563eb"),
        _box(380, 55, 120, 48, "GW-B IPsec", "#2563eb"),
        _box(530, 55, 130, 48, "Site B LAN", "#16a34a"),
        _line(300, 79, 380, 79, "Internet (encrypted)"),
        _line(150, 79, 180, 79),
        _line(500, 79, 530, 79),
        _note(140, "Phase1=IKE SA | Phase2=IPsec SA | Interesting traffic"),
        _note(165, "مثال: show crypto isakmp sa | ترافیک 10.1.0.0/24 ↔ 10.2.0.0/24"),
    ])
    return _svg(inner, 720, 195, "Site-to-Site IPsec VPN")


def firewall_zones() -> str:
    inner = "".join([
        _box(20, 55, 100, 48, "Trust\nLAN", "#16a34a"),
        _box(160, 55, 120, 48, "Firewall\nPolicy", "#f59e0b"),
        _box(320, 30, 100, 40, "DMZ", "#8b5cf6"),
        _box(320, 90, 100, 40, "Untrust", "#dc2626"),
        _box(480, 55, 140, 48, "Internet / Server", "#0ea5e9"),
        _line(120, 79, 160, 79),
        _line(280, 70, 320, 50),
        _line(280, 88, 320, 110),
        _note(160, "Default deny | از specific به general | Log برای deny"),
        _note(185, "مثال: LAN→Web allow 80/443 | LAN→Any deny | DMZ→LAN deny"),
    ])
    return _svg(inner, 700, 215, "فایروال Zone و Policy")


def stp_loop() -> str:
    inner = "".join([
        _box(280, 30, 120, 40, "Root Bridge", "#16a34a"),
        _box(40, 110, 120, 40, "SW-A", "#2563eb"),
        _box(280, 110, 120, 40, "SW-B", "#2563eb"),
        _box(520, 110, 120, 40, "SW-C", "#2563eb"),
        _line(160, 120, 280, 120),
        _line(400, 120, 520, 120),
        _line(340, 70, 340, 110),
        _line(100, 110, 300, 50, ""),
        _note(175, "بدون STP حلقه = Broadcast storm | با STP یک لینک Blocking"),
        _note(200, "مثال: show spanning-tree | BPDU Guard روی access"),
    ])
    return _svg(inner, 700, 230, "STP و جلوگیری از Loop")


def ha_hsrp() -> str:
    inner = "".join([
        _box(40, 70, 100, 44, "کلاینت", "#0ea5e9"),
        _box(200, 40, 140, 44, "R1 Active", "#16a34a"),
        _box(200, 110, 140, 44, "R2 Standby", "#f59e0b"),
        _box(420, 70, 160, 44, "VIP 10.10.10.1", "#8b5cf6"),
        _line(140, 92, 200, 62),
        _line(140, 92, 200, 132),
        _note(180, "VIP مشترک | اگر Active بمیرد Standby بالا می‌آید"),
        _note(205, "مثال: show standby | priority و preempt را درست تنظیم کن"),
    ])
    return _svg(inner, 650, 230, "HA — HSRP/VRRP")


def qos_queue() -> str:
    inner = "".join([
        _box(20, 50, 100, 100, "ترافیک\nمخلوط", "#64748b"),
        _box(180, 40, 120, 36, "Voice EF", "#16a34a"),
        _box(180, 85, 120, 36, "Biz AF", "#2563eb"),
        _box(180, 130, 120, 36, "Best Effort", "#f59e0b"),
        _box(380, 70, 140, 50, "خروجی WAN", "#0ea5e9"),
        _line(120, 100, 180, 58),
        _line(120, 100, 180, 103),
        _line(120, 100, 180, 148),
        _line(300, 100, 380, 95),
        _note(190, "Classify → Mark → Queue → Police/Shape"),
        _note(215, "مثال: voice روی EF | نباید همه را Priority کنی و لینک را خفه کنی"),
    ])
    return _svg(inner, 600, 245, "QoS صف‌بندی")


# ——— نگاشت دسته → نمودارها ———

CAT_GRAPHICS: Dict[str, List[str]] = {
    "vlan": ["vlan", "switch", "packet", "osi"],
    "stp": ["stp", "switch", "packet"],
    "ospf": ["ospf", "router", "packet"],
    "bgp": ["bgp", "router", "packet"],
    "acl": ["firewall", "router", "packet"],
    "nat": ["nat", "packet", "router"],
    "vpn": ["vpn", "packet", "router"],
    "dhcp": ["dhcp", "packet", "osi"],
    "dns": ["dns", "packet", "osi"],
    "wireless": ["wifi", "packet", "osi", "dhcp"],
    "firewall": ["firewall", "nat", "packet"],
    "ha": ["ha", "router", "packet"],
    "qos": ["qos", "packet"],
    "tcpip": ["osi", "tcp", "arp", "packet", "router"],
    "security": ["firewall", "vpn", "packet"],
    "mpls": ["router", "packet", "osi"],
    "vxlan": ["packet", "switch", "osi"],
    "multicast": ["packet", "router"],
    "linux": ["packet", "firewall", "osi"],
    "windows": ["dns", "dhcp", "packet"],
    "python": ["packet", "osi"],
    "general": ["packet", "osi", "router", "switch"],
}

_BUILDERS = {
    "packet": packet_path_l2_l3,
    "wifi": packet_path_wireless,
    "switch": switch_decision,
    "router": router_decision,
    "osi": osi_packet_build,
    "tcp": tcp_handshake,
    "arp": arp_flow,
    "dhcp": dhcp_dora,
    "dns": dns_resolve,
    "nat": nat_pat,
    "vlan": vlan_trunk,
    "ospf": ospf_areas,
    "bgp": bgp_as,
    "vpn": vpn_ipsec,
    "firewall": firewall_zones,
    "stp": stp_loop,
    "ha": ha_hsrp,
    "qos": qos_queue,
}


def graphics_for_category(cat: str) -> List[str]:
    keys = CAT_GRAPHICS.get(cat) or CAT_GRAPHICS["general"]
    out = []
    for k in keys:
        fn = _BUILDERS.get(k)
        if fn:
            out.append(fn())
    return out


def all_infographics() -> List[Tuple[str, str]]:
    order = [
        ("مسیر پکت تا اینترنت", packet_path_l2_l3),
        ("مسیر وایرلس", packet_path_wireless),
        ("تصمیم سوئیچ", switch_decision),
        ("تصمیم روتر", router_decision),
        ("Encapsulation", osi_packet_build),
        ("TCP Handshake", tcp_handshake),
        ("ARP", arp_flow),
        ("DHCP DORA", dhcp_dora),
        ("DNS", dns_resolve),
        ("NAT/PAT", nat_pat),
        ("VLAN + Trunk", vlan_trunk),
        ("OSPF Areas", ospf_areas),
        ("BGP Multi-Home", bgp_as),
        ("IPsec VPN", vpn_ipsec),
        ("فایروال Zone", firewall_zones),
        ("STP Loop", stp_loop),
        ("HSRP/VRRP", ha_hsrp),
        ("QoS", qos_queue),
    ]
    return [(t, fn()) for t, fn in order]


def markdown_block(cat: str) -> str:
    svgs = graphics_for_category(cat)
    if not svgs:
        return ""
    return (
        "\n\n---\n\n## اینفوگرافیک + مثال عملی\n\n"
        "نمودارها جریان واقعی را نشان می‌دهند؛ مثال زیر هر نمودار را در Lab تکرار کن.\n\n"
        + "\n\n".join(svgs)
        + "\n"
    )


def worked_example(cat: str, topic: str) -> str:
    """مثال عددی/سناریویی عمیق‌تر برای هر دسته."""
    examples = {
        "vlan": f"""### مثال عددی VLAN — مرتبط با «{topic}»

توپولوژی: SW1 Fa0/1 Access VLAN 10 (PC-A 10.10.10.10/24) | Fa0/2 Access VLAN 20 (PC-B 10.10.20.10/24) | Gi0/1 Trunk به روتر.

1. PC-A نمی‌تواند PC-B را مستقیم پینگ کند (VLAN جدا).
2. روتر با SVI یا Router-on-a-Stick: `encapsulation dot1Q 10` و `20`.
3. Verify: `show vlan brief` | `show interfaces trunk` | `ping` از PC-A به GW VLAN10.
4. اشتباه رایج: native VLAN ناهمسان روی دو سر trunk → ترافیک بدون تگ قاطی می‌شود.
""",
        "tcpip": f"""### مثال Encapsulation — «{topic}»

درخواست: `curl https://example.com`

1. DNS → IP (مثلاً 93.184.216.34)
2. TCP SYN به 93.184.216.34:443
3. IP header: Src=IP کلاینت Dst=93.184.216.34 TTL=64
4. Ethernet: Dst MAC = gateway (از ARP)
5. اگر پینگ OK ولی HTTPS نه: به ACL/فایروال پورت 443 یا SNI نگاه کن.
""",
        "nat": f"""### مثال NAT — «{topic}»

داخل: 10.10.10.0/24 | بیرون: 203.0.113.10

```
ip nat inside source list 1 interface Gig0/0 overload
access-list 1 permit 10.10.10.0 0.0.0.255
```

Verify: از PC داخلی `curl ifconfig.me` باید 203.0.113.10 ببینید | `show ip nat translations`
""",
        "ospf": f"""### مثال OSPF — «{topic}»

R1–R2 Area 0 روی 10.0.0.0/30 | LAN R1: 10.1.1.0/24 | LAN R2: 10.2.2.0/24

```
router ospf 1
 network 10.0.0.0 0.0.0.3 area 0
 network 10.1.1.0 0.0.0.255 area 0
```

Verify: `show ip ospf neighbor` = FULL | `show ip route ospf` باید 10.2.2.0 را ببینید.
""",
        "dhcp": f"""### مثال DHCP — «{topic}»

کلاینت VLAN 30 بدون IP ثابت. سرور DHCP روی VLAN 10.

روی روتر: `ip helper-address 10.10.10.50` روی SVI VLAN30.

Verify: کلاینت IP از scope می‌گیرد | اگر 169.254 ماند: helper یا trust snooping یا سرور down.
""",
        "dns": f"""### مثال DNS — «{topic}»

```
dig www.example.com A +trace
nslookup www.example.com 8.8.8.8
```

اگر نام resolve نشود ولی IP مستقیم باز شود: مشکل DNS است نه لینک.
""",
        "vpn": f"""### مثال VPN — «{topic}»

SiteA 10.1.0.0/24 ↔ SiteB 10.2.0.0/24 | Phase1 AES256/SHA256 | Phase2 ESP

Verify: `show crypto isakmp sa` = QM_IDLE | پینگ از 10.1.0.10 به 10.2.0.10

اگر Phase1 بالا و پینگ نه: interesting traffic یا ACL تونل را چک کن.
""",
        "wireless": f"""### مثال وایرلس — «{topic}»

SSID Corp → VLAN 40 → DHCP 10.40.40.0/24 → GW 10.40.40.1

کلاینت وصل می‌شود ولی اینترنت ندارد: 1) IP گرفته؟ 2) GW پینگ؟ 3) DNS؟ 4) ACL/NAT؟
""",
        "firewall": f"""### مثال Policy — «{topic}»

قانون: LAN → Internet allow 80/443 | LAN → DMZ allow 22 به 10.50.50.10 | Any → LAN deny

ترتیب مهم است: اول specific بعد general. Log on deny برای RCA.
""",
        "bgp": f"""### مثال BGP — «{topic}»

دو ISP: Primary pref بالاتر | Backup فقط اگر Primary قطع شد.

```
route-map FROM-ISP1 permit 10
 set local-preference 200
```

Verify: `show ip bgp` | مسیر پیش‌فرض از ISP1 باشد.
""",
    }
    return examples.get(
        cat,
        f"""### مثال عملی — «{topic}»

1. Baseline بگیر (`show` / لاگ).
2. یک تغییر کوچک و برگشت‌پذیر اعمال کن.
3. Verify محلی و از کلاینت.
4. عمداً یک شکست وارد کن و با RCA پیدا کن.
5. Rollback را اجرا کن.
""",
    )
