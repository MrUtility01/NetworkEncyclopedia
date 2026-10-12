# -*- coding: utf-8 -*-
"""محتوای درس — فقط حول همان موضوع عنوان؛ بدون قاطی کردن مطالب بی‌ربط."""
from __future__ import annotations
import re
from typing import Any, Dict, List, Tuple
from core.rich_data import BANKS, COMMON

def level_tag(title: str) -> str:
    m = re.match(r"\[(L[0-4])\]", title or "")
    return m.group(1) if m else "L0"

def clean_topic(title: str) -> str:
    t = re.sub(r"^\[L[0-4]\]\s*", "", title or "").strip()
    t = re.sub(r"\s*[—\-]\s*(آشنایی|مقدماتی|ادمین|مهندس|خبره).*$", "", t, flags=re.I)
    return t.strip() or (title or "موضوع")

def _cat_for(topic: str) -> str:
    t = (topic or "").lower()
    if any(k in t for k in ("vlan", "trunk", "svi", "access port")):
        return "vlan"
    if any(k in t for k in ("ospf", "lsa", "area", "neighbor")):
        return "ospf"
    if any(k in t for k in ("bgp", "as number", "prefix-list", "route-map")):
        return "bgp"
    if any(k in t for k in ("nat", "pat", "masquerade", "source nat")):
        return "nat"
    if any(k in t for k in ("dhcp", "dora", "lease", "relay")):
        return "dhcp"
    if any(k in t for k in ("dns", "resolver", "zone", "record")):
        return "dns"
    if any(k in t for k in ("vpn", "ipsec", "tunnel", "phase")):
        return "vpn"
    if any(k in t for k in ("firewall", "acl", "policy", "filter")):
        return "firewall"
    if any(k in t for k in ("wireless", "wifi", "ssid", "wpa")):
        return "wireless"
    if any(k in t for k in ("tcp", "udp", "arp", "icmp", "ip "):
        return "tcpip"
    if any(k in t for k in ("mikrotik", "routeros", "winbox")):
        return "mikrotik"
    if any(k in t for k in ("stp", "rstp", "bpdu", "root bridge")):
        return "stp"
    return "general"

def _arch_for(topic: str, cat: str) -> str:
    tables = {
        "vlan": "Access / Trunk / Native / SVI — فقط مفاهیم VLAN",
        "ospf": "Area / Neighbor / LSA / Cost — فقط OSPF",
        "bgp": "AS / eBGP / prefix-list / route-map — فقط BGP",
        "nat": "Inside / Outside / PAT — فقط NAT",
        "dhcp": "DORA / Scope / Relay — فقط DHCP",
        "dns": "Resolver / Zone / TTL — فقط DNS",
        "vpn": "Phase1 / Phase2 / interesting traffic — فقط VPN",
        "firewall": "Zone / Policy / Session — فقط فایروال",
        "wireless": "SSID / AP / Auth / DHCP — فقط وایرلس",
        "tcpip": "IP / TCP|UDP / ARP — فقط پشته",
        "mikrotik": "filter / nat / mangle / route — فقط RouterOS",
        "stp": "Root / RP / DP / Blocking — فقط STP",
    }
    return tables.get(cat, f"اجزای مرتبط با «{topic}» را در همان دامنه نگه دار.")

def _focused_story(topic: str, cat: str) -> str:
    return f"«{topic}» را به‌عنوان یک قابلیت مستقل در نظر بگیر: ورودی، پردازش، خروجی و نقطهٔ شکست."

def _steps_for(topic: str, cat: str) -> str:
    return f"""1. تعریف دقیق «{topic}» و مرز آن
2. پیش‌نیازها و وابستگی‌ها
3. پیکربندی حداقلی قابل Verify
4. تست مثبت و منفی
5. Rollback و مستندسازی"""

def _topic_commands(topic: str, cat: str) -> str:
    samples = {
        "vlan": "show vlan brief\nshow interfaces trunk",
        "ospf": "show ip ospf neighbor\nshow ip route ospf",
        "bgp": "show ip bgp summary\nshow ip bgp",
        "nat": "show ip nat translations\nshow ip nat statistics",
        "dhcp": "show ip dhcp binding\nshow ip dhcp pool",
        "dns": "nslookup example.com\ndig example.com",
        "vpn": "show crypto isakmp sa\nshow crypto ipsec sa",
        "firewall": "show access-lists\nshow firewall",
        "mikrotik": "/ip firewall filter print stats\n/ip route print",
        "wireless": "show ap summary\nshow wireless client summary",
    }
    body = samples.get(cat, f"# دستورات مرتبط با {topic}\nshow running-config | include {topic[:20]}")
    lines = body.strip().splitlines()
    return "\n".join(f"```\n{ln}\n```" for ln in lines if ln.strip())

def _focused_lab(topic: str, cat: str, level: str) -> str:
    return f"""## Lab متمرکز — {topic}
1. محیط آزمایش (GNS3/EVE/سخت‌افزار)
2. پیکربندی حداقلی «{topic}»
3. Verify با دستورات بالا
4. یک خطا عمدی و RCA
5. Rollback"""

def build_deep_fallback(title_fa: str, title_en: str = "", level: str | None = None) -> Dict[str, Any]:
    level = level or level_tag(title_fa)
    topic = clean_topic(title_fa)
    cat = _cat_for(topic)
    spec = {"extra_full": "", "extra_commands": "", "extra_lab": "", "extra_notes": ""}
    try:
        from core.specialized_depth import specialized_block, detect_specialty
        sp = detect_specialty(title_fa, title_en)
        if sp:
            spec = specialized_block(title_fa, title_en, level) or spec
    except Exception:
        pass

    summary = f"درس «{topic}» — فقط همین موضوع؛ مثال و دستور و Lab متمرکز. سطح {level}."
    example = f"مثال: در یک سناریوی سازمانی کوچک، «{topic}» را پیاده کن و با دستورات Verify نتیجه را ثبت کن."
    info = spec.get("extra_full") or ""

    full = f"""# {topic}

**سطح:** {level}

## تصویر ذهنی

{_focused_story(topic, cat)}

---

## اجزا و معماری مربوط به همین موضوع

{_arch_for(topic, cat)}

---

## جریان عملی «{topic}»

{_steps_for(topic, cat)}
{info}
---

## مثال حل‌شده مخصوص «{topic}»

{example}

---

## جمع‌بندی یک‌خطی

«{topic}» را وقتی بلدی که بتوانی بدون دست‌زدن به بقیهٔ شبکه، آن را Verify و در صورت نیاز Rollback کنی.
"""

    return {
        "summary": summary,
        "full_content": full,
        "commands": _topic_commands(topic, cat) + ("\n" + (spec.get("extra_commands") or "")),
        "examples": _focused_lab(topic, cat, level) + "\n\n" + example + ("\n\n" + (spec.get("extra_lab") or "")),
        "notes": f"## فقط «{topic}»\n\nVerify و RCA را به همین موضوع محدود کن.\n" + (spec.get("extra_notes") or ""),
        "level": level,
        "topic": topic,
        "category": cat,
    }
