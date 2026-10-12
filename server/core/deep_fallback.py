# -*- coding: utf-8 -*-
"""موتور محتوای عمیق — با اینفوگرافیک و تشبیه وابسته به دسته (کم‌تکرارتر)."""
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
        "vlan": f"در یک سازمان دو دپارتمان روی یک سوئیچ هستند. بدون جداسازی «{topic}»، broadcast و حتی ترافیک حساس بین آن‌ها قاطی می‌شود و عیب‌یابی کابوس می‌شود.",
        "ospf": f"لینک اصلی بین دو سایت قطع شده. اگر «{topic}» درست باشد مسیر پشتیبان باید ظرف ثانیه‌ها جایگزین شود؛ وگرنه شعبه از مرکز جدا می‌ماند.",
        "bgp": f"دو ISP دارید. بدون سیاست درست «{topic}» یا ترافیک از لینک گران می‌رود یا هنگام قطعی یکی از ISPها blackhole می‌گیرید.",
        "nat": f"سرور داخلی باید از بیرون دیده شود. اشتباه در «{topic}» یا همه اینترنت را به داخل باز می‌کند یا سرویس از بیرون timeout می‌دهد.",
        "wireless": f"کاربران در راهرو وای‌فای دارند ولی در اتاق جلسه قطع می‌شود. «{topic}» را باید از قدرت سیگنال تا DHCP و gateway جداگانه ایزوله کنید.",
        "tcpip": f"پینگ جواب می‌دهد ولی اپلیکیشن نه. بدون فهم «{topic}» بین لایه ۳ و ۴ گیر می‌کنید و زمان را روی کابل تلف می‌کنید.",
    }
    return stories.get(
        cat,
        f"گزارش NOC: سرویس مرتبط با «{topic}» ناپایدار است. باید از لایه فیزیکی تا اپلیکیشن ایزوله کنید، "
        f"شواهد با دستور جمع کنید و با حداقل قطعی رفع نمایید — نه حدس زدن.",
    )


def _arch_table(cat: str) -> str:
    tables = {
        "vlan": "| جزء | نقش |\n|-----|-----|\n| Access Port | یک VLAN به کلاینت |\n| Trunk | چند VLAN با تگ 802.1Q |\n| Native VLAN | بدون تگ روی trunk |\n| SVI | gateway لایه ۳ همان VLAN |",
        "stp": "| جزء | نقش |\n|-----|-----|\n| Root Bridge | مرجع توپولوژی |\n| Root Port | نزدیک‌ترین به Root |\n| Designated Port | مسئول سگمنت |\n| Blocking | جلوگیری از loop |\n| BPDU | سیگنال کنترل |",
        "ospf": "| جزء | نقش |\n|-----|-----|\n| Area 0 | Backbone |\n| Neighbor | adjacency |\n| LSA | تبلیغ توپولوژی |\n| DR/BDR | کاهش flooding |\n| Cost | معیار مسیر |",
        "bgp": "| جزء | نقش |\n|-----|-----|\n| AS | دامنه سیاست |\n| eBGP / iBGP | بین/داخل AS |\n| Prefix-list | فیلتر پیشوند |\n| Route-map | سیاست |\n| Next-hop | مقصد بعدی |",
        "dhcp": "| جزء | نقش |\n|-----|-----|\n| DORA | Discover→Offer→Request→Ack |\n| Scope | محدوده آدرس |\n| Relay | عبور بین VLAN |\n| Reservation | آدرس ثابت |\n| Lease | مدت اعتبار |",
        "dns": "| جزء | نقش |\n|-----|-----|\n| Resolver | کلاینت پرسشگر |\n| Recursive | جستجوی کامل |\n| Authoritative | منبع zone |\n| Forwarder | هدایت بالادست |\n| Cache + TTL | سرعت پاسخ |",
        "vpn": "| جزء | نقش |\n|-----|-----|\n| Phase 1 (IKE) | کانال کنترل |\n| Phase 2 (IPsec) | تونل داده |\n| SA | Association |\n| PSK/Cert | احراز |\n| PFS | Forward Secrecy |",
        "firewall": "| جزء | نقش |\n|-----|-----|\n| Zone | گروه‌بندی |\n| Policy | قانون عبور |\n| NAT | ترجمه آدرس |\n| Session | وضعیت اتصال |\n| Log | ثبت رویداد |",
        "wireless": "| جزء | نقش |\n|-----|-----|\n| SSID | نام شبکه |\n| AP | رادیو لبه |\n| WLC | کنترلر مرکزی |\n| CAPWAP | تونل AP↔WLC |\n| Roaming | جابجایی بدون قطع IP |",
        "tcpip": "| جزء | نقش |\n|-----|-----|\n| IP | آدرس منطقی |\n| TCP | اتصال قابل اعتماد |\n| UDP | سبک بدون اتصال |\n| ARP | IP→MAC |\n| ICMP | پیام کنترل/خطا |",
    }
    return tables.get(
        cat,
        "| جزء | نقش |\n|-----|-----|\n| Control plane | تصمیم و سیگنالینگ |\n| Data plane | عبور ترافیک |\n| Management | پیکربندی و لاگ |\n| Policy / AAA | مجوز |",
    )


def _frame_steps(cat: str) -> str:
    steps = {
        "vlan": "1. کلاینت فریم می‌فرستد\n2. سوئیچ VLAN را از پورت access می‌فهمد\n3. روی trunk تگ 802.1Q می‌خورد\n4. مقصد در همان VLAN → forward؛ وگرنه drop یا به L3\n5. SVI اگر gateway باشد ARP و route",
        "ospf": "1. Hello برای کشف همسایه\n2. تبادل DBD / LSA\n3. ساخت LSDB یکسان در Area\n4. SPF → جدول مسیریابی\n5. تغییر لینک → LSA جدید و محاسبه مجدد",
        "bgp": "1. TCP 179 و Open\n2. تبادل UPDATE (prefix + attributes)\n3. Best path selection\n4. نصب در RIB/FIB در صورت مجاز\n5. سیاست با prefix-list/route-map",
        "nat": "1. پکت از داخل با IP خصوصی\n2. مطابقت با rule NAT\n3. بازنویسی Src/Dst و ذخیره در جدول\n4. ارسال به WAN\n5. پاسخ با ترجمه معکوس",
        "dhcp": "1. Discover (broadcast)\n2. Offer\n3. Request\n4. Ack + Lease\n5. Renewal در ۵۰٪ و ۸۷٫۵٪",
        "dns": "1. پرسش به Resolver\n2. Cache یا Recursive\n3. Root → TLD → Authoritative\n4. پاسخ + TTL\n5. Split-Horizon در صورت سیاست",
        "vpn": "1. IKE Phase1\n2. IKE Phase2 / IPsec SA\n3. Interesting traffic\n4. Encrypt + ارسال\n5. DPD/Keepalive",
        "wireless": "1. Probe / Association\n2. 802.1X یا PSK\n3. کلیدهای نشست WPA\n4. DHCP روی SSID/VLAN\n5. ترافیک از AP به سوئیچ/WLC",
        "tcpip": "1. App داده می‌دهد\n2. TCP/UDP هدر و پورت\n3. IP Src/Dst + TTL\n4. فریم Ethernet با MAC\n5. روی مدیوم فیزیکی",
        "stp": "1. انتخاب Root\n2. محاسبه Root Port / Designated\n3. Blocking پورت‌های اضافی\n4. BPDU دوره‌ای\n5. شکست لینک → همگرایی مجدد",
    }
    return steps.get(
        cat,
        "1. Backup\n2. دامنه تغییر\n3. پیکربندی حداقلی\n4. Verify محلی\n5. Verify End-to-End\n6. لاگ\n7. Rollback در صورت شکست",
    )


def _lab_concrete(topic: str, cat: str, level: str) -> str:
    base = f"""# آزمایشگاه عملی — {topic}

## توپولوژی
- حداقل: ۲ کلاینت + ۱ سوئیچ + ۱ روتر (یا EVE-NG / GNS3 / Packet Tracer)
- یک uplink و در صورت امکان یک مسیر backup

## مراحل

### ۱) Baseline
| مورد | قبل از تغییر | دستور |
|------|-------------|--------|
| اینترفیس | | `show ip interface brief` / `ip -br a` |
| مسیر / جدول | | وابسته به «{topic}» |
| لاگ | | `show logging` / `journalctl -n 50` |

### ۲) Backup
```
copy running-config startup-config
show running-config | redirect flash:pre-lab.cfg
```

### ۳) تغییر حداقلی مرتبط با «{topic}» سپس Verify
- [ ] Verify روی دستگاه
- [ ] Verify از کلاینت (ping / curl / nslookup)
- [ ] بدون خطای جدید در لاگ

### ۴) Failure Injection
عمداً یک مورد را بشکن (کابل، VLAN اشتباه، ACL deny) و با RCA پیدا کن.

### ۵) Rollback نوشته‌شده را اجرا کن
"""
    if level in ("L3", "L4"):
        base += f"""
### ۶) سطح {level}
- پنجره Change و اطلاع‌رسانی
- Runbook یک‌صفحه
- مانیتور حداقل ۳۰ دقیقه بعد از apply
"""
    return base


def _rca_table(cat: str) -> str:
    rows = ERRORS.get(cat, [
        ("سرویس قطع", "فیزیکی / gateway", "show interface / ping gateway"),
        ("فقط بعضی کلاینت‌ها", "VLAN / ACL / DNS", "مقایسه کلاینت خوب و بد"),
        ("کندی", "duplex / congestion / DNS", "interface counters / dig"),
    ])
    lines = ["| علامت | علت محتمل | دستور اول |", "|--------|-----------|-----------|"]
    for a, b, c in rows[:6]:
        lines.append(f"| {a} | {b} | `{c}` |")
    return "\n".join(lines)


def _security_block(cat: str, level: str) -> str:
    common = (
        "- حداقل دسترسی مدیریت (AAA، SSH key، غیرفعال کردن Telnet)\n"
        "- تغییر فقط با Backup و Rollback\n"
        "- جداسازی Management از User VLAN\n"
    )
    extra = {
        "vlan": "- Native VLAN غیرپیش‌فرض\n- Prune VLANهای بلااستفاده روی trunk",
        "stp": "- BPDU Guard روی access\n- Root Guard روی لبه",
        "dhcp": "- DHCP Snooping\n- Trust فقط uplink سرور",
        "wireless": "- WPA3/WPA2-Enterprise در صورت امکان\n- جداسازی Guest",
        "firewall": "- Default deny\n- Policy از خاص به عام",
        "vpn": "- AES-GCM / SHA2\n- PFS",
    }
    return common + extra.get(cat, "")


def _level_guidance(level: str) -> str:
    return {
        "L0": "تصویر ذهنی و تشبیه؛ هنوز حفظ دستور لازم نیست.",
        "L1": "مشاهده + Lab ساده؛ خروجی show را بخوان.",
        "L2": "پیکربندی + Verify + Rollback.",
        "L3": "طراحی چندسگمنت و RCA سیستماتیک.",
        "L4": "معماری سازمانی، Change Control، Runbook.",
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
    analogy = _ANALOGY.get(cat, f"«{topic}» قطعه‌ای از زنجیره تحویل سرویس است؛ اگر اینجا بشکند، علامت ممکن است جای دیگر دیده شود.")

    try:
        from core.infographics import markdown_block

        info = markdown_block(cat)
    except Exception:
        info = ""

    summary = (
        f"«{topic}» ({level_fa}). "
        f"تمرکز این درس: جریان واقعی ترافیک، نقاط شکست، Verify و Rollback — نه تکرار شعار کلی."
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
                    ("show running-config | redirect flash:pre-change.cfg", "بک‌آپ قبل تغییر"),
                    ("copy running-config startup-config", "ذخیره پس از Verify"),
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

## تشبیه مخصوص این دسته

{analogy}

---

## معماری اجزا

{_arch_table(cat)}

---

## جریان گام‌به‌گام

{_frame_steps(cat)}
{info}
---

## سطح تو ({level})

{_level_guidance(level)}

---

## امنیت مرتبط

{_security_block(cat, level)}

---

## RCA سریع

{_rca_table(cat)}

مسیر: Symptom → Scope → Evidence → Hypothesis → Test → Fix → Verify → Document

---

## چک‌لیست قبل از Production

- [ ] Backup و مسیر Rollback
- [ ] دامنه تغییر مشخص
- [ ] Verify محلی و End-to-End
- [ ] مانیتور بعد از change

---

## جمع‌بندی

از این درس سه چیز ببر:
1. اولین دستورات Verify برای «{topic}»
2. نقطه شکست رایج در دسته {cat}
3. مسیر Rollback
"""

    return {
        "summary": summary,
        "full_content": full,
        "commands": commands,
        "examples": _lab_concrete(topic, cat, level),
        "notes": f"## RCA — {topic}\n\n{_rca_table(cat)}\n\n{_level_guidance(level)}\n",
        "level": level,
        "topic": topic,
        "category": cat,
    }
