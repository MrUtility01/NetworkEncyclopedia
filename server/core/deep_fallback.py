# -*- coding: utf-8 -*-
"""محتوای عمیق سطح‌بندی‌شده (L0→L4) برای درس‌های بدون teacher اختصاصی."""
from __future__ import annotations
import re
from typing import Any, Dict, List, Tuple

def level_tag(title: str) -> str:
    m = re.match(r"\[(L[0-4])\]", title or "")
    return m.group(1) if m else "L0"

def clean_topic(title: str) -> str:
    t = re.sub(r"^\[L[0-4]\]\s*", "", title or "").strip()
    t = re.sub(r"\s*[—\-]\s*(آشنایی|مقدماتی|ادمین|مهندس|خبره).*$", "", t, flags=re.I)
    return t.strip() or (title or "موضوع")

def _cat_for(topic: str) -> str:
    t = (topic or "").lower()
    rules: List[Tuple[Tuple[str, ...], str]] = [
        (("vlan", "trunk", "svi", "access port", "private vlan"), "vlan"),
        (("ospf", "lsa", "area 0", "neighbor ospf", "dr/bdr"), "ospf"),
        (("bgp", "as number", "prefix-list", "route-map", "as-path"), "bgp"),
        (("nat", "pat", "masquerade", "source nat", "destination nat"), "nat"),
        (("dhcp", "dora", "lease", "relay agent", "snooping"), "dhcp"),
        (("dns", "resolver", "zone", "record a", "doh", "dot"), "dns"),
        (("vpn", "ipsec", "tunnel", "phase1", "phase2", "wireguard", "openvpn", "gre"), "vpn"),
        (("firewall", "acl", "policy", "filter", "ids", "ips", "waf"), "firewall"),
        (("wireless", "wifi", "ssid", "wpa", "802.11", "wlc", "capwap"), "wireless"),
        (("tcp", "udp", "arp", "icmp", "mtu", "mss", "ecn"), "tcpip"),
        (("mikrotik", "routeros", "winbox"), "mikrotik"),
        (("stp", "rstp", "mstp", "bpdu", "root bridge", "loop guard"), "stp"),
        (("qos", "queue", "dscp", "policer", "shaper", "cbwfq"), "qos"),
        (("ha", "hsrp", "vrrp", "glbp", "failover", "cluster"), "ha"),
        (("monitor", "snmp", "syslog", "netflow", "prometheus", "grafana", "zabbix", "telemetry"), "monitor"),
        (("automat", "ansible", "terraform", "python net", "api rest", "netconf", "napalm"), "automation"),
        (("cloud", "aws", "azure", "gcp", "vpc", "s3", "tgw"), "cloud"),
        (("security", "aaa", "radius", "tacacs", "802.1x", "zero trust", "pki", "hardening"), "security"),
        (("storage", "san", "nas", "iscsi", "nfs", "smb"), "storage"),
        (("virtual", "vmware", "hyper-v", "kvm", "docker", "kubernet", "overlay"), "virtualization"),
        (("linux", "systemd", "iptables", "nftables", "sshd", "iproute"), "linux"),
        (("window", "active directory", "gpo", "powershell", "dns server"), "windows"),
        (("backup", "snapshot", "restore", "dr ", "rpo", "rto"), "backup"),
        (("sdn", "sd-wan", "overlay", "underlay", "controller", "vxlan"), "sdn"),
        (("fortigate", "fortinet", "fortios"), "fortigate"),
        (("pfsense", "opnsense"), "pfsense"),
        (("mpls", "label", "l3vpn", "l2vpn", "vrf"), "mpls"),
        (("ipv6", "slaac", "ndp", "ra ", "dad"), "ipv6"),
    ]
    for keys, cat in rules:
        if any(k in t for k in keys):
            return cat
    return "general"

def _level_depth(level: str) -> str:
    return {
        "L0": "آشنایی — مفهوم و تصویر ذهنی",
        "L1": "مقدماتی — پیکربندی ساده و Verify",
        "L2": "ادمین — طراحی چنددستگاهی و عیب‌یابی",
        "L3": "مهندس — مقیاس سازمانی و Failure Domain",
        "L4": "خبره — تصمیم معماری، Trade-off و مصاحبه فنی",
    }.get(level, "عمومی")

def _arch_for(topic: str, cat: str) -> str:
    tables = {
        "vlan": "Access / Trunk / Native / SVI / Inter-VLAN Routing",
        "ospf": "Area / Neighbor FSM / LSA Types / Cost / DR-BDR",
        "bgp": "AS / eBGP-iBGP / NLRI / Attributes / Policy",
        "nat": "Inside-Outside / Static / Dynamic / PAT / Twice NAT",
        "dhcp": "DORA / Scope / Relay / Reservation / Snooping",
        "dns": "Stub-Resolver / Auth Zone / Cache / TTL / DNSSEC",
        "vpn": "IKE Phase1 / IPsec Phase2 / Interesting Traffic / SA",
        "firewall": "Zone / Policy order / Stateful / NAT / Log",
        "wireless": "SSID / AP-WLC / 802.1X/PSK / VLAN map / Roaming",
        "tcpip": "Ethernet / IP / TCP-UDP / ARP-ND / Path MTU",
        "mikrotik": "filter / nat / mangle / raw / route / queue",
        "stp": "Root / RP / DP / Alternate / BPDU Guard-Filter",
        "qos": "Classify / Mark / Queue / Police / Shape",
        "ha": "VIP / Active-Standby / Hello / Preempt / Track",
        "monitor": "Metric / Log / Trace / Alert / Baseline",
        "automation": "Inventory / Module / Idempotent / CI / Drift",
        "cloud": "VPC / Subnet / SG-NACL / RT / IAM / Edge",
        "security": "Identity / AuthZ / Encrypt / Segment / Audit",
        "backup": "Full-Inc / Snapshot / RPO-RTO / Offsite / Test",
        "sdn": "Control / Data / Overlay / Underlay / Policy",
        "mpls": "Label / LFIB / VRF / PE-CE / LDP-RSVP",
        "ipv6": "Global / Link-Local / RA / SLAAC / DHCPv6",
        "general": f"ورودی → پردازش «{topic}» → خروجی قابل Verify",
    }
    return tables.get(cat, tables["general"])

def _progressive_body(topic: str, cat: str, level: str) -> str:
    L = level or "L0"
    parts: List[str] = []
    parts.append(f"""## ۱) چرا «{topic}» مهم است؟

در شبکه واقعی، «{topic}» نقطه‌ای است که اگر اشتباه پیکربندی شود، سرویس قطع می‌شود یا عیب‌یابی ساعت‌ها طول می‌کشد.
قبل از config این سه سؤال را جواب بده:
1. **دامنه اثر** چیست؟ (یک پورت، یک VLAN، کل سایت)
2. **معیار موفقیت** چیست؟ (پینگ، نام، Session، Metric)
3. **Rollback** چطور است؟ (کپی running، checkpoint)
""")
    parts.append(f"""## ۲) معماری مرتبط

{_arch_for(topic, cat)}

توپولوژی مرجع:
`Client → Access → Distribution/Core → Edge/FW → WAN/Internet`
«{topic}» معمولاً در یکی از این لایه‌ها متمرکز است.
""")
    parts.append(f"""## ۳) مفهوم به زبان ساده (پایه)

فرض کن یک دفتر کوچک داری. «{topic}» مثل یک **قانون مشخص** است:
- بدون قانون → هرج‌ومرج
- قانون بیش‌ازحد پیچیده → کسی جرأت تغییر ندارد

در سطح آشنایی بدان:
- ورودی‌اش چیست؟
- چه چیزی را جدا / وصل / محدود / مشاهده می‌کند؟
- با کدام دستور ساده می‌فهمی کار می‌کند؟

### واژه‌های کلیدی
- **Interface / Port / SSID** — نقطه اتصال
- **Policy / ACL / Route** — تصمیم‌گیری
- **State / Session / Neighbor** — زنده‌بودن
- **Log / Counter / Metric** — شواهد Verify
""")
    if L in ("L1", "L2", "L3", "L4"):
        parts.append(f"""## ۴) پیکربندی حداقلی و Verify

الگوی استاندارد برای «{topic}»:

```
1) Baseline: show / log قبل از تغییر
2) Config حداقلی فقط برای همین موضوع
3) Verify محلی روی دستگاه
4) Verify از دید کلاینت
5) ذخیره فقط بعد از موفقیت
```

| چک | انتظار |
|----|--------|
| وضعیت سرویس/پروتکل | up / established |
| مسیر یا Policy | در جدول دیده شود |
| تست کلاینت | پایدار |
| لاگ خطا | بدون deny غیرمنتظره |
""")
    if L in ("L2", "L3", "L4"):
        parts.append(f"""## ۵) طراحی چنددستگاهی و عیب‌یابی (ادمین+)

### ماتریس عیب‌یابی سریع
| علامت | احتمال نزدیک | اقدام اول |
|-------|---------------|-----------|
| کلاینت IP ندارد | DHCP / VLAN / Port | interface + scope |
| IP دارد اینترنت ندارد | GW / NAT / DNS / Policy | پینگ GW → 1.1.1.1 → نام |
| بعضی VLANها OK | Trunk / Allowed / SVI | show trunk / svi |
| قطعی متناوب | STP / Duplex / HA | log + errdisable |
| بعد از تغییر خراب شد | آخرین change | diff / rollback |

### قوانین RCA برای «{topic}»
1. **یک متغیر** را عوض کن.
2. از **لبه نزدیک کاربر** شروع کن.
3. **زمان‌بندی** علامت‌ها را با پنجره تغییر‌ها تطبیق بده.
""")
    if L in ("L3", "L4"):
        parts.append(f"""## ۶) مقیاس سازمانی و Failure Domain (مهندس)

«{topic}» نباید Single Point of Failure پنهان بسازد.

**سؤالات طراحی**
- اگر از کار بیفتد، شعاع خرابی چند کاربر/سایت است؟
- Redundancy Active-Standby یا Active-Active؟
- تغییر سایت A روی سایت B اثر دارد؟ (Shared fate)

**الگوی پیشنهادی**
- جداسازی Control و Data
- محدودیت دامنه (Area / Zone / VRF)
- Observability: Metric + Log + Synthetic test
""")
    if L == "L4":
        parts.append(f"""## ۷) سطح خبره — Trade-off و مصاحبه فنی

### Trade-offها
| انتخاب | سود | هزینه |
|--------|-----|-------|
| سادگی عملیاتی | خطای انسانی کمتر | انعطاف کمتر |
| Policy زیاد | دقت/امنیت | پیچیدگی |
| Vendor واحد | یکپارچگی | lock-in |
| اتوماسیون کامل | تکرارپذیری | هزینه اولیه |

### سؤالات مصاحبه
1. «{topic}» را در ۲ دیتاسنتر با لینک نابرابر چطور طراحی می‌کنی؟
2. چه Metricهایی برای SLO تعریف می‌کنی؟
3. یک رخداد واقعی RCA که به «{topic}» ختم شد را شرح بده.
""")
    parts.append(f"""## ۸) مثال حل‌شده

**سناریو:** دفتر ۴۰ نفره + سرور داخلی + اینترنت روی Edge.

هدف مرتبط با «{topic}»:
- Users به اینترنت
- Servers فقط پورت‌های لازم
- تغییر بدون قطعی کامل

**مراحل**
1. Baseline از Edge و Access
2. تغییر در پنجره نگهداری
3. کلاینت تست: DHCP → GW → DNS → HTTPS
4. لاگ Edge برای deny جدید
5. ثبت خروجی Verify
""")
    parts.append(f"""## ۹) جمع‌بندی پیش‌رونده

| سطح | باید بتوانی |
|-----|-------------|
| L0 | مفهوم را با مثال بگویی |
| L1 | Config ساده و Verify |
| L2 | عیب‌یابی چند دستگاه |
| L3 | Failure Domain و مقیاس |
| L4 | Trade-off و مصاحبه فنی |

**سطح فعلی این درس:** {_level_depth(L)}
""")
    return "\n".join(parts)

def _topic_commands(topic: str, cat: str, level: str) -> str:
    base = {
        "vlan": ["show vlan brief", "show interfaces trunk", "show interfaces switchport", "show ip interface brief"],
        "ospf": ["show ip ospf neighbor", "show ip route ospf", "show ip ospf database", "show ip ospf interface"],
        "bgp": ["show ip bgp summary", "show ip bgp", "show ip route bgp", "show bgp ipv4 unicast neighbors"],
        "nat": ["show ip nat translations", "show ip nat statistics", "show run | section nat"],
        "dhcp": ["show ip dhcp binding", "show ip dhcp pool", "show ip dhcp conflict"],
        "dns": ["nslookup example.com", "dig example.com +short", "resolvectl status"],
        "vpn": ["show crypto isakmp sa", "show crypto ipsec sa", "show run | section crypto"],
        "firewall": ["show access-lists", "show log | include deny", "show zone-pair security"],
        "mikrotik": ["/ip firewall filter print stats", "/ip route print", "/interface print", "/log print"],
        "wireless": ["show ap summary", "show wireless client summary", "show wlan summary"],
        "stp": ["show spanning-tree", "show spanning-tree root", "show spanning-tree inconsistentports"],
        "qos": ["show policy-map interface", "show queueing interface"],
        "ha": ["show standby brief", "show vrrp", "show track"],
        "monitor": ["snmpwalk -v2c -c public HOST system", "tail -f /var/log/syslog", "show logging | last 50"],
        "automation": ["ansible all -m ping", "terraform plan", "napalm --help"],
        "security": ["show aaa servers", "show authentication sessions", "show run | section radius"],
        "linux": ["ip -br a", "ss -tulpn", "nft list ruleset", "journalctl -u NetworkManager -n 50"],
        "sdn": ["show sdwan", "show control connections", "show omp peers"],
        "fortigate": ["get system status", "diagnose sys session list", "show firewall policy"],
        "ipv6": ["show ipv6 interface brief", "show ipv6 route", "show ipv6 neighbors"],
        "mpls": ["show mpls ldp neighbor", "show mpls forwarding-table", "show vrf"],
    }
    lines = base.get(cat, [f"show running-config | include {topic[:24]}", "show logging | last 30"])
    if level in ("L3", "L4"):
        lines = lines + ["# packet-capture / debug فقط در lab با برنامه rollback"]
    return "\n".join(f"```\n{ln}\n```" for ln in lines)

def _focused_lab(topic: str, cat: str, level: str) -> str:
    extra = ""
    if level in ("L2", "L3", "L4"):
        extra = f"""
### سناریوی خراب‌کاری عمدی
1. یک تنظیم حیاتی «{topic}» را عمداً اشتباه کن
2. با ماتریس عیب‌یابی علت را پیدا کن
3. Rollback تمیز انجام بده
"""
    if level in ("L3", "L4"):
        extra += f"""
### سناریوی مقیاس
- دو سایت (HQ / Branch) برای «{topic}» طراحی کن
- Shared Fate را مشخص کن
- یک تست Failover بنویس
"""
    return f"""## Lab — {topic} ({_level_depth(level)})

| مرحله | کار | معیار |
|-------|-----|-------|
| 1 | توپولوژی Lab | لینک‌ها up |
| 2 | Config «{topic}» | ذخیره شد |
| 3 | Verify دستگاه | مطابق انتظار |
| 4 | Verify کلاینت | سرویس پایدار |
| 5 | مستندسازی | ۳ خط + اسکرین |
{extra}
"""

def _quiz_block(topic: str, cat: str, level: str) -> str:
    common = [
        (f"اولین قدم برای «{topic}»؟", "Baseline و معیار موفقیت", "حذف همه ACLها", "قطع اینترنت سازمان", 0),
        (f"Verify خوب؟", "دستگاه + کلاینت", "فقط LED", "فقط حس تکنسین", 0),
        (f"بعد از تغییر خراب شد؟", "آخرین change محور RCA", "ریبوت همه", "نادیده بگیر", 0),
    ]
    advanced = [
        (f"Failure Domain یعنی؟", "شعاع خرابی در صورت ازکارافتادن", "سرعت پورت", "برند دستگاه", 0),
        (f"سطح مهندس چه اضافه می‌کند؟", "مقیاس، افزونگی، Observability", "رنگ کابل", "حذف مستندات", 0),
    ]
    qs = common + (advanced if level in ("L3", "L4") else [])
    lines = [f"## آزمون — {topic} ({level})\n"]
    for i, (q, a, b, c, ans) in enumerate(qs, 1):
        opts = [a, b, c]
        lines.append(f"**{i}. {q}**")
        for j, o in enumerate(opts):
            lines.append(f"- {'✓' if j == ans else '○'} {o}")
        lines.append(f"  *پاسخ: {opts[ans]}*\n")
    return "\n".join(lines)

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

    body = _progressive_body(topic, cat, level)
    if spec.get("extra_full"):
        body += "\n\n## عمق تخصصی\n" + spec["extra_full"]

    summary = (
        f"«{topic}» | {level} — {_level_depth(level)}. "
        f"از مفهوم تا Verify، Lab، RCA و (سطوح بالاتر) مقیاس و Trade-off."
    )
    notes = f"""## RCA و آزمون — {topic}

### مسیر RCA
1. علامت دقیق (چه کسی، کی، کجا)
2. آخرین تغییر مرتبط
3. Verify لایه به لایه
4. یک فرضیه، یک تست
5. Monitoring بعد از رفع

{_quiz_block(topic, cat, level)}
""" + (spec.get("extra_notes") or "")

    examples = _focused_lab(topic, cat, level)
    if spec.get("extra_lab"):
        examples += "\n\n" + spec["extra_lab"]

    commands = _topic_commands(topic, cat, level)
    if spec.get("extra_commands"):
        commands += "\n" + spec["extra_commands"]

    return {
        "summary": summary,
        "full_content": body,
        "commands": commands,
        "examples": examples,
        "notes": notes,
        "level": level,
        "topic": topic,
        "category": cat,
    }
