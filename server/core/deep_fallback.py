# -*- coding: utf-8 -*-
"""موتور محتوای عمیق — با اینفوگرافیک و مثال عددی وابسته به دسته."""
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
        "vlan": f"در یک سازمان دو دپارتمان روی یک سوئیچ هستند. بدون جداسازی «{topic}»، broadcast و ترافیک حساس قاطی می‌شود.",
        "ospf": f"لینک اصلی بین دو سایت قطع شده. «{topic}» باید مسیر پشتیبان را سریع جایگزین کند.",
        "bgp": f"دو ISP دارید. بدون سیاست درست «{topic}» ترافیک از لینک گران می‌رود یا blackhole می‌گیرید.",
        "nat": f"اشتباه در «{topic}» یا همه اینترنت را به داخل باز می‌کند یا سرویس از بیرون timeout می‌دهد.",
        "wireless": f"کاربران در راهرو وای‌فای دارند ولی در اتاق جلسه قطع می‌شود — «{topic}» را لایه به لایه ایزوله کنید.",
        "tcpip": f"پینگ جواب می‌دهد ولی اپلیکیشن نه. بدون فهم «{topic}» بین لایه ۳ و ۴ گیر می‌کنید.",
    }
    return stories.get(
        cat,
        f"NOC گزارش می‌دهد سرویس مرتبط با «{topic}» ناپایدار است. از لایه ۱ تا ۷ ایزوله کنید و با شواهد رفع کنید.",
    )


def _arch_table(cat: str) -> str:
    tables = {
        "vlan": "| جزء | نقش |\n|-----|-----|\n| Access | یک VLAN |\n| Trunk | چند VLAN + 802.1Q |\n| Native | بدون تگ |\n| SVI | gateway L3 |",
        "ospf": "| جزء | نقش |\n|-----|-----|\n| Area 0 | Backbone |\n| Neighbor | adjacency |\n| LSA | توپولوژی |\n| Cost | معیار مسیر |",
        "bgp": "| جزء | نقش |\n|-----|-----|\n| AS | دامنه سیاست |\n| eBGP/iBGP | بین/داخل |\n| Prefix-list | فیلتر |\n| Route-map | سیاست |",
        "nat": "| جزء | نقش |\n|-----|-----|\n| Inside | LAN |\n| Outside | WAN |\n| PAT | چند به یک |\n| Static | یک به یک |",
        "dhcp": "| جزء | نقش |\n|-----|-----|\n| DORA | چهار مرحله |\n| Scope | محدوده |\n| Relay | بین VLAN |\n| Lease | مدت |",
        "dns": "| جزء | نقش |\n|-----|-----|\n| Resolver | کلاینت |\n| Recursive | جستجو |\n| Auth | zone |\n| TTL | cache |",
        "vpn": "| جزء | نقش |\n|-----|-----|\n| Phase1 | IKE |\n| Phase2 | IPsec |\n| SA | association |\n| PFS | secrecy |",
        "firewall": "| جزء | نقش |\n|-----|-----|\n| Zone | گروه |\n| Policy | قانون |\n| Session | حالت |\n| Log | رویداد |",
        "wireless": "| جزء | نقش |\n|-----|-----|\n| SSID | نام |\n| AP | رادیو |\n| WLC | کنترلر |\n| CAPWAP | تونل |",
        "tcpip": "| جزء | نقش |\n|-----|-----|\n| IP | منطقی |\n| TCP/UDP | انتقال |\n| ARP | IP→MAC |\n| ICMP | کنترل |",
    }
    return tables.get(cat, "| جزء | نقش |\n|-----|-----|\n| Control | تصمیم |\n| Data | عبور ترافیک |\n| Mgmt | پیکربندی |")


def _frame_steps(cat: str) -> str:
    steps = {
        "vlan": "1. فریم از access\n2. تعیین VLAN\n3. تگ روی trunk\n4. forward در همان VLAN\n5. L3 فقط با SVI/روتر",
        "ospf": "1. Hello\n2. DBD/LSA\n3. LSDB یکسان\n4. SPF\n5. نصب route",
        "bgp": "1. TCP 179\n2. UPDATE\n3. Best path\n4. RIB/FIB\n5. سیاست",
        "nat": "1. پکت داخلی\n2. match rule\n3. rewrite\n4. WAN\n5. ترجمه معکوس",
        "dhcp": "1. Discover\n2. Offer\n3. Request\n4. Ack\n5. Renew",
        "dns": "1. پرسش\n2. cache/recursive\n3. Root→TLD→Auth\n4. پاسخ+TTL",
        "vpn": "1. IKE1\n2. IKE2\n3. interesting traffic\n4. encrypt\n5. DPD",
        "wireless": "1. Association\n2. Auth\n3. DHCP\n4. Gateway\n5. Internet",
        "tcpip": "1. App\n2. L4 port\n3. IP\n4. MAC\n5. Physical",
        "stp": "1. Root\n2. RP/DP\n3. Block\n4. BPDU\n5. reconverge",
    }
    return steps.get(cat, "1. Backup\n2. Change\n3. Verify\n4. RCA\n5. Rollback")


def _lab_concrete(topic: str, cat: str, level: str) -> str:
    base = f"""# Lab — {topic}

## توپولوژی
۲ کلاینت + سوئیچ + روتر (یا EVE-NG/GNS3)

## مراحل
1. Baseline: `show ip interface brief` / لاگ
2. Backup: `copy run start`
3. تغییر حداقلی «{topic}»
4. Verify محلی + از کلاینت
5. Failure injection و RCA
6. Rollback
"""
    if level in ("L3", "L4"):
        base += f"\n## سطح {level}\nChange window + Runbook + مانیتور ۳۰ دقیقه\n"
    return base


def _rca_table(cat: str) -> str:
    rows = ERRORS.get(cat, [
        ("قطع کامل", "فیزیکی/GW", "show interface / ping"),
        ("بعضی کلاینت‌ها", "VLAN/ACL/DNS", "مقایسه خوب/بد"),
        ("کندی", "duplex/DNS", "counters / dig"),
    ])
    lines = ["| علامت | علت | دستور |", "|--------|------|--------|"]
    for a, b, c in rows[:6]:
        lines.append(f"| {a} | {b} | `{c}` |")
    return "\n".join(lines)


def _security_block(cat: str, level: str) -> str:
    common = "- AAA/SSH\n- Backup قبل change\n- Management جدا از User\n"
    extra = {
        "vlan": "- Native غیرپیش‌فرض\n- Prune VLAN اضافه",
        "stp": "- BPDU Guard\n- Root Guard",
        "dhcp": "- Snooping\n- Trust فقط uplink",
        "wireless": "- WPA2/3-Ent\n- Guest جدا",
        "firewall": "- Default deny\n- Log deny",
        "vpn": "- AES-GCM\n- PFS",
    }
    return common + extra.get(cat, "")


def _level_guidance(level: str) -> str:
    return {
        "L0": "تصویر ذهنی و نمودار؛ حفظ دستور بعداً.",
        "L1": "Lab ساده + خواندن خروجی show.",
        "L2": "پیکربندی + Verify + Rollback.",
        "L3": "طراحی و RCA.",
        "L4": "معماری و Change Control.",
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

    summary = (
        f"«{topic}» ({level_fa}) — با اینفوگرافیک مسیر پکت و مثال عددی؛ "
        f"تمرکز روی جریان واقعی، Verify و Rollback."
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
                    ("copy running-config startup-config", "ذخیره بعد Verify"),
                ]
            ),
        ]
    )

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

---

## جمع‌بندی

1. Verify اول برای «{topic}»
2. نقطه شکست رایج دسته {cat}
3. مسیر Rollback
"""

    return {
        "summary": summary,
        "full_content": full,
        "commands": commands,
        "examples": (_lab_concrete(topic, cat, level) + "\n\n" + (example or "")),
        "notes": f"## RCA — {topic}\n\n{_rca_table(cat)}\n\n{_level_guidance(level)}\n",
        "level": level,
        "topic": topic,
        "category": cat,
    }
