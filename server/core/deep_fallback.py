# -*- coding: utf-8 -*-
"""محتوای عمیق عمومی برای درس‌هایی که teacher اختصاصی ندارند."""
from __future__ import annotations
import re
from typing import Any, Dict

def level_tag(title: str) -> str:
    m = re.match(r"\[(L[0-4])\]", title or "")
    return m.group(1) if m else "L0"

def clean_topic(title: str) -> str:
    t = re.sub(r"^\[L[0-4]\]\s*", "", title or "").strip()
    t = re.sub(r"\s*[—\-]\s*(آشنایی|مقدماتی|ادمین|مهندس|خبره).*$", "", t, flags=re.I)
    return t.strip() or (title or "موضوع")

def _cat_for(topic: str) -> str:
    t = (topic or "").lower()
    rules = [
        (("vlan", "trunk", "svi", "access port"), "vlan"),
        (("ospf", "lsa", "area 0", "neighbor ospf"), "ospf"),
        (("bgp", "as number", "prefix-list", "route-map"), "bgp"),
        (("nat", "pat", "masquerade", "source nat"), "nat"),
        (("dhcp", "dora", "lease", "relay agent"), "dhcp"),
        (("dns", "resolver", "zone", "record a"), "dns"),
        (("vpn", "ipsec", "tunnel", "phase1", "phase2", "wireguard", "openvpn"), "vpn"),
        (("firewall", "acl", "policy", "filter", "ids", "ips"), "firewall"),
        (("wireless", "wifi", "ssid", "wpa", "802.11", "wlc"), "wireless"),
        (("tcp", "udp", "arp", "icmp", "mtu", "mss"), "tcpip"),
        (("mikrotik", "routeros", "winbox"), "mikrotik"),
        (("stp", "rstp", "mstp", "bpdu", "root bridge"), "stp"),
        (("qos", "queue", "dscp", "policer", "shaper"), "qos"),
        (("ha", "hsrp", "vrrp", "glbp", "failover", "cluster"), "ha"),
        (("monitor", "snmp", "syslog", "netflow", "prometheus", "grafana", "zabbix"), "monitor"),
        (("automat", "ansible", "terraform", "python net", "api rest", "netconf"), "automation"),
        (("cloud", "aws", "azure", "gcp", "vpc", "s3"), "cloud"),
        (("security", "aaa", "radius", "tacacs", "802.1x", "zero trust", "pki"), "security"),
        (("storage", "san", "nas", "iscsi", "nfs", "smb"), "storage"),
        (("virtual", "vmware", "hyper-v", "kvm", "docker", "kubernet"), "virtualization"),
        (("linux", "systemd", "iptables", "nftables", "sshd"), "linux"),
        (("window", "active directory", "gpo", "powershell", "dns server"), "windows"),
        (("backup", "snapshot", "restore", "dr ", "rpo", "rto"), "backup"),
        (("sdn", "sd-wan", "overlay", "underlay", "controller"), "sdn"),
        (("fortigate", "fortinet", "fortios"), "fortigate"),
        (("pfsense", "opnsense"), "pfsense"),
    ]
    for keys, cat in rules:
        if any(k in t for k in keys):
            return cat
    return "general"

def _arch_for(topic: str, cat: str) -> str:
    tables = {
        "vlan": "Access / Trunk / Native / SVI — جداسازی L2 و gateway",
        "ospf": "Area / Neighbor / LSA / Cost — مسیریابی link-state",
        "bgp": "AS / eBGP-iBGP / prefix-list / route-map — سیاست مسیر",
        "nat": "Inside-Outside / PAT / Static — ترجمه آدرس",
        "dhcp": "DORA / Scope / Relay / Reservation",
        "dns": "Resolver / Auth Zone / Cache / TTL",
        "vpn": "Phase1-IKE / Phase2-IPsec / interesting traffic",
        "firewall": "Zone / Policy order / Stateful session / Log",
        "wireless": "SSID / AP-WLC / Auth (PSK/802.1X) / VLAN map",
        "tcpip": "L2 MAC / L3 IP / L4 port / ARP-ND",
        "mikrotik": "filter-nat-mangle / route / address-list",
        "stp": "Root / Root Port / Designated / Blocked / BPDU",
        "qos": "Classification / Marking / Queuing / Policing / Shaping",
        "ha": "Active-Standby / VIP / Hello / Preempt",
        "monitor": "Agent / SNMP trap / Syslog / Metrics / Alert",
        "automation": "Inventory / Playbook-Module / Idempotent / Drift",
        "cloud": "Region-VPC / SG-NACL / Route table / IAM",
        "security": "Identity / AuthN-AuthZ / Encryption / Audit",
        "storage": "Block-File-Object / LUN / Snapshot / Multipath",
        "virtualization": "Hypervisor / vSwitch / Overlay / Resource pool",
        "linux": "Kernel-Netfilter / iproute2 / systemd unit",
        "windows": "AD DS / DNS-DHCP role / GPO / Firewall profile",
        "backup": "Full-Inc-Diff / RPO-RTO / Offsite / Test restore",
        "sdn": "Control-Data plane / Overlay / Controller API",
        "fortigate": "VDOM / Policy / UTM / SD-WAN rule",
        "pfsense": "Interface / Rule / NAT / Package",
        "general": f"ورودی → پردازش «{topic}» → خروجی Verify",
    }
    return tables.get(cat, tables["general"])

def _focused_story(topic: str, cat: str) -> str:
    stories = {
        "vlan": f"«{topic}»: دو گروه کاربر روی یک سوئیچ؛ بدون VLAN ترافیک قاطی می‌شود.",
        "ospf": f"«{topic}»: چند لینک بین روترها؛ OSPF همسایه و بهترین Cost را می‌سازد.",
        "bgp": f"«{topic}»: مرز سازمان با ISP؛ BGP مسیر را با سیاست انتخاب می‌کند.",
        "monitor": f"«{topic}»: بدون مانیتورینگ فقط وقتی کاربر فریاد می‌زند می‌فهمی قطع شده.",
        "automation": f"«{topic}»: پیکربندی دستی روی ۲۰ دستگاه = خطای انسانی.",
        "security": f"«{topic}»: فایروال لازم است ولی بدون Identity و لاگ، RCA ناقص است.",
        "cloud": f"«{topic}»: در ابر مرز امنیتی SG/NACL است نه فقط کابل.",
        "backup": f"«{topic}»: Backup بدون تست Restore فقط حس امنیت کاذب است.",
    }
    return stories.get(cat, f"«{topic}» را در شبکه واقعی تصور کن: ورودی، پردازش، خروجی قابل اندازه‌گیری.")

def _steps_for(topic: str, cat: str) -> str:
    return f"""1. Baseline بگیر (وضعیت قبل از تغییر «{topic}»).
2. تغییر حداقلی و مستند اعمال کن.
3. Verify محلی و از دید کلاینت.
4. یک شکست عمدی مرتبط و RCA.
5. Rollback و مقایسه با Baseline."""

def _topic_commands(topic: str, cat: str) -> str:
    samples = {
        "vlan": "show vlan brief\nshow interfaces trunk\nshow interfaces switchport",
        "ospf": "show ip ospf neighbor\nshow ip route ospf\nshow ip ospf database",
        "bgp": "show ip bgp summary\nshow ip bgp\nshow ip route bgp",
        "nat": "show ip nat translations\nshow ip nat statistics",
        "dhcp": "show ip dhcp binding\nshow ip dhcp pool",
        "dns": "nslookup example.com\ndig example.com +short",
        "vpn": "show crypto isakmp sa\nshow crypto ipsec sa",
        "firewall": "show access-lists\nshow log | include deny",
        "mikrotik": "/ip firewall filter print stats\n/ip route print\n/interface print",
        "wireless": "show ap summary\nshow wireless client summary",
        "stp": "show spanning-tree\nshow spanning-tree root",
        "qos": "show policy-map interface\nshow queueing interface",
        "ha": "show standby\nshow vrrp\nshow track",
        "monitor": "snmpwalk -v2c -c public HOST system\ntail -f /var/log/syslog",
        "automation": "ansible all -m ping\nterraform plan",
        "cloud": "aws ec2 describe-instances\naz network vnet list",
        "security": "show aaa servers\nshow authentication sessions",
        "linux": "ip -br a\nss -tulpn\nnft list ruleset",
        "windows": "Get-NetIPConfiguration\nGet-NetFirewallProfile",
        "backup": "# verify last backup job + test restore path",
        "sdn": "show sdwan\n# controller API health",
        "fortigate": "get system status\ndiagnose sys session list",
        "pfsense": "# Status > System Logs > Firewall",
    }
    body = samples.get(cat, f"# دستورات مرتبط با {topic}\nshow running-config | include related")
    lines = [ln for ln in body.strip().splitlines() if ln.strip()]
    return "\n".join(f"```\n{ln}\n```" for ln in lines)

def _focused_lab(topic: str, cat: str, level: str) -> str:
    return f"""## Lab متمرکز — {topic} (سطح {level})

**هدف:** پیاده‌سازی و Verify فقط «{topic}».

| مرحله | کار | معیار موفقیت |
|-------|-----|----------------|
| 1 | Lab در GNS3/EVE/سخت‌افزار | توپولوژی بالا می‌آید |
| 2 | پیکربندی حداقلی «{topic}» | config ذخیره شد |
| 3 | دستورات Verify | خروجی با انتظار می‌خواند |
| 4 | یک خطا عمدی | RCA زیر ۱۵ دقیقه |
| 5 | Rollback | برگشت به Baseline |

**تحویل:** اسکرین‌شات Verify + ۳ خط یادداشت RCA.
"""

def _quiz_block(topic: str, cat: str) -> str:
    bank = {
        "vlan": [
            ("Native VLAN روی Trunk؟", "VLAN بدون تگ روی trunk", "VLAN مدیریتی همیشه", "VLAN مهمان", 0),
            ("SVI برای چیست؟", "Gateway لایه ۳ برای VLAN", "فقط مانیتورینگ", "جایگزین STP", 0),
        ],
        "ospf": [
            ("LSA نوع ۱؟", "Router LSA", "Summary", "External", 0),
            ("Area 0 نقش؟", "Backbone", "Stub فقط", "فقط BGP", 0),
        ],
        "bgp": [
            ("eBGP در برابر iBGP؟", "بین AS در برابر داخل AS", "سرعت بیشتر", "فقط IPv6", 0),
            ("Local Preference بالاتر؟", "ترجیح خروجی از آن مسیر", "حذف مسیر", "قطع همسایه", 0),
        ],
        "firewall": [
            ("ترتیب Policy؟", "اولین match برنده است", "آخرین همیشه", "تصادفی", 0),
            ("Stateful یعنی؟", "Session را به خاطر می‌سپارد", "فقط IP", "بدون لاگ", 0),
        ],
        "monitor": [
            ("Metric در برابر Log؟", "عدد پیوسته در برابر رویداد متنی", "یکی هستند", "فقط SNMP", 0),
            ("Alert بدون Baseline؟", "False positive زیاد", "دقیق‌تر", "نیازی نیست", 0),
        ],
        "security": [
            ("AAA یعنی؟", "Authentication Authorization Accounting", "فقط فایروال", "VPN", 0),
            ("802.1X کجا؟", "لبه دسترسی پورت/وایرلس", "فقط هسته", "فقط اینترنت", 0),
        ],
        "automation": [
            ("Idempotent؟", "تکرار نتیجه را خراب نمی‌کند", "فقط یک‌بار اجرا", "بدون لاگ", 0),
            ("Inventory؟", "فهرست میزبان‌ها و گروه‌ها", "رمز عبور", "لایسنس", 0),
        ],
        "backup": [
            ("RPO یعنی؟", "حداکثر داده قابل از دست رفتن", "زمان بازیابی", "حجم دیسک", 0),
            ("Backup بدون تست Restore؟", "اعتبار ندارد", "کافی است", "فقط برای لاگ", 0),
        ],
    }
    qs = bank.get(cat) or [
        (f"اولین قدم برای «{topic}»؟", "Baseline و Verify", "حذف همه ACL", "قطع اینترنت", 0),
        (f"Rollback برای «{topic}»؟", "برگشت امن بعد از تغییر بد", "فقط زیبایی", "نیازی نیست", 0),
        (f"RCA از کجا؟", "علائم + آخرین تغییر", "تعویض سخت‌افزار فوری", "نادیده گرفتن لاگ", 0),
    ]
    lines = [f"## آزمون سریع — {topic}\n"]
    for i, (q, a, b, c, ans) in enumerate(qs, 1):
        opts = [a, b, c]
        lines.append(f"**{i}. {q}**")
        for j, o in enumerate(opts):
            mark = "✓" if j == ans else "○"
            lines.append(f"- {mark} {o}")
        lines.append(f"  *پاسخ: {opts[ans]}*\n")
    return "\n".join(lines)

def _worked_example(topic: str, cat: str) -> str:
    examples = {
        "vlan": f"""### مثال عددی — {topic}
PC-A VLAN10=10.10.10.10/24 GW 10.10.10.1 | PC-B VLAN20=10.10.20.10/24
بدون روتر/SVI بین VLANها پینگ نمی‌شود.""",
        "ospf": f"""### مثال — {topic}
R1-R2 لینک 10.0.0.0/30 | شبکه 10.1.0.0/24 روی R1
network statements در area 0 → neighbor Full و route در جدول.""",
        "monitor": f"""### مثال — {topic}
اگر ICMP به GW سه بار fail شد Alert. Baseline latency ۲۰ms؛ آستانه ۱۰۰ms یا loss>۲٪.""",
        "backup": f"""### مثال — {topic}
RPO=۴ ساعت → Backup هر ۴ ساعت. RTO=۱ ساعت → Restore زیر ۶۰ دقیقه تست شود.""",
    }
    return examples.get(cat, f"""### مثال عملی — {topic}
دفتر ۲۰ نفره. «{topic}» را طوری پیاده کن که کلاینت تست قبل/بعد را مقایسه کند.
معیار: دستور Verify + نتیجه کلاینت.""")

def build_deep_fallback(title_fa: str, title_en: str = "", level: str | None = None) -> Dict[str, Any]:
    level = level or level_tag(title_fa)
    topic = clean_topic(title_fa)
    cat = _cat_for(topic)
    spec = {"extra_full": "", "extra_commands": "", "extra_lab": "", "extra_notes": ""}
    try:
        from core.specialized_depth import specialized_block, detect_specialty
        if detect_specialty(title_fa, title_en):
            spec = specialized_block(title_fa, title_en, level) or spec
    except Exception:
        pass

    summary = (
        f"«{topic}» — سطح {level}. "
        f"معماری، جریان عملی، دستور Verify، Lab و آزمون کوتاه."
    )
    quiz = _quiz_block(topic, cat)
    example = _worked_example(topic, cat)
    lab = _focused_lab(topic, cat, level)
    info = spec.get("extra_full") or ""

    full = f"""# {topic}

**سطح:** {level} · **دسته:** {cat}

## تصویر ذهنی
{_focused_story(topic, cat)}

## معماری مرتبط
{_arch_for(topic, cat)}

## جریان عملی
{_steps_for(topic, cat)}
{info}

## مثال حل‌شده
{example}

## جمع‌بندی
«{topic}» را وقتی بلدی که بتوانی Verify، RCA و Rollback کنی.
"""

    notes = f"""## نکات RCA — {topic}

1. آخرین تغییر مرتبط چه بود؟
2. Verify محلی OK است یا از کلاینت هم؟
3. همیشگی است یا بعد از رویداد خاص؟
4. لاگ/Alarm چه می‌گوید؟

{quiz}
""" + (spec.get("extra_notes") or "")

    return {
        "summary": summary,
        "full_content": full,
        "commands": _topic_commands(topic, cat) + ("\n" + (spec.get("extra_commands") or "")),
        "examples": lab + "\n\n" + example + ("\n\n" + (spec.get("extra_lab") or "")),
        "notes": notes,
        "level": level,
        "topic": topic,
        "category": cat,
    }
