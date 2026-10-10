#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate chapter prompt files: chapters/chXX.md and chXX/PROMPT.md"""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "chapters"

CHAPTERS = [
    (1, "مبانی IT و معماری کامپیوتر", "Architecture CPU RAM Bus"),
    (2, "اسمبل، عیب‌یابی و سرورهای سازمانی", "Hardware assembly server"),
    (3, "BIOS UEFI و بوت", "UEFI Secure Boot"),
    (4, "سیستم‌عامل پایه", "OS process memory"),
    (5, "فایل‌سیستم و Storage پایه", "FS RAID"),
    (6, "مبانی شبکه", "OSI TCP/IP model"),
    (7, "اترنت و سوییچینگ پایه", "VLAN STP"),
    (8, "IPv4 IPv6 ساب‌نتینگ", "Subnetting routing intro"),
    (9, "ARP ICMP TCP UDP", "L3 L4 protocols"),
    (10, "DNS", "DNS records recursion"),
    (11, "DHCP و IPAM", "DHCP failover IPAM"),
    (12, "کابل‌کشی فیبر رک", "Structured cabling fiber"),
    (13, "سوییچینگ سیسکو", "Cisco switching VTP EtherChannel"),
    (14, "مسیریابی پیشرفته", "OSPF BGP Redistribution"),
    (15, "MPLS VRF L3VPN", "MPLS L3VPN"),
    (16, "Multicast", "PIM IGMP"),
    (17, "EVPN VXLAN", "Leaf-Spine EVPN"),
    (18, "SDN SD-WAN SASE", "SD-WAN overlay"),
    (19, "MikroTik مبانی", "RouterOS basics"),
    (20, "MikroTik Routing Firewall NAT", "MikroTik FW NAT"),
    (21, "MikroTik QoS VPN HA", "MikroTik VPN HA"),
    (22, "وایرلس سازمانی", "Enterprise WiFi"),
    (23, "PtP PtMP", "Wireless backhaul"),
    (24, "FortiGate", "FortiGate policy VPN"),
    (25, "pfSense OPNsense Sophos", "Open-source firewalls"),
    (26, "PKI TLS", "Certificates TLS"),
    (27, "AAA NAC", "802.1X RADIUS"),
    (28, "Windows Server Core", "Windows Server roles"),
    (29, "Active Directory", "AD DS GPO"),
    (30, "Windows DNS DHCP NPS", "MS network services"),
    (31, "فایل چاپ DFS", "File server DFS"),
    (32, "امنیت Endpoint ویندوز", "Windows hardening"),
    (33, "Entra ID Hybrid", "Azure AD hybrid"),
    (34, "M365 Intune ایمیل", "M365 Intune"),
    (35, "PowerShell CMD", "PowerShell automation"),
    (36, "مدیریت لینوکس", "Linux admin"),
    (37, "شبکه لینوکس", "Linux networking"),
    (38, "سرویس لینوکس وب", "Nginx Apache"),
    (39, "امنیت لینوکس", "Linux security"),
    (40, "VMware Hyper-V", "Virtualization"),
    (41, "Proxmox Docker", "Proxmox containers"),
    (42, "Kubernetes", "K8s networking"),
    (43, "شبکه ابری", "VPC cloud networking"),
    (44, "امنیت ابر Governance", "Cloud security"),
    (45, "Storage سازمانی", "SAN NAS"),
    (46, "Backup DR", "Backup DR"),
    (47, "Data Center", "DC design"),
    (48, "HA و Load Balancing", "HA LB"),
    (49, "مانیتورینگ", "SNMP Prometheus"),
    (50, "SIEM ELK", "SIEM SOC tools"),
    (51, "اتوماسیون و AI در IT", "Ansible Python AIOps"),
    (52, "مدیریت دیتابیس", "DBA basics"),
    (53, "امنیت دیتابیس", "DB security"),
    (54, "VoIP سانترال", "VoIP QoS"),
    (55, "CCTV Access BMS IoT", "Physical security IoT"),
    (56, "امنیت پایه Zero Trust ITIL", "Zero Trust ITIL"),
    (57, "امنیت شبکه", "Network security"),
    (58, "Endpoint AppSec DevSecOps", "AppSec"),
    (59, "SOC IR Hunting", "SOC IR"),
    (60, "عیب‌یابی هک اخلاقی لاب سازمانی", "Authorized labs only"),
    (61, "معماری سازمانی Enterprise Architecture", "EA"),
    (62, "عملیات IT و NOC", "NOC ops"),
    (63, "مستندسازی Runbook و CMDB", "Runbook CMDB"),
    (64, "Git و کنترل نسخه", "Git"),
    (65, "امنیت سایبری و هک اخلاقی دفاعی + وایرلس", "Defensive security wireless"),
    (66, "مسیریابی عمیق OSPF/BGP/Redistribution", "Deep routing"),
    (67, "VPN سازمانی IPsec/SSL", "Enterprise VPN"),
    (68, "دانشنامه جامع دستورات", "Cisco MikroTik FortiGate Issabel PowerShell"),
]


def body(n: int, title: str, kw: str) -> str:
    return f"""# پرامپت فصل {n:02d} — {title}

این متن را **کامل** به ChatGPT بده (همراه با `tools/chapter_prompts/_MASTER_PROMPT.md`).

---

نقش: تولیدکننده محتوا برای NetworkEncyclopedia / ENGINEER JOKAR  
ریپو: https://github.com/MrUtility01/NetworkEncyclopedia  

## موضوع
- **شماره فصل:** {n}
- **عنوان:** {title}
- **کلیدواژه‌ها:** {kw}

## هدف
آموزش L0 تا L4 با سناریوی سازمانی؛ دستورات + Lab + RCA + ارزیابی.

## محدودیت
فقط Lab مجاز؛ سؤالات جدا از answer_key.

## فیلدهای JSON هر درس
uid (`lesson:ch{n:02d}:lvMMM:lKKKK`), chapter_order={n}, subchapter_order, lesson_order,
level, title_fa, title_en, topic, summary, full_content, commands, examples, notes,
learning_objectives, meta.assessment.questions, meta.assessment.answer_key,
source_status=review_required

## full_content
معرفی، از صفر، تشبیه، معماری، مثال، دستورات، Lab، RCA، امنیت، خلاصه، واژه‌نامه

## شروع
۱) فهرست درس‌ها با uid  ۲) JSON بسته‌های ۲۰تایی

## ذخیره
`tools/packs/ch{n:02d}/ch{n:02d}_pack.json`
"""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    lines = ["# فهرست فصل‌ها\n", "| فصل | عنوان | پوشه |", "|-----|--------|-------|"]
    for n, title, kw in CHAPTERS:
        text = body(n, title, kw)
        (OUT / f"ch{n:02d}.md").write_text(text, encoding="utf-8")
        folder = ROOT / f"ch{n:02d}"
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "PROMPT.md").write_text(text, encoding="utf-8")
        (folder / "README.md").write_text(
            f"# فصل {n}: {title}\n\nپرامپت: [PROMPT.md](PROMPT.md)\nخروجی: `tools/packs/ch{n:02d}/`\n",
            encoding="utf-8",
        )
        lines.append(f"| {n} | {title} | [ch{n:02d}/PROMPT.md](ch{n:02d}/PROMPT.md) |")
    (ROOT / "INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {len(CHAPTERS)} chapter folders under {ROOT}")


if __name__ == "__main__":
    main()
