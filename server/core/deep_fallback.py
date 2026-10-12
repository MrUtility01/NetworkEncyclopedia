# -*- coding: utf-8 -*-
"""موتور محتوای عمیق — اینفوگرافیک + مثال + عمق تخصصی vendor."""
from __future__ import annotations
import re
from typing import Any, Dict, List, Tuple
from core.rich_data import BANKS, COMMON, ERRORS, SCENARIO_HOOKS

_LEVEL_FA = {
    "L0": "آشنایی / تصویر ذهنی",
    "L1": "Junior — مشاهده و Lab ساده",
    "L2": "Administrator — پیکربندی + Verify + Rollback",
    "L3": "Engineer / Senior — طراحی و RCA",
    "L4": "Architect — سازمانی، چندسایت، Change Control",
}

_CATS: List[Tuple[str, List[str]]] = [
    ("vlan", ["vlan", "trunk", "access", "802.1q", "native vlan", "svi"]),
    ("stp", ["stp", "spanning", "rstp", "bpdu", "root bridge", "portfast", "loop"]),
    ("ospf", ["ospf", "area", "lsa", "neighbor", "dr", "bdr", "cost"]),
    ("bgp", ["bgp", "prefix-list", "route-map", "as number", "ebgp", "ibgp", "peering"]),
    ("acl", ["acl", "access-list", "extended", "standard", "named acl"]),
    ("nat", ["nat", "pat", "overload", "static nat", "port forward"]),
    ("vpn", ["vpn", "ipsec", "ike", "tunnel", "phase1", "phase2", "ssl vpn"]),
    ("dhcp", ["dhcp", "scope", "lease", "relay", "helper", "dora", "reservation"]),
    ("dns", ["dns", "resolver", "zone", "forwarder", "dnssec", "split-horizon"]),
    ("wireless", ["wifi", "wireless", "ssid", "wpa", "wlc", "roaming", "ap"]),
    ("firewall", ["firewall", "fortigate", "asa", "policy", "zone"]),
    ("ha", ["hsrp", "vrrp", "glbp", "failover", "active-standby"]),
    ("qos", ["qos", "dscp", "policing", "shaping", "priority"]),
    ("linux", ["linux", "iptables", "nftables", "systemd", "journalctl", "ss "]),
    ("windows", ["windows", "powershell", "gpo", "active directory", "kerberos"]),
    ("storage", ["raid", "nvme", "ssd", "san", "iscsi", "latency", "iops"]),
    ("virtualization", ["vmware", "esxi", "kubernetes", "docker", "pod", "hypervisor"]),
    ("security", ["aaa", "radius", "tacacs", "tls", "snmp", "802.1x", "port security"]),
    ("tcpip", ["tcp", "udp", "icmp", "handshake", "window", "retransmission", "arp", "ip ", "ipv4", "ipv6"]),
    ("mpls", ["mpls", "ldp", "label", "vrf", "l3vpn", "pe ", "ce "]),
    ("multicast", ["multicast", "pim", "igmp", "ssm", "rendezvous"]),
    ("vxlan", ["vxlan", "vni", "vtep", "evpn", "overlay", "underlay"]),
    ("sql", ["sql", "postgres", "mysql", "elasticsearch"]),
    ("python", ["python", "paramiko", "netmiko", "ansible", "automation"]),
]

_ANALOGY = {
    "vlan": "مثل جدا کردن طبقات یک برج با کلیدهای مختلف — هر VLAN یک طبقه امنیتی/پخش است.",
    "stp": "مثل نگهبان تقاطع که یکی از جاده‌های موازی را می‌بندد تا تصادف حلقه‌ای نشود.",
    "ospf": "مثل نقشه مترو که هر ایستگاه همسایه‌ها را اعلام می‌کند و کوتاه‌ترین مسیر محاسبه می‌شود.",
    "bgp": "مثل توافق بین کشورهای همسایه برای عبور بار — سیاست مهم‌تر از کوتاهی مسیر است.",
    "acl": "مثل نگهبانی درب که لیست مجاز/غیرمجاز را چک می‌کند قبل از ورود.",
    "nat": "مثل شماره داخلی شرکت که با یک خط شهری به بیرون حرف می‌زند.",
    "vpn": "مثل لوله زرهی بین دو ساختمان روی خیابان عمومی.",
    "dhcp": "مثل باجه اجاره آدرس موقت در ورودی پارکینگ.",
    "dns": "مثل دفترچه تلفن اینترنت — اسم را به شماره (IP) تبدیل می‌کند.",
    "wireless": "مثل بی‌سیم اداره پست: ثبت‌نام در باجه (AP) بعد تحویل به جاده سیمی.",
    "firewall": "مثل گمرک مرزی با سیاست واردات/صادرات و بازرسی بسته‌ها.",
    "tcpip": "مثل ارسال مرسوله با کد رهگیری (TCP) یا کارت پستال بدون رسید (UDP).",
    "ha": "مثل دو خلبان — اگر یکی از کار بیفتد دیگری کنترل را می‌گیرد.",
    "qos": "مثل خط ویژه آمبولانس در ترافیک — ترافیک حیاتی اول می‌رود.",
}


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


def _story(topic: str, cat: str) -> str:
    hooks = SCENARIO_HOOKS.get(cat) if isinstance(SCENARIO_HOOKS, dict) else None
    if hooks:
        try:
            return hooks[0].format(topic=topic)
        except Exception:
            return hooks[0]
    stories = {
        "vlan": f"بدون جداسازی «{topic}» broadcast و ترافیک حساس قاطی می‌شود.",
        "ospf": f"لینک اصلی قطع شده؛ «{topic}» باید backup را سریع جایگزین کند.",
        "bgp": f"بدون سیاست درست «{topic}» ترافیک از لینک گران می‌رود یا blackhole می‌گیرید.",
        "nat": f"اشتباه در «{topic}» یا همه را باز می‌کند یا سرویس timeout می‌دهد.",
        "wireless": f"«{topic}» را از RF تا DHCP و gateway جدا ایزوله کنید.",
        "tcpip": f"پینگ OK و اپ نه — بدون فهم «{topic}» بین L3/L4 گیر می‌کنید.",
    }
    return stories.get(cat, f"سرویس «{topic}» ناپایدار است — از لایه ۱ تا ۷ با شواهد ایزوله کنید.")


def _arch_table(cat: str) -> str:
    tables = {
        "vlan": "| جزء | نقش |\n|-----|-----|\n| Access | یک VLAN |\n| Trunk | 802.1Q |\n| SVI | gateway L3 |",
        "ospf": "| جزء | نقش |\n|-----|-----|\n| Area 0 | Backbone |\n| LSA | توپولوژی |\n| Cost | معیار |",
        "bgp": "| جزء | نقش |\n|-----|-----|\n| AS | سیاست |\n| eBGP/iBGP | بین/داخل |\n| Route-map | فیلتر |",
        "nat": "| جزء | نقش |\n|-----|-----|\n| Inside/Outside | مرز |\n| PAT | چندبهیک |",
        "dhcp": "| جزء | نقش |\n|-----|-----|\n| DORA | اجاره IP |\n| Relay | بین VLAN |",
        "dns": "| جزء | نقش |\n|-----|-----|\n| Resolver | پرسش |\n| Auth | zone |",
        "vpn": "| جزء | نقش |\n|-----|-----|\n| Phase1/2 | IKE/IPsec |",
        "firewall": "| جزء | نقش |\n|-----|-----|\n| Zone/Policy | کنترل |",
        "wireless": "| جزء | نقش |\n|-----|-----|\n| AP/WLC | دسترسی |",
        "tcpip": "| جزء | نقش |\n|-----|-----|\n| IP/TCP/ARP | پشته |",
    }
    return tables.get(cat, "| جزء | نقش |\n|-----|-----|\n| Control/Data | تصمیم/عبور |")


def _frame_steps(cat: str) -> str:
    steps = {
        "vlan": "1 Access 2 VLAN 3 Tag 4 Forward 5 L3",
        "ospf": "1 Hello 2 LSA 3 SPF 4 Route",
        "bgp": "1 TCP179 2 UPDATE 3 Bestpath 4 RIB",
        "nat": "1 Match 2 Rewrite 3 WAN 4 Reverse",
        "dhcp": "1 Discover 2 Offer 3 Request 4 Ack",
        "dns": "1 Query 2 Recursive 3 Answer",
        "vpn": "1 IKE1 2 IKE2 3 Encrypt",
        "wireless": "1 Assoc 2 Auth 3 DHCP 4 GW",
        "tcpip": "1 App 2 L4 3 IP 4 MAC 5 Phy",
        "stp": "1 Root 2 Block 3 BPDU",
    }
    return steps.get(cat, "1 Backup 2 Change 3 Verify 4 Rollback").replace(" ", "\n")


def _lab_concrete(topic: str, cat: str, level: str) -> str:
    base = f"# Lab — {topic}\n\n1. Baseline\n2. Backup\n3. Change «{topic}»\n4. Verify\n5. Failure + RCA\n6. Rollback\n"
    if level in ("L3", "L4"):
        base += f"\n## {level}\nChange window + Runbook\n"
    return base


def _rca_table(cat: str) -> str:
    rows = ERRORS.get(cat, [
        ("قطع", "فیزیکی/GW", "show interface"),
        ("ناقص", "VLAN/ACL", "مقایسه کلاینت"),
        ("کند", "duplex/DNS", "counters"),
    ])
    lines = ["| علامت | علت | دستور |", "|--------|------|--------|"]
    for a, b, c in rows[:6]:
        lines.append(f"| {a} | {b} | `{c}` |")
    return "\n".join(lines)


def _security_block(cat: str, level: str) -> str:
    common = "- AAA/SSH\n- Backup\n- Mgmt جدا\n"
    extra = {
        "vlan": "- Native غیرپیش‌فرض",
        "stp": "- BPDU Guard",
        "dhcp": "- Snooping",
        "wireless": "- WPA2/3",
        "firewall": "- Default deny",
        "vpn": "- PFS",
    }
    return common + extra.get(cat, "")


def _level_guidance(level: str) -> str:
    return {
        "L0": "نمودار و مفهوم",
        "L1": "Lab + show",
        "L2": "Config + Verify + Rollback",
        "L3": "طراحی و RCA",
        "L4": "معماری و Change Control",
    }.get(level, "")


def build_deep_fallback(
    title_fa: str, title_en: str = "", level: str | None = None
) -> Dict[str, Any]:
    level = level or _level(title_fa)
    topic = _topic(title_fa)
    cat = _cat(topic)
    level_fa = _LEVEL_FA.get(level, level)
    bank = BANKS.get(cat, BANKS.get("general", COMMON))
    story = _story(topic, cat)
    analogy = _ANALOGY.get(cat, f"«{topic}» حلقه‌ای از زنجیره سرویس است.")

    try:
        from core.infographics import markdown_block, worked_example

        info = markdown_block(cat)
        example = worked_example(cat, topic)
    except Exception:
        info = ""
        example = ""

    try:
        from core.specialized_depth import specialized_block

        spec = specialized_block(title_fa, title_en, level)
    except Exception:
        spec = {"extra_full": "", "extra_commands": "", "extra_lab": "", "extra_notes": ""}

    summary = (
        f"«{topic}» ({level_fa}) — اینفوگرافیک + مثال عددی"
        + (" + عمق تخصصی vendor" if spec.get("extra_full") else "")
        + "."
    )

    commands = "\n".join(
        [
            f"# دستورات — {topic} | {level} | {cat}",
            "",
            "## Verify پایه",
            _fmt(COMMON[:6]),
            f"## تخصصی ({cat})",
            _fmt(bank[:14] if len(bank) > 14 else bank),
            "## Backup",
            _fmt(
                [
                    ("show running-config | redirect flash:pre-change.cfg", "بک‌آپ"),
                    ("copy running-config startup-config", "ذخیره"),
                ]
            ),
        ]
    )

    spec_full = (spec.get("extra_full") or "").strip()
    full = f"""# {topic}

**سطح:** {level} — {level_fa}  
**EN:** {title_en or topic}  
**دسته:** {cat}

---

## چرا این موضوع؟

{story}

---

## تشبیه

{analogy}

---

## معماری

{_arch_table(cat)}

---

## جریان گام‌به‌گام

{_frame_steps(cat)}
{info}
## مثال حل‌شده (با اعداد واقعی)

{example}

---

## سطح تو ({level})

{_level_guidance(level)}

---

## امنیت

{_security_block(cat, level)}

---

## RCA

{_rca_table(cat)}

Symptom → Scope → Evidence → Hypothesis → Test → Fix → Verify → Document

---

## چک‌لیست Production

- [ ] Backup + Rollback
- [ ] دامنه تغییر
- [ ] Verify محلی و End-to-End
- [ ] مانیتور بعد از change

{spec_full}

---

## جمع‌بندی

1. Verify اول برای «{topic}»
2. نقطه شکست رایج دسته {cat}
3. مسیر Rollback
"""

    return {
        "summary": summary,
        "full_content": full,
        "commands": commands + ("\n" + (spec.get("extra_commands") or "")),
        "examples": (_lab_concrete(topic, cat, level) + "\n\n" + (example or "") + "\n\n" + (spec.get("extra_lab") or "")),
        "notes": f"## RCA — {topic}\n\n{_rca_table(cat)}\n\n{_level_guidance(level)}\n\n" + (spec.get("extra_notes") or ""),
        "level": level,
        "topic": topic,
        "category": cat,
    }
