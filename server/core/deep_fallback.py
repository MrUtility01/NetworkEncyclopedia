# -*- coding: utf-8 -*-
"""موتور محتوای عمیق و ملموس برای هر درسی که teacher اختصاصی ندارد.
هر درس شامل: داستان واقعی سازمانی، معماری، فریم‌به‌فریم، دستورات چندوندر،
Lab عملی، جدول RCA، امنیت، چک‌لیست Production و جمع‌بندی استاد.
"""
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
    ("tcpip", ["tcp", "udp", "icmp", "handshake", "window", "retransmission"]),
    ("mpls", ["mpls", "ldp", "label", "vrf", "l3vpn", "pe ", "ce "]),
    ("multicast", ["multicast", "pim", "igmp", "ssm", "rendezvous"]),
    ("vxlan", ["vxlan", "vni", "vtep", "evpn", "overlay", "underlay"]),
    ("sql", ["sql", "postgres", "mysql", "elasticsearch"]),
    ("python", ["python", "paramiko", "netmiko", "scrapli"]),
    ("ansible", ["ansible", "playbook", "inventory"]),
    ("terraform", ["terraform", "iac", "provider"]),
]


def _level(title: str) -> str:
    m = re.match(r"\[(L[0-4])\]", title or "")
    return m.group(1) if m else "L0"


def _topic(title: str) -> str:
    t = re.sub(r"^\[L[0-4]\]\s*", "", title or "").strip()
    t = re.sub(
        r"\s*[—\-]\s*(آشنایی|مقدماتی|ادمین|مهندس|خبره|Intro|Junior|Admin|Senior|Architect).*$",
        "",
        t,
        flags=re.I,
    )
    return t.strip() or (title or "موضوع")


def _cat(topic: str) -> str:
    t = topic.lower()
    for c, keys in _CATS:
        if any(k in t for k in keys):
            return c
    return "general"


def _fmt(pairs: List[Tuple[str, str]]) -> str:
    return "\n".join(f"```\n{cmd}\n```\n→ {desc}\n" for cmd, desc in pairs)


def _story(topic: str, cat: str) -> str:
    hooks = SCENARIO_HOOKS.get(cat, SCENARIO_HOOKS.get("general", []))
    if hooks:
        return hooks[0]
    return (
        f"سازمانی با چند سایت و حدود ۸۰۰ کاربر. تیم NOC گزارش می‌دهد که "
        f"«{topic}» باعث کندی یا قطع سرویس حیاتی شده. شما به عنوان مهندس شبکه "
        f"باید از لایه ۱ تا ۷ ایزوله کنید، شواهد جمع کنید و با حداقل قطعی رفع کنید."
    )


def _arch_table(cat: str) -> str:
    tables = {
        "vlan": "| جزء | نقش |\n|-----|-----|\n| Access Port | یک VLAN به کلاینت |\n| Trunk | چند VLAN با تگ 802.1Q |\n| Native VLAN | بدون تگ روی trunk |\n| SVI | gateway لایه ۳ همان VLAN |\n| VTP/Manual | توزیع یا مدیریت محلی VLAN |",
        "stp": "| جزء | نقش |\n|-----|-----|\n| Root Bridge | مرجع توپولوژی |\n| Root Port | نزدیک‌ترین به Root |\n| Designated Port | مسئول سگمنت |\n| Blocking/Alternate | جلوگیری از loop |\n| BPDU | سیگنال کنترل |",
        "ospf": "| جزء | نقش |\n|-----|-----|\n| Area 0 | Backbone |\n| Neighbor | adjacency |\n| LSA | تبلیغ توپولوژی |\n| DR/BDR | کاهش flooding در multi-access |\n| Cost | معیار مسیر |",
        "bgp": "| جزء | نقش |\n|-----|-----|\n| AS | دامنه سیاست |\n| eBGP / iBGP | بین/داخل AS |\n| Prefix-list | فیلتر پیشوند |\n| Route-map | سیاست |\n| Next-hop | مقصد بعدی |",
        "dhcp": "| جزء | نقش |\n|-----|-----|\n| DORA | Discover→Offer→Request→Ack |\n| Scope | محدوده آدرس |\n| Relay | عبور درخواست بین VLAN |\n| Reservation | آدرس ثابت برای دستگاه |\n| Lease | مدت اعتبار |",
        "dns": "| جزء | نقش |\n|-----|-----|\n| Resolver | کلاینت پرسشگر |\n| Recursive | جستجوی کامل |\n| Authoritative | منبع حقیقت zone |\n| Forwarder | هدایت به بالادست |\n| Split-Horizon | پاسخ متفاوت داخل/خارج |",
        "vpn": "| جزء | نقش |\n|-----|-----|\n| Phase 1 (IKE) | کانال امن کنترل |\n| Phase 2 (IPsec) | تونل داده |\n| SA | Security Association |\n| PSK / Cert | احراز هویت |\n| PFS | Perfect Forward Secrecy |",
        "firewall": "| جزء | نقش |\n|-----|-----|\n| Zone | گروه‌بندی امنیتی |\n| Policy | قانون عبور |\n| NAT | ترجمه آدرس |\n| Session | وضعیت اتصال |\n| Logging | ثبت رویداد |",
    }
    return tables.get(
        cat,
        "| جزء | نقش |\n|-----|-----|\n| Control plane | تصمیم و سیگنالینگ |\n| Data plane | عبور ترافیک |\n| Management plane | پیکربندی و لاگ |\n| Policy / AAA | مجوز و حسابرسی |",
    )


def _frame_steps(cat: str) -> str:
    steps = {
        "vlan": "1. تعریف VLAN روی سوییچ\n2. پورت access به VLAN اختصاص\n3. trunk بین سوییچ‌ها (allowed VLAN)\n4. SVI برای gateway (اگر L3)\n5. تست پینگ داخل VLAN و بین VLAN",
        "stp": "1. انتخاب Root Bridge (اولویت)\n2. محاسبه مسیر Root Port\n3. انتخاب Designated در هر سگمنت\n4. Block کردن لینک‌های اضافی\n5. در صورت تغییر توپولوژی: reconvergence",
        "ospf": "1. فعال‌سازی OSPF روی اینترفیس\n2. Hello → 2-Way → ExStart → Exchange → Full\n3. تبادل LSA\n4. محاسبه SPF\n5. نصب مسیر در جدول مسیریابی",
        "dhcp": "1. کلاینت Discover (broadcast)\n2. سرور Offer\n3. کلاینت Request\n4. سرور Ack + Lease\n5. Renewal در ۵۰٪ و ۸۷٫۵٪ عمر Lease",
        "dns": "1. کلاینت به Resolver محلی\n2. اگر cache نبود → Recursive به Root/TLD/Authoritative\n3. پاسخ + TTL\n4. ذخیره در cache\n5. در Split-Horizon: پاسخ بر اساس منبع پرسش",
        "vpn": "1. IKE Phase1 (Main/Aggressive) → ISAKMP SA\n2. IKE Phase2 → IPsec SA\n3. ترافیک جفت می‌شود (interesting traffic)\n4. رمزنگاری و ارسال\n5. Keepalive / DPD برای تشخیص قطع",
    }
    return steps.get(
        cat,
        "1. Backup پیکربندی فعلی\n2. تعیین دامنه تغییر (دستگاه / VLAN / VRF)\n3. پیکربندی حداقلی\n4. Verify محلی\n5. Verify End-to-End\n6. بررسی لاگ\n7. Rollback اگر شکست",
    )


def _lab_concrete(topic: str, cat: str, level: str) -> str:
    base = f"""# آزمایشگاه عملی — {topic}

## توپولوژی پیشنهادی Lab
- ۲ سوییچ / ۱ روتر / ۲ کلاینت (یا GNS3/EVE-NG/Packet Tracer)
- یک لینک uplink و یک لینک backup (برای تست failover)

## مراحل اجرا

### مرحله ۱ — وضعیت پایه (قبل از تغییر)
| مورد | مقدار قبل | دستور مشاهده |
|------|-----------|--------------|
| وضعیت اینترفیس | | `show ip interface brief` / `ip -br a` |
| جدول مرتبط | | دستور تخصصی دسته |
| لاگ اخیر | | `show logging` / `journalctl -n 50` |

### مرحله ۲ — تغییر برگشت‌پذیر
1. **Backup اجباری** قبل از هر change:
```
copy running-config startup-config
! یا
show running-config | redirect flash:pre-lab.cfg
```
2. پیکربندی حداقلی مرتبط با «{topic}»
3. ذخیره موقت (نه لزوماً startup تا verify کامل نشود)

### مرحله ۳ — Verify
- [ ] Verify محلی (روی همان دستگاه)
- [ ] Verify از کلاینت واقعی (پینگ / curl / nslookup)
- [ ] لاگ بدون خطای جدید

### مرحله ۴ — شکست عمدی (Failure Injection)
عمداً یکی از این‌ها را بشکن و با جدول RCA پیدا کن:
- کابل uplink را بکش
- VLAN اشتباه روی access بگذار
- ACL deny اشتباه اعمال کن
- تایمر/اولویت را خراب کن

### مرحله ۵ — Rollback
```
configure terminal
! دستورات معکوس
end
copy startup-config running-config   ! اگر نیاز
```
"""
    if level in ("L3", "L4"):
        base += f"""
### مرحله ۶ — سطح سازمانی ({level})
- پنجره Change را تعریف کن (مثلاً ۲۲:۰۰–۲۳:۰۰)
- Runbook یک‌صفحه‌ای بنویس
- Monitoring بعد از change (حداقل ۳۰ دقیقه)
- Document: چه تغییری، چرا، نتیجه، درس‌آموخته
"""
    return base


def _rca_table(cat: str) -> str:
    rows = ERRORS.get(cat, [
        ("سرویس قطع کامل", "لایه فیزیکی یا gateway", "show interface / ping gateway"),
        ("فقط بعضی کلاینت‌ها", "VLAN / ACL / DNS خاص", "مقایسه کلاینت خوب و بد"),
        ("بعد از reboot برگشت", "startup ≠ running", "show startup-config"),
        ("کندی نه قطعی", "QoS / congestion / duplex", "show interface counters / perf"),
        ("قطع متناوب", "flapping / STP reconvergence", "log | include UPDOWN|SPANTREE"),
    ])
    header = "| علامت (Symptom) | علت محتمل | دستور شواهد | اقدام اول |\n|---|---|---|---|"
    body = "\n".join(
        f"| {a} | {b} | `{c}` | ایزوله + backup |" for a, b, c in rows
    )
    return f"{header}\n{body}"


def _security_block(cat: str, level: str) -> str:
    common = """- حداقل دسترسی (least privilege) روی management
- لاگ تغییرات (who / when / what)
- جداسازی management plane از data plane
- قبل از expose به اینترنت: threat model کوتاه"""
    extra = {
        "vlan": "\n- Native VLAN را از VLAN کاربران جدا کن\n- Trunk را به allowed VLAN محدود کن\n- Port-security روی access",
        "stp": "\n- BPDU Guard روی پورت‌های access\n- Root Guard روی لبه‌های دامنه\n- PortFast فقط روی کلاینت نه uplink",
        "dhcp": "\n- DHCP Snooping + Trust فقط روی uplink سرور\n- محدودیت rate روی untrusted\n- Reservation برای زیرساخت حیاتی",
        "dns": "\n- DNSSEC در صورت امکان\n- محدود کردن recursion\n- جداسازی internal/external (Split-Horizon)",
        "vpn": "\n- الگوریتم‌های قوی (AES-GCM، SHA2)\n- PFS فعال\n- محدود کردن interesting traffic\n- مانیتور Phase1/Phase2",
        "firewall": "\n- Policy از specific به general\n- Default deny\n- لاگ sessionهای deny\n- جداسازی zone",
    }
    return common + extra.get(cat, "")


def _level_guidance(level: str) -> str:
    return {
        "L0": "فقط تصویر ذهنی و تشبیه. هنوز دستور حفظ نکن؛ بفهم «چرا».",
        "L1": "مشاهده کن + یک Lab ساده. دستورات show را اجرا و خروجی را بخوان.",
        "L2": "پیکربندی کامل + Verify + Rollback. بدون backup تغییر نده.",
        "L3": "طراحی برای چند سگمنت، RCA سیستماتیک، تأثیر روی سرویس‌های دیگر.",
        "L4": "معماری سازمانی، Change Control، HA، مستندسازی و Runbook قابل تحویل به تیم.",
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

    summary = (
        f"«{topic}» — سطح {level_fa}. "
        f"داستان سازمانی واقعی + معماری + فریم‌به‌فریم + دستورات چندوندر + "
        f"Lab عملی + جدول RCA + امنیت + چک‌لیست Production."
    )

    commands = "\n".join(
        [
            f"# بانک دستورات عملی — {topic} | {level} | دسته: {cat}",
            "",
            "## پایه و Verify (همیشه اول این‌ها)",
            _fmt(COMMON[:8]),
            f"## تخصصی دسته «{cat}»",
            _fmt(bank[:18] if len(bank) > 18 else bank),
            "## Backup و Capture",
            _fmt(
                [
                    ("show running-config | redirect flash:pre-change.cfg", "بک‌آپ قبل تغییر"),
                    ("copy running-config startup-config", "ذخیره بعد از موفقیت Verify"),
                    ("tcpdump -i any -nn -c 100 -w /tmp/cap.pcap", "نمونه پکت (لینوکس)"),
                    ("show logging | include %LINK|%LINEPROTO|%OSPF|%BGP|%SYS", "رویدادهای کلیدی"),
                    ("terminal length 0", "خروجی کامل بدون صفحه‌بندی"),
                ]
            ),
            "## Rollback سریع",
            "```\nconfigure terminal\n! دستورات معکوس Runbook را اینجا بگذار\nend\n```\n",
        ]
    )

    full = f"""# {topic}

**سطح:** {level} — {level_fa}
**EN:** {title_en or topic}
**دسته عملیاتی:** {cat}

---

## ۰) داستان واقعی سازمانی (چرا این درس مهم است؟)

{story}

اگر فقط تئوری بخوانی، در لحظه قطعی سرویس گیج می‌شوی.
این درس تو را از «دانستن اسم» به «بلد بودن رفع» می‌رساند.

---

## ۱) تشبیه ساده (برای ماندن در ذهن)

رانندگی در شهر شلوغ:
- قوانین ترافیک = پروتکل/استاندارد
- رانندگی در خیابان خلوت = Lab
- رانندگی در بزرگراه ساعت اوج = Production با چک‌لیست و Rollback

«{topic}» همان قطعه‌ای است که اگر اشتباه تنظیم شود، یا ترافیک گیر می‌کند یا تصادف (loop / blackhole / outage) رخ می‌دهد.

---

## ۲) معماری (Control / Data / Management)

{_arch_table(cat)}

---

## ۳) فریم‌به‌فریم (چه اتفاقی پشت صحنه می‌افتد؟)

{_frame_steps(cat)}

---

## ۴) سطح‌به‌سطح — تو الان کجایی؟

{_level_guidance(level)}

| سطح | انتظار از تو |
|-----|-------------|
| L0–L1 | مفهوم + مشاهده + Lab ساده |
| L2 | پیکربندی + Verify + Rollback مطمئن |
| L3–L4 | طراحی، RCA، تأثیر سازمانی، Runbook |

---

## ۵) امنیت (حتی در Lab هم عادت کن)

{_security_block(cat, level)}

---

## ۶) جدول عیب‌یابی سریع (RCA)

{_rca_table(cat)}

**مسیر RCA استاندارد:**
Symptom → Scope (کجا؟) → Evidence (دستور) → Hypothesis → Test → Fix → Verify → Document

---

## ۷) چک‌لیست Production (قبل از Apply در سازمان)

- [ ] Backup گرفته شده و قابل restore است
- [ ] Rollback نوشته و تست شده (حداقل روی کاغذ)
- [ ] دامنه تغییر مشخص است (کدام دستگاه / VLAN / VRF)
- [ ] پنجره Change و اطلاع‌رسانی انجام شده
- [ ] Monitoring بعد از change فعال است
- [ ] Runbook یک‌صفحه‌ای آماده است

---

## ۸) جمع‌بندی استاد

سه چیز را از بر باش، نه طوطی‌وار:
1. **سه دستور Verify اول** برای این موضوع
2. **مسیر RCA** وقتی علامت عجیب دیدی
3. **نقطه Rollback** قبل از هر change

«{topic}» را وقتی بلدی که بتوانی ساعت ۲ شب، با لاگ و یک کلاینت واقعی، سرویس را برگردانی.
"""

    lab = _lab_concrete(topic, cat, level)

    notes = f"""## نکات سریع عیب‌یابی — {topic}

{_rca_table(cat)}

### ترتیب ایزوله‌سازی پیشنهادی
1. لایه فیزیکی / لینک (up/down, errors, duplex)
2. لایه ۲ (VLAN, trunk, STP state)
3. لایه ۳ (gateway, route, ACL/NAT)
4. سرویس (DNS, DHCP, app)
5. کلاینت در برابر زیرساخت (مقایسه خوب/بد)

### یادداشت سطح {level}
{_level_guidance(level)}
"""

    return {
        "summary": summary,
        "full_content": full,
        "commands": commands,
        "examples": lab,
        "notes": notes,
        "level": level,
        "topic": topic,
        "category": cat,
    }
