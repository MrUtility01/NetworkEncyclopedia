# -*- coding: utf-8 -*-
"""اینفوگرافیک SVG — مسیر پکت و اجزای شبکه برای درج در درس و UI."""
from __future__ import annotations

from typing import Dict, List, Tuple


def _svg_wrap(inner: str, w: int = 720, h: int = 220, title: str = "") -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="100%" style="max-width:{w}px;background:#f8fafc;border:1px solid #e2e8f0;'
        f'border-radius:12px;margin:12px 0">\n'
        f'<text x="16" y="22" font-family="Tahoma,sans-serif" font-size="13" '
        f'fill="#0f172a" font-weight="bold">{title}</text>\n'
        f"{inner}\n</svg>"
    )


def _box(x: int, y: int, w: int, h: int, label: str, color: str = "#2563eb") -> str:
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" '
        f'fill="{color}" opacity="0.12" stroke="{color}" stroke-width="2"/>\n'
        f'<text x="{x + w // 2}" y="{y + h // 2 + 5}" text-anchor="middle" '
        f'font-family="Tahoma,sans-serif" font-size="12" fill="#0f172a">{label}</text>\n'
    )


def _arrow(x1: int, y1: int, x2: int, y2: int, label: str = "") -> str:
    s = (
        f'<defs><marker id="ah" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">'
        f'<path d="M0,0 L6,3 L0,6 Z" fill="#64748b"/></marker></defs>\n'
        if "id=\"ah\"" not in label
        else ""
    )
    # single marker def once - caller may duplicate; browsers tolerate
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#64748b" '
        f'stroke-width="2" marker-end="url(#ah)"/>\n'
        + (
            f'<text x="{(x1 + x2) // 2}" y="{y1 - 8}" text-anchor="middle" '
            f'font-family="Tahoma,sans-serif" font-size="10" fill="#64748b">{label}</text>\n'
            if label
            else ""
        )
    )


def packet_path_l2_l3() -> str:
    """کلاینت → سوئیچ → روتر → مودم/ISP → اینترنت"""
    parts = []
    parts.append(
        '<defs><marker id="ah" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">'
        '<path d="M0,0 L6,3 L0,6 Z" fill="#64748b"/></marker></defs>'
    )
    boxes = [
        (20, 80, 100, 56, "PC / کلاینت", "#0ea5e9"),
        (150, 80, 100, 56, "سوئیچ L2", "#8b5cf6"),
        (280, 80, 100, 56, "روتر / L3", "#2563eb"),
        (410, 80, 100, 56, "مودم / FW", "#f59e0b"),
        (540, 80, 120, 56, "ISP / اینترنت", "#16a34a"),
    ]
    for b in boxes:
        parts.append(_box(*b))
    ys = 108
    for x1, x2, lab in (
        (120, 150, "Ethernet"),
        (250, 280, "VLAN/Trunk"),
        (380, 410, "IP/NAT"),
        (510, 540, "WAN"),
    ):
        parts.append(
            f'<line x1="{x1}" y1="{ys}" x2="{x2}" y2="{ys}" stroke="#64748b" '
            f'stroke-width="2" marker-end="url(#ah)"/>'
        )
        parts.append(
            f'<text x="{(x1 + x2) // 2}" y="{ys - 10}" text-anchor="middle" '
            f'font-family="Tahoma,sans-serif" font-size="10" fill="#64748b">{lab}</text>'
        )
    parts.append(
        '<text x="16" y="175" font-family="Tahoma,sans-serif" font-size="11" fill="#475569">'
        "① MAC learning در سوئیچ  ② تصمیم مسیریابی در روتر  ③ NAT روی مرز  ④ تحویل به ISP"
        "</text>"
    )
    parts.append(
        '<text x="16" y="198" font-family="Tahoma,sans-serif" font-size="11" fill="#475569">'
        "بازگشت: همان مسیر معکوس با جدول ARP/MAC و connection tracking"
        "</text>"
    )
    return _svg_wrap("\n".join(parts), 720, 220, "مسیر یک پکت از کلاینت تا اینترنت")


def packet_path_wireless() -> str:
    parts = []
    parts.append(
        '<defs><marker id="ah2" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">'
        '<path d="M0,0 L6,3 L0,6 Z" fill="#64748b"/></marker></defs>'
    )
    boxes = [
        (30, 70, 110, 56, "موبایل / لپ‌تاپ", "#0ea5e9"),
        (180, 70, 100, 56, "AP وایرلس", "#8b5cf6"),
        (320, 70, 100, 56, "سوئیچ", "#6366f1"),
        (460, 70, 100, 56, "WLC / روتر", "#2563eb"),
        (600, 70, 90, 56, "اینترنت", "#16a34a"),
    ]
    for b in boxes:
        parts.append(_box(*b))
    ys = 98
    for x1, x2, lab in (
        (140, 180, "802.11"),
        (280, 320, "CAPWAP/Ethernet"),
        (420, 460, "VLAN"),
        (560, 600, "WAN"),
    ):
        parts.append(
            f'<line x1="{x1}" y1="{ys}" x2="{x2}" y2="{ys}" stroke="#64748b" '
            f'stroke-width="2" marker-end="url(#ah2)"/>'
        )
        parts.append(
            f'<text x="{(x1 + x2) // 2}" y="{ys - 10}" text-anchor="middle" '
            f'font-family="Tahoma,sans-serif" font-size="10" fill="#64748b">{lab}</text>'
        )
    parts.append(
        '<text x="16" y="170" font-family="Tahoma,sans-serif" font-size="11" fill="#475569">'
        "Association → Authentication (WPA2/3) → DHCP → Gateway → Internet | Roaming = AP جدید + همان IP"
        "</text>"
    )
    return _svg_wrap("\n".join(parts), 720, 200, "مسیر پکت در شبکه وایرلس سازمانی")


def switch_decision() -> str:
    parts = [
        '<defs><marker id="ah3" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">'
        '<path d="M0,0 L6,3 L0,6 Z" fill="#64748b"/></marker></defs>',
        _box(40, 50, 140, 50, "فریم ورودی", "#0ea5e9"),
        _box(240, 50, 160, 50, "جدول MAC؟", "#f59e0b"),
        _box(480, 30, 140, 40, "Unicast → پورت", "#16a34a"),
        _box(480, 90, 140, 40, "Unknown → Flood", "#dc2626"),
        '<line x1="180" y1="75" x2="240" y2="75" stroke="#64748b" stroke-width="2" marker-end="url(#ah3)"/>',
        '<line x1="400" y1="65" x2="480" y2="50" stroke="#64748b" stroke-width="2" marker-end="url(#ah3)"/>',
        '<line x1="400" y1="85" x2="480" y2="110" stroke="#64748b" stroke-width="2" marker-end="url(#ah3)"/>',
        '<text x="16" y="170" font-family="Tahoma,sans-serif" font-size="11" fill="#475569">'
        "Learning: Source MAC+Port | Aging | Broadcast/Multicast همیشه Flood در VLAN"
        "</text>",
    ]
    return _svg_wrap("\n".join(parts), 680, 200, "تصمیم‌گیری سوئیچ لایه ۲")


def router_decision() -> str:
    parts = [
        '<defs><marker id="ah4" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">'
        '<path d="M0,0 L6,3 L0,6 Z" fill="#64748b"/></marker></defs>',
        _box(30, 55, 120, 50, "پکت IP", "#0ea5e9"),
        _box(190, 55, 140, 50, "Routing Table", "#2563eb"),
        _box(370, 30, 130, 40, "Longest Match", "#16a34a"),
        _box(370, 95, 130, 40, "No route → Drop", "#dc2626"),
        _box(540, 55, 120, 50, "Next-hop / ARP", "#8b5cf6"),
        '<line x1="150" y1="80" x2="190" y2="80" stroke="#64748b" stroke-width="2" marker-end="url(#ah4)"/>',
        '<line x1="330" y1="70" x2="370" y2="50" stroke="#64748b" stroke-width="2" marker-end="url(#ah4)"/>',
        '<line x1="330" y1="90" x2="370" y2="115" stroke="#64748b" stroke-width="2" marker-end="url(#ah4)"/>',
        '<line x1="500" y1="50" x2="540" y2="80" stroke="#64748b" stroke-width="2" marker-end="url(#ah4)"/>',
        '<text x="16" y="175" font-family="Tahoma,sans-serif" font-size="11" fill="#475569">'
        "TTL-- | ACL/NAT در مسیر | Write new L2 header برای hop بعدی"
        "</text>",
    ]
    return _svg_wrap("\n".join(parts), 700, 200, "تصمیم‌گیری روتر لایه ۳")


def osi_packet_build() -> str:
    layers = [
        ("Application", "HTTP / DNS / SSH", "#0ea5e9"),
        ("Transport", "TCP/UDP + Port", "#8b5cf6"),
        ("Network", "IP Src/Dst", "#2563eb"),
        ("Data Link", "MAC + EtherType", "#f59e0b"),
        ("Physical", "بیت روی کابل/رادیو", "#16a34a"),
    ]
    parts = []
    y = 40
    for name, desc, color in layers:
        parts.append(_box(80, y, 560, 28, f"{name}  —  {desc}", color))
        y += 34
    return _svg_wrap("\n".join(parts), 720, 230, "Encapsulation: از App تا کابل (و برعکس Decapsulation)")


CAT_GRAPHICS: Dict[str, List[str]] = {
    "vlan": ["switch", "packet", "osi"],
    "stp": ["switch", "packet"],
    "tcpip": ["osi", "packet", "router"],
    "ospf": ["router", "packet"],
    "bgp": ["router", "packet"],
    "nat": ["packet", "router"],
    "acl": ["router", "packet"],
    "wireless": ["wifi", "packet", "osi"],
    "vpn": ["packet", "router"],
    "firewall": ["packet", "router"],
    "dhcp": ["packet", "osi"],
    "dns": ["packet", "osi"],
    "ha": ["router", "packet"],
    "mpls": ["router", "packet"],
    "vxlan": ["packet", "switch"],
}


def graphics_for_category(cat: str) -> List[str]:
    keys = CAT_GRAPHICS.get(cat, ["packet", "osi"])
    out = []
    mapping = {
        "packet": packet_path_l2_l3,
        "wifi": packet_path_wireless,
        "switch": switch_decision,
        "router": router_decision,
        "osi": osi_packet_build,
    }
    for k in keys:
        fn = mapping.get(k)
        if fn:
            out.append(fn())
    return out


def all_infographics() -> List[Tuple[str, str]]:
    return [
        ("مسیر پکت تا اینترنت", packet_path_l2_l3()),
        ("مسیر وایرلس", packet_path_wireless()),
        ("تصمیم سوئیچ", switch_decision()),
        ("تصمیم روتر", router_decision()),
        ("Encapsulation", osi_packet_build()),
    ]


def markdown_block(cat: str) -> str:
    svgs = graphics_for_category(cat)
    if not svgs:
        return ""
    body = "\n\n".join(svgs)
    return (
        "\n\n---\n\n## اینفوگرافیک مسیر پکت / معماری\n\n"
        "نمودارهای زیر برای درک جریان واقعی ترافیک است — نه حفظ طوطی‌وار.\n\n"
        + body
        + "\n"
    )
