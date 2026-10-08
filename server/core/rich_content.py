# -*- coding: utf-8 -*-
"""محتوای عمیق + دستورات چندوندری با توضیح کامل آرگومان."""
from __future__ import annotations

import re
from typing import Any, Dict, List


def level_tag(title: str) -> str:
    m = re.match(r"\[(L[0-4])\]", title or "")
    return m.group(1) if m else "L0"


def clean_topic(title: str) -> str:
    t = re.sub(r"^\[L[0-4]\]\s*", "", title or "").strip()
    t = re.sub(
        r"\s*[—\-]\s*(آشنایی|مقدماتی|ادمین|مهندس|خبره|Intro|Junior|Admin|Senior|Architect)\s*$",
        "",
        t,
        flags=re.I,
    )
    return t.strip() or (title or "موضوع")


_LEVEL_FA = {
    "L0": "آشنایی / مقدماتی",
    "L1": "کاربر فنی / Junior",
    "L2": "Administrator",
    "L3": "Engineer / Senior",
    "L4": "Architect / Enterprise",
}

_DEPTH = {
    "L0": 3,
    "L1": 4,
    "L2": 6,
    "L3": 8,
    "L4": 10,
}


def _detect_vendors(topic: str) -> List[str]:
    t = topic.lower()
    v = []
    rules = [
        ("cisco", ["cisco", "ios", "nx-os", "catalyst", "nexus", "ospf", "eigrp", "bgp", "vlan", "trunk", "stp", "hsrp", "vtp", "acl"]),
        ("mikrotik", ["mikrotik", "routeros", "winbox", "ros"]),
        ("fortigate", ["forti", "fortigate", "fortinet", "utm"]),
        ("windows", ["windows", "active directory", "ad ds", "powershell", "gpo", "dns", "dhcp", "nps", "kerberos"]),
        ("linux", ["linux", "bash", "systemd", "iptables", "nftables", "sshd"]),
        ("vmware", ["vmware", "vsphere", "esxi", "vcenter", "nsx"]),
        ("wireless", ["wifi", "wi-fi", "wireless", "wlc", "ssid", "802.11"]),
    ]
    for name, keys in rules:
        if any(k in t for k in keys):
            v.append(name)
    if not v:
        v = ["cisco", "linux"]  # پیش‌فرض عملی
    return v


def _cmd_cisco(topic: str, level: str) -> str:
    fw = (topic.split() or ["feature"])[0]
    return f"""
### Cisco IOS / NX-OS — {topic}

enable
  # ورود به Privileged EXEC؛ بدون این بسیاری دستورات show/config اجرا نمی‌شوند

show version
  # مدل، نسخه IOS، uptime، حافظه — پایه Inventory و سازگاری feature

show running-config
  # کل پیکربندی فعال؛ قبل از تغییر برای diff و مستندسازی

show running-config | include {fw}
  # فقط خطوط مرتبط با کلیدواژه موضوع؛ آرگومان include = الگوی regex/متن

show ip interface brief
  # وضعیت up/down و IP هر اینترفیس — Scope اولیه قطعی

show interfaces status
  # VLAN، speed، duplex، connect — لایه Access

show ip route
  # جدول مسیریابی؛ default route و routeهای یادگرفته‌شده را چک کنید

show logging | last 100
  # ۱۰۰ خط آخر لاگ؛ آرگومان last = تعداد خطوط

configure terminal
  # ورود به Global Configuration

interface GigabitEthernet0/1
  # انتخاب اینترفیس؛ نام را با show ip int brief تطبیق دهید
  description LAB-{fw}
    # برچسب انسانی برای مستندات و NetBox
  no shutdown
    # روشن کردن اینترفیس (در صورت down بودن اداری)

end
  # بازگشت به Privileged EXEC

write memory
  # ذخیره running → startup؛ معادل copy running-config startup-config

# --- Verify ---
ping 8.8.8.8 repeat 5
  # تست L3؛ repeat = تعداد بسته
traceroute 8.8.8.8
  # مسیر hop-by-hop برای یافتن نقطه شکست

# --- Rollback ایده ---
# configure terminal
#  (دستورات معکوس را از قبل در Runbook بنویسید)
# end
# write memory
""".strip()


def _cmd_mikrotik(topic: str, level: str) -> str:
    return f"""
### MikroTik RouterOS — {topic}

/system resource print
  # CPU، RAM، uptime — سلامت کلی دستگاه

/system identity print
  # نام دستگاه برای موجودی و مستندات

/export file=backup-before-change
  # خروجی کامل پیکربندی قبل از تغییر؛ فایل در storage دستگاه

/interface print detail
  # لیست اینترفیس‌ها با وضعیت و ویژگی‌ها

/ip address print
  # آدرس‌های L3 فعلی

/ip route print
  # جدول مسیر؛ dst-address و gateway را بررسی کنید

/log print where topics~"error|critical"
  # لاگ خطا؛ where = فیلتر

/ip firewall filter print
  # قوانین فایروال؛ ترتیب chain مهم است

# نمونه اعمال ایمن (Lab):
# /ip address add address=192.168.10.1/24 interface=bridge1 comment="{topic}"
#   address = IP/Mask | interface = نام پورت/بریج | comment = یادداشت

/system backup save name=after-lab
  # بکاپ باینری پس از تست موفق
""".strip()


def _cmd_fortigate(topic: str, level: str) -> str:
    return f"""
### FortiGate — {topic}

get system status
  # نسخه firmware، سریال، حالت HA

get system interface physical
  # وضعیت لینک پورت‌های فیزیکی

show system interface
  # IP، allowaccess، role هر اینترفیس

show firewall policy
  # سیاست‌ها؛ ترتیب top-down مهم است

diagnose firewall iprope lookup <src> <dst> <proto> <port>
  # شبیه‌سازی تصمیم Policy؛ برای عیب‌یابی deny

diagnose sniffer packet any "host x.x.x.x" 4 50 l
  # capture سبک؛ آرگومان: فیلتر، verbosity، تعداد بسته

execute backup config tftp <server> <filename>
  # بکاپ پیکربندی قبل از تغییر

# پس از تغییر:
# diagnose debug enable
# diagnose debug flow filter addr <ip>
# diagnose debug flow trace start 50
#   برای دنبال کردن مسیر بسته در Policy/NAT
""".strip()


def _cmd_windows(topic: str, level: str) -> str:
    return f"""
### Windows / PowerShell — {topic}

Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion
  # نسخه ویندوز برای سازگاری feature

ipconfig /all
  # IP، DNS، DHCP، MAC — پایه شبکه کلاینت/سرور

Get-Service | Where-Object Status -eq 'Running'
  # سرویس‌های در حال اجرا

Get-EventLog -LogName System -Newest 50
  # ۵۰ رویداد اخیر System؛ Newest = تعداد

# Active Directory (در صورت مرتبط بودن):
# Get-ADDomain
# Get-ADDomainController
# nltest /dsgetdc:<domain>
#   پیدا کردن DC مناسب سایت

# DNS:
# Resolve-DnsName <name> -Type A
# Get-DnsServerResourceRecord -ZoneName <zone>  (روی DNS Server)

# تست:
Test-NetConnection -ComputerName 8.8.8.8 -Port 53
  # اتصال TCP/UDP به مقصد؛ Port = پورت هدف
""".strip()


def _cmd_linux(topic: str, level: str) -> str:
    return f"""
### Linux — {topic}

uname -a
  # کرنل و معماری

ip -br a
  # خلاصه آدرس اینترفیس‌ها

ip route show
  # جدول مسیر

ss -tulpn
  # سوکت‌های گوش‌دهنده؛ t=TCP u=UDP l=listen p=process n=numeric

journalctl -xe -n 100
  # لاگ systemd؛ n = تعداد خطوط

# فایروال نمونه:
# sudo iptables -L -n -v
#   L=list n=numeric v=verbose

# تست:
ping -c 5 8.8.8.8
  # c = تعداد بسته
traceroute 8.8.8.8
curl -v https://example.com
  # v = جزئیات TLS/HTTP
""".strip()


_CMD_BUILDERS = {
    "cisco": _cmd_cisco,
    "mikrotik": _cmd_mikrotik,
    "fortigate": _cmd_fortigate,
    "windows": _cmd_windows,
    "linux": _cmd_linux,
    "vmware": _cmd_linux,
    "wireless": _cmd_cisco,
}


def _commands_block(topic: str, level: str) -> str:
    vendors = _detect_vendors(topic)
    parts = [
        f"# دستورات عمیق — {topic} | سطح {level}",
        "# هر دستور با توضیح کاربرد و آرگومان آمده است.",
        "# ابتدا Lab، سپس Change Window در Production.",
        "",
        "## ایمنی مشترک",
        "# 1) Backup  2) Diff  3) Apply  4) Verify  5) Document",
        "",
    ]
    for v in vendors:
        fn = _CMD_BUILDERS.get(v, _cmd_cisco)
        parts.append(fn(topic, level))
        parts.append("")
    if level in ("L3", "L4"):
        parts.append(
            "## چک‌لیست Engineer\n"
            "- [ ] Backup گرفته شد\n"
            "- [ ] Rollback نوشته شد\n"
            "- [ ] Verify از دو نقطه\n"
            "- [ ] لاگ/مانیتورینگ چک شد\n"
            "- [ ] CMDB/NetBox به‌روز شد\n"
        )
    return "\n".join(parts)


def build_rich_lesson(title_fa: str, title_en: str = "", level: str | None = None) -> Dict[str, Any]:
    level = level or level_tag(title_fa)
    topic = clean_topic(title_fa)
    depth = _DEPTH.get(level, 6)
    level_name = _LEVEL_FA.get(level, level)
    vendors = _detect_vendors(topic)

    summary = (
        f"دیدگاه جامع «{topic}» (سطح {level} — {level_name}): "
        f"این مبحث یکی از بلوک‌های عملیاتی شبکه/زیرساخت/امنیت است. "
        f"مهندس باید بداند موضوع چیست، در کدام لایه OSI/معماری قرار می‌گیرد، "
        f"با چه سرویس‌هایی جفت می‌شود، چه پارامترهایی باعث outage می‌شوند، "
        f"و چگونه با Backup→Configure→Verify→Troubleshoot→Document کار کند. "
        f"Vendorهای مرتبط تشخیص‌داده‌شده: {', '.join(vendors)}. "
        f"در این سطح خروجی یادگیری شامل درک مفهوم، سناریوی سازمانی، "
        f"دستورات چندوندری با معنی آرگومان، و معیار Verify است."
    )

    sections: List[str] = [
        f"# {topic}\n",
        f"**سطح:** {level} — {level_name}\n",
        f"**EN:** {title_en or topic}\n",
        f"**Vendors:** {', '.join(vendors)}\n",
        "\n## خلاصه اجرایی (دیدگاه کلی)\n\n",
        summary + "\n",
        "\n## ۱) تعریف و مرز مسئولیت\n\n",
        f"«{topic}» را باید بتوانید در دو دقیقه برای مدیر غیرتخصصی و در ده دقیقه برای مهندس توضیح دهید. "
        f"مرز مسئولیت یعنی چه چیزی داخل این مبحث است و چه چیزی به DNS، Firewall، Identity یا لینک فیزیکی واگذار می‌شود.\n",
        "\n## ۲) جایگاه در معماری\n\n",
        "- لایه منطقی (Access / Distribution / Core / Edge / DC)\n",
        "- وابستگی به Identity، DNS، Time، Routing، Policy\n",
        "- اثر روی Confidentiality / Integrity / Availability\n",
        "\n## ۳) پیش‌نیازها\n\n",
        "TCP/IP، آدرس‌دهی، تفاوت Control Plane و Data Plane، مدل Change سازمانی، خواندن لاگ.\n",
        "\n## ۴) مفاهیم کلیدی (عمیق)\n\n",
    ]

    concepts = [
        ("تعریف عملیاتی", f"«{topic}» در محیط واقعی دقیقاً چه مشکلی را حل می‌کند؟"),
        ("اجزای تشکیل‌دهنده", "کدام پروتکل‌ها، سرویس‌ها و اشیاء پیکربندی درگیر هستند؟"),
        ("پارامترهای حساس", "کدام مقدار غلط باعث قطعی یا حفره امنیتی می‌شود؟"),
        ("حالت‌های Fail", "علائم رایج خرابی و اولین دستورات تشخیص؟"),
        ("Verify", "بعد از تغییر چه خروجی show/log/test باید دیده شود؟"),
        ("امنیت", "Least Privilege، لاگ، جداسازی Management"),
        ("مقیاس", "از Lab تک‌دستگاه تا چندسایت Enterprise چه عوض می‌شود؟"),
        ("اتوماسیون", "کدام بخش‌ها idempotent و قابل Playbook هستند؟"),
        ("مشاهده‌پذیری", "چه متریک/لاگی باید به مانیتورینگ برود؟"),
        ("مستندسازی", "حداقل فیلدهای Runbook و CMDB چیست؟"),
    ]
    for i in range(min(depth, len(concepts))):
        title_c, q = concepts[i]
        sections.append(f"### {i + 1}) {title_c}\n\n{q}\n\n")
        sections.append(
            f"برای «{topic}» این مورد را روی کاغذ برای محیط خودتان بنویسید؛ "
            f"بدون مثال محیطی یادگیری سطحی می‌ماند.\n\n"
        )

    sections += [
        "\n## ۵) سناریوی سازمانی\n\n",
        f"سازمانی با چند صد تا چند هزار کاربر می‌خواهد «{topic}» را استاندارد کند. "
        f"محدودیت: پنجره Change، بودجه، و عدم قطعی سرویس‌های حیاتی. "
        f"شما طرح، Lab proof، Runbook و معیار پذیرش (Acceptance) تحویل می‌دهید.\n",
        "\n## ۶) مسیر مهندسی\n\n",
        "```\nLearn → Design → Lab → Change → Configure → Verify → Monitor → Troubleshoot → Harden → Document\n```\n",
        "\n## ۷) Verification\n\n",
        "1. Backup و hash پیکربندی\n2. اعمال در پنجره مجاز\n"
        "3. show/status/log\n4. تست از دو کلاینت/دو سایت\n5. ثبت نتیجه در تیکت\n",
        "\n## ۸) Troubleshooting ساخت‌یافته\n\n",
        "1. Symptom دقیق\n2. Scope (یک کاربر؟ یک VLAN؟ یک سایت؟)\n"
        "3. Evidence (log/counter/capture)\n4. Hypothesis + تست\n5. Fix + Verify\n6. Root cause و اقدام پیشگیرانه\n",
    ]
    if level in ("L2", "L3", "L4"):
        sections.append(
            "\n## ۹) امنیت و Hardening\n\n"
            f"- دسترسی مدیریتی به «{topic}» با AAA/Least Privilege\n"
            "- ثبت تغییرات و هشدار\n- جداسازی MGMT\n- به‌روزرسانی firmware/patch\n"
        )
    if level in ("L3", "L4"):
        sections.append(
            "\n## ۱۰) نگاه Architect\n\n"
            "Failure domain، RTO/RPO، ظرفیت، هزینه، یکپارچگی با NetBox/CMDB، "
            "و حذف SPOF را برای این مبحث طراحی کنید.\n"
        )

    full_content = "".join(sections)
    commands = _commands_block(topic, level)

    examples = "\n".join(
        [
            f"مثال Lab ۱: توپولوژی حداقلی برای «{topic}» بسازید و baseline ذخیره کنید.",
            f"مثال Lab ۲: یک پیکربندی غلط عمدی اعمال و با مسیر Troubleshooting پیدا کنید.",
            f"مثال سازمانی: تغییر را در پنجره Change با Rollback از پیش نوشته اجرا کنید.",
        ]
        + ([f"مثال HA: قطع مسیر اصلی و اندازه‌گیری بازیابی مرتبط با «{topic}»."] if level in ("L3", "L4") else [])
    )

    notes = (
        f"سطح {level}: عمق این درس برای کار عملی است. "
        f"دستورات چندوندری ({', '.join(vendors)}) را در Lab تکرار کنید. "
        "Production فقط با Backup و Rollback."
    )

    return {
        "summary": summary,
        "full_content": full_content,
        "commands": commands,
        "examples": examples,
        "notes": notes,
        "level": level,
        "topic": topic,
        "learning_objectives": [
            f"توضیح معماری‌گونه {topic}",
            f"اجرای دستورات چندوندری با درک آرگومان",
            f"Verify و Troubleshooting {topic}",
            f"آماده‌سازی Runbook سازمانی",
        ],
    }
