# -*- coding: utf-8 -*-
"""محتوای درس — فقط حول همان موضوع عنوان؛ بدون قاطی کردن مطالب بی‌ربط."""
from __future__ import annotations
import re
from typing import Any, Dict, List, Tuple
from core.rich_data import BANKS, COMMON, ERRORS, SCENARIO_HOOKS

_LEVEL_FA = {
    "L0": "آشنایی",
    "L1": "مقدماتی",
    "L2": "ادمین",
    "L3": "مهندس",
    "L4": "معمار",
}

_CATS: List[Tuple[str, List[str]]] = [
    ("vlan", ["vlan", "trunk", "access", "802.1q", "native vlan", "svi"]),
    ("stp", ["stp", "spanning", "rstp", "bpdu", "root bridge", "portfast"]),
    ("ospf", ["ospf", "area", "lsa", "neighbor", "dr", "bdr"]),
    ("bgp", ["bgp", "prefix-list", "route-map", "as number", "ebgp", "ibgp"]),
    ("acl", ["acl", "access-list", "extended", "standard"]),
    ("nat", ["nat", "pat", "overload", "static nat"]),
    ("vpn", ["vpn", "ipsec", "ike", "tunnel", "phase1", "phase2"]),
    ("dhcp", ["dhcp", "scope", "lease", "relay", "helper", "dora"]),
    ("dns", ["dns", "resolver", "zone", "forwarder"]),
    ("wireless", ["wifi", "wireless", "ssid", "wpa", "wlc", "roaming", "ap", "وایرلس"]),
    ("firewall", ["firewall", "fortigate", "asa", "policy", "zone"]),
    ("ha", ["hsrp", "vrrp", "glbp", "failover"]),
    ("qos", ["qos", "dscp", "policing", "shaping"]),
    ("tcpip", ["tcp", "udp", "icmp", "handshake", "arp", "ipv4", "ipv6", "subnet"]),
    ("mpls", ["mpls", "ldp", "label", "vrf", "l3vpn"]),
    ("security", ["aaa", "radius", "tacacs", "802.1x", "port security"]),
    ("linux", ["linux", "iptables", "nftables", "systemd"]),
    ("windows", ["powershell", "gpo", "active directory"]),
    ("python", ["python", "paramiko", "netmiko", "ansible"]),
    ("mikrotik", ["mikrotik", "routeros", "winbox", "pppoe", "queue tree"]),
]


def _level(title: str) -> str:
    m = re.match(r"\[(L[0-4])\]", title or "")
    return m.group(1) if m else "L0"


def _topic(title: str) -> str:
    t = re.sub(r"^\[L[0-4]\]\s*", "", title or "").strip()
    t = re.sub(r"\s*[—\-]\s*(آشنایی|مقدماتی|ادمین|مهندس|خبره).*$", "", t, flags=re.I)
    return t.strip() or (title or "موضوع")


def _cat(topic: str) -> str:
    low = (topic or "").lower()
    for name, keys in _CATS:
        if any(k in low for k in keys):
            return name
    return "general"


def _fmt(pairs):
    return "\n".join(f"```\n{cmd}\n```\n→ {desc}\n" for cmd, desc in pairs)


def _topic_commands(topic: str, cat: str) -> str:
    """فقط دستورات مرتبط با همین موضوع/دسته — نه بانک کلی قاطی."""
    bank = BANKS.get(cat) or []
    # حداکثر ۸ دستور تخصصی دسته
    specialized = bank[:8] if bank else []
    lines = [f"# دستورات مرتبط با «{topic}»\n"]
    if specialized:
        lines.append(_fmt(specialized))
    else:
        # حداقل‌های عمومی فقط اگر دسته ناشناخته است — کوتاه و برچسب‌خورده
        lines.append(_fmt([
            ("show running-config | include " + topic.split()[0][:20], f"جستجو در کانفیگ برای {topic}"),
            ("show logging | last 50", "رویدادهای اخیر"),
        ]))
    lines.append("\n## Backup قبل از تغییر مربوط به این درس\n")
    lines.append(_fmt([
        ("show running-config | redirect flash:pre-change.cfg", "بک‌آپ"),
        ("copy running-config startup-config", "ذخیره بعد از Verify موفق"),
    ]))
    return "\n".join(lines)


def _focused_story(topic: str, cat: str) -> str:
    return (
        f"این درس فقط دربارهٔ «{topic}» است. "
        f"هدف: بفهمی این موضوع دقیقاً چه مشکلی را حل می‌کند، چطور پیکربندی/مشاهده می‌شود، "
        f"و وقتی خراب است با چه شواهدی تشخیصش می‌دهی — نه مخلوط کردن با مباحث دیگر.\n\n"
        f"اگر در عمل با «{topic}» روبه‌رو شدی، اول همان را ایزوله کن؛ همزمان VLAN و BGP و WiFi را عوض نکن."
    )


def _focused_example(topic: str, cat: str) -> str:
    """مثال عددی که صریحاً نام موضوع درس را دارد."""
    try:
        from core.infographics import worked_example

        ex = worked_example(cat, topic)
        # فقط اگر مثال به دسته مربوط است نگه دار
        if ex and topic.split()[0][:4].lower() in ex.lower() or cat != "general":
            return f"### مثال متمرکز روی «{topic}»\n\n{ex}"
    except Exception:
        pass
    return f"""### مثال متمرکز روی «{topic}»

1. وضعیت قبل را ثبت کن (دستور show مرتبط با {topic}).
2. فقط یک تغییر مربوط به «{topic}» اعمال کن.
3. Verify همان موضوع (نه کل شبکه).
4. اگر fail شد فقط همان مسیر «{topic}» را RCA کن.
5. Rollback همان تغییر.
"""


def _focused_lab(topic: str, cat: str, level: str) -> str:
    return f"""# Lab فقط برای «{topic}»

## محدوده
در این Lab حق داری فقط مؤلفه‌های مرتبط با «{topic}» را تغییر بدهی.

## مراحل
1. Baseline مربوط به {topic}
2. Backup
3. یک تغییر حداقلی روی {topic}
4. Verify همان موضوع
5. Failure تزریقی فقط روی {topic}
6. Rollback

## معیار قبولی
بتوانی با یک جمله بگویی: «مشکل از {topic} هست / نیست» و شاهد داشته باشی.
"""


def _maybe_info(topic: str, cat: str) -> str:
    """اینفوگرافیک فقط اگر با کلیدواژه موضوع جور باشد."""
    try:
        from core.infographics import graphics_for_category, _BUILDERS

        # نگاشت سخت: فقط اگر topic صریحاً به نمودار اشاره دارد
        topic_l = topic.lower()
        wanted = []
        rules = [
            (["vlan", "trunk"], ["vlan", "switch"]),
            (["stp", "spanning"], ["stp"]),
            (["ospf"], ["ospf", "router"]),
            (["bgp"], ["bgp", "router"]),
            (["nat", "pat"], ["nat"]),
            (["dhcp"], ["dhcp"]),
            (["dns"], ["dns"]),
            (["vpn", "ipsec"], ["vpn"]),
            (["wifi", "wireless", "وایرلس", "ssid"], ["wifi"]),
            (["tcp", "handshake"], ["tcp"]),
            (["arp"], ["arp"]),
            (["firewall", "policy", "zone"], ["firewall"]),
            (["hsrp", "vrrp"], ["ha"]),
            (["qos"], ["qos"]),
            (["osi", "encapsulation"], ["osi"]),
            (["مسیر پکت", "packet"], ["packet"]),
        ]
        for keys, graphs in rules:
            if any(k in topic_l for k in keys):
                wanted.extend(graphs)
        if not wanted:
            return ""  # هیچ اینفوگرافیک عمومی قاطی نکن
        # unique preserve order
        seen = set()
        parts = []
        for g in wanted:
            if g in seen:
                continue
            seen.add(g)
            fn = _BUILDERS.get(g)
            if fn:
                parts.append(fn())
        if not parts:
            return ""
        return (
            "\n\n## اینفوگرافیک مرتبط با همین درس\n\n"
            + "\n\n".join(parts)
            + "\n"
        )
    except Exception:
        return ""


def _maybe_specialty(title_fa: str, title_en: str, topic: str, level: str) -> Dict[str, str]:
    """عمق vendor فقط اگر عنوان درس صریحاً همان vendor/domain باشد."""
    blob = f"{title_fa} {title_en} {topic}".lower()
    # کلیدهای سخت — نه هر ACL به security
    hard = {
        "mikrotik": ["mikrotik", "routeros", "winbox"],
        "fortigate": ["fortigate", "fortinet", "fortios"],
        "cisco_l3": ["cisco ios", "ios-xe", "eigrp"],  # فقط اگر صریح
        "wireless": ["wlc", "capwap", "وایرلس", "wireless", "wifi"],
        "automation": ["ansible", "netmiko", "paramiko", "napalm"],
        "voip": ["issabel", "asterisk", "sip ", "voip"],
    }
    # OSPF/BGP depth از specialized cisco فقط اگر عنوان Cisco دارد
    try:
        from core.specialized_depth import specialized_block, detect_specialty

        sp = detect_specialty(title_fa, title_en)
        if not sp:
            return {"extra_full": "", "extra_commands": "", "extra_lab": "", "extra_notes": ""}
        keys = hard.get(sp)
        if keys and not any(k in blob for k in keys):
            # specialty تشخیص داده شده ولی عنوان درس صریح نیست → نچسبان
            if sp in ("cisco_l3", "security"):
                return {"extra_full": "", "extra_commands": "", "extra_lab": "", "extra_notes": ""}
        return specialized_block(title_fa, title_en, level)
    except Exception:
        return {"extra_full": "", "extra_commands": "", "extra_lab": "", "extra_notes": ""}


def _arch_for(topic: str, cat: str) -> str:
    from core.deep_fallback import _arch_table  # not available - inline minimal
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
    base = tables.get(cat, f"اجزای مستقیم «{topic}» را در این بخش نگه دار؛ مبحث موازی ننویس.")
    return f"**تمرکز:** {topic}\n\n{base}"


def _steps_for(topic: str, cat: str) -> str:
    steps = {
        "vlan": "پورت access → VLAN → trunk tag → forward همان VLAN",
        "ospf": "Hello → adjacency → LSA → SPF → route",
        "bgp": "TCP 179 → OPEN → UPDATE → best path",
        "nat": "match → translate → forward → reverse",
        "dhcp": "Discover → Offer → Request → Ack",
        "dns": "query → cache/recursive → answer",
        "vpn": "IKE1 → IKE2 → encrypt data",
        "stp": "elect root → block loop → re-converge",
        "wireless": "associate → auth → DHCP → GW",
        "tcpip": "L4 → IP → MAC → wire",
        "mikrotik": "in-interface → filter/mangle → route → nat → out",
        "firewall": "ingress → policy → session → egress",
    }
    s = steps.get(cat, f"مشاهده → تغییر حداقلی «{topic}» → Verify → Rollback")
    return f"جریان مخصوص «{topic}»:\n{s}"


def build_deep_fallback(
    title_fa: str, title_en: str = "", level: str | None = None
) -> Dict[str, Any]:
    level = level or _level(title_fa)
    topic = _topic(title_fa)
    cat = _cat(topic)
    level_fa = _LEVEL_FA.get(level, level)

    info = _maybe_info(topic, cat)
    example = _focused_example(topic, cat)
    spec = _maybe_specialty(title_fa, title_en, topic, level)
    spec_full = (spec.get("extra_full") or "").strip()
    # اگر specialty به موضوع نمی‌خورد، خالی بماند (از قبل فیلتر شده)

    summary = f"درس «{topic}» — فقط همین موضوع؛ مثال و دستور و Lab متمرکز. سطح {level_fa}."

    full = f"""# {topic}

**سطح:** {level} — {level_fa}  
**EN:** {title_en or topic}

> محدوده این درس: **فقط «{topic}»**. مباحث دیگر را اینجا مخلوط نکن.

---

## چرا «{topic}»؟

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

## عیب‌یابی فقط برای «{topic}»

وقتی علامت دیدی بپرس:
1. آیا شواهد مستقیماً به «{topic}» اشاره دارد؟
2. کدام دستور Verify مخصوص همین موضوع را اجرا کردم؟
3. آیا همزمان چیز دیگری را عوض کردم؟ (نباید)

---

## چک‌لیست

- [ ] تغییر فقط روی «{topic}»
- [ ] Backup
- [ ] Verify مرتبط
- [ ] Rollback آماده‌است

{spec_full}

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
