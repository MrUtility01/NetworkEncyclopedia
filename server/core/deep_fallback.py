# -*- coding: utf-8 -*-
"""موتور محتوای عمیق برای هر درسی که teacher اختصاصی ندارد."""
from __future__ import annotations
import re
from typing import Any, Dict, List
from core.rich_data import BANKS, COMMON, ERRORS

_LEVEL_FA = {"L0": "آشنایی / مقدماتی", "L1": "Junior", "L2": "Administrator", "L3": "Engineer / Senior", "L4": "Architect"}
_CATS = [
    ("vlan", ["vlan", "trunk", "access", "802.1q"]), ("stp", ["stp", "spanning", "rstp", "bpdu"]),
    ("ospf", ["ospf", "area", "lsa"]), ("bgp", ["bgp", "prefix-list", "route-map"]),
    ("acl", ["acl", "access-list"]), ("nat", ["nat", "pat", "overload"]),
    ("vpn", ["vpn", "ipsec", "ike", "tunnel"]), ("dhcp", ["dhcp", "scope", "lease", "relay"]),
    ("dns", ["dns", "resolver", "zone"]), ("wireless", ["wifi", "wireless", "ssid", "wpa"]),
    ("firewall", ["firewall", "fortigate", "asa"]), ("ha", ["hsrp", "vrrp", "glbp"]),
    ("qos", ["qos", "dscp", "policing"]), ("linux", ["linux", "iptables", "systemd"]),
    ("windows", ["windows", "powershell", "gpo"]), ("storage", ["raid", "nvme", "ssd", "san"]),
    ("virtualization", ["vmware", "esxi", "kubernetes", "docker", "pod"]),
    ("security", ["aaa", "radius", "tls", "snmp"]), ("tcpip", ["tcp", "udp", "icmp", "snmp"]),
    ("sql", ["sql", "postgres", "mysql", "elasticsearch"]), ("python", ["python", "paramiko", "netmiko"]),
    ("ansible", ["ansible", "playbook"]), ("terraform", ["terraform", "iac"]),
]

def _level(title):
    m = re.match(r"\[(L[0-4])\]", title or "")
    return m.group(1) if m else "L0"

def _topic(title):
    t = re.sub(r"^\[L[0-4]\]\s*", "", title or "").strip()
    t = re.sub(r"\s*[—\-]\s*(آشنایی|مقدماتی|ادمین|مهندس|خبره|Intro|Junior|Admin|Senior|Architect).*$", "", t, flags=re.I)
    return t.strip() or (title or "موضوع")

def _cat(topic):
    t = topic.lower()
    for c, keys in _CATS:
        if any(k in t for k in keys):
            return c
    return "general"

def _fmt(pairs):
    return "\n".join(f"```\n{cmd}\n```\n→ {desc}\n" for cmd, desc in pairs)

def build_deep_fallback(title_fa: str, title_en: str = "", level: str | None = None) -> Dict[str, Any]:
    level = level or _level(title_fa)
    topic = _topic(title_fa)
    cat = _cat(topic)
    level_fa = _LEVEL_FA.get(level, level)
    vendors = ["cisco", "linux", "windows"]
    bank = BANKS.get(cat, BANKS.get("linux", COMMON))
    summary = f"«{topic}» سطح {level_fa}: مفهوم، معماری، فریم‌به‌فریم، دستورات چندوندر، Lab، RCA و امنیت — {cat}."
    commands = "\n".join([
        f"# بانک دستورات عمیق — {topic} | {level} | {cat}", "",
        "## پایه و Verify", _fmt(COMMON),
        f"## تخصصی ({cat})", _fmt(bank[:20] if len(bank) > 20 else bank),
        "## Backup و Capture", _fmt([
            ("show running-config | redirect flash:pre-change.cfg", "بک‌آپ قبل تغییر"),
            ("copy running-config startup-config", "ذخیره بعد موفقیت"),
            ("tcpdump -i any -nn -c 100", "نمونه پکت"),
            ("show logging | include %LINK|%LINEPROTO|%OSPF|%BGP", "رویدادها"),
        ]),
        "## Rollback", "```\nconfigure terminal\n! معکوس Runbook\nend\n```\n",
    ])
    err_rows = ERRORS.get(cat, [
        (f"سرویس {topic} قطع", "ایزوله L1→L7", "ping / show interface / log"),
        ("بعد reboot برگشت", "startup≠running", "show startup-config"),
        ("فقط بعضی کلاینت‌ها", "VLAN/ACL/DNS", "مقایسه کلاینت خوب و بد"),
    ])
    err_table = "\n".join(["| علامت | علت | اقدام |", "|---|---|---|"] + [f"| {a} | {b} | `{c}` |" for a,b,c in err_rows])
    full = f"""# {topic}

**سطح:** {level} — {level_fa}
**EN:** {title_en or topic}
**دسته:** {cat}
**Vendors:** {', '.join(vendors)}

---

## ۱) چرا مهم است؟
«{topic}» بلوک عملیاتی واقعی است. بدون معماری و Verify، عیب‌یابی حدسی و change خطرناک می‌شود.

### تشبیه
رانندگی: قوانین → Lab → production با چک‌لیست.

## ۲) معماری
| جزء | نقش |
|-----|-----|
| Control plane | تصمیم و سیگنالینگ |
| Data plane | عبور ترافیک/داده |
| Management plane | پیکربندی و لاگ |
| Policy / AAA | مجوز |

## ۳) فریم‌به‌فریم
1. Backup  2. دامنه (دستگاه/VLAN/VRF)  3. پیکربندی حداقلی  4. Verify محلی  5. Verify E2E  6. لاگ  7. Rollback اگر شکست

## ۴) سطح‌به‌سطح
L0–L1 مفهوم+مشاهده | L2 پیکربندی+Verify+Rollback | L3–L4 طراحی+RCA

## ۵) امنیت
حداقل دسترسی، لاگ تغییرات، جداسازی management، threat model قبل از expose

## ۶) چک‌لیست Production
- [ ] Backup  - [ ] Rollback مشخص  - [ ] Monitoring  - [ ] Runbook

## ۷) جمع‌بندی استاد
سه دستور Verify اول و مسیر RCA را از بر باش — نه حفظ طوطی‌وار.

{err_table}
"""
    lab = f"""# آزمایشگاه — {topic}

## ۱ مشاهده
| مورد | قبل | بعد |
|------|-----|-----|
| | | |

## ۲ تغییر برگشت‌پذیر (اول backup)
## ۳ شکست عمدی در Lab و پیدا کردن با جدول عیب‌یابی
## ۴ سه دستور اول در قطعی سازمانی
1.
2.
3.
"""
    notes = f"## عیب‌یابی\n\n{err_table}\n\n### RCA\nSymptom→Scope→Evidence→Hypothesis→Test→Fix→Verify→Document\n"
    return {"summary": summary, "full_content": full, "commands": commands, "examples": lab, "notes": notes, "level": level, "topic": topic, "category": cat}
