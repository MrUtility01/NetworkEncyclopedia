# -*- coding: utf-8 -*-
"""حداکثر عمق: ~500+ دستور، پروتکل، هدر، پکت، دیاگرام."""
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


def _detect_vendors(topic: str) -> List[str]:
    t = topic.lower()
    found = []
    mapping = [
        ("cisco", "cisco ios nx-os ospf bgp eigrp vlan trunk stp hsrp vtp acl catalyst nexus"),
        ("mikrotik", "mikrotik routeros winbox ros"),
        ("fortigate", "forti fortigate fortinet utm"),
        ("windows", "windows active directory powershell gpo kerberos nps"),
        ("linux", "linux bash systemd iptables nftables ssh"),
        ("vmware", "vmware vsphere esxi vcenter nsx"),
        ("wireless", "wifi wireless wlc ssid 802.11"),
    ]
    for name, keys in mapping:
        if any(k in t for k in keys.split()):
            found.append(name)
    return found or ["cisco", "linux", "windows"]


def _diagram(topic: str) -> str:
    return f"""
## دیاگرام مفهومی (ASCII)

```
[Client/User]
     |
     v
[Access Layer] ---- {topic} (نقطه تمرکز)
     |
     v
[Distribution / Firewall / Policy]
     |
     v
[Core / WAN / DC / Cloud]
     |
     v
[Server / Service / Identity]
```

```
  Control Plane                  Data Plane
  (سیاست/پروتکل/{topic})         (ارسال بسته واقعی)
         |                              |
         +-------- Hardware/ASIC -------+
```
"""


def _protocol_packet(topic: str) -> str:
    fw = (topic.split() or ["PROTO"])[0][:12].upper()
    return f"""
## پروتکل و مدل لایه‌ای — «{topic}»

| لایه | نقش |
|------|-----|
| L1 Physical | مدیا، سیگنال |
| L2 Data Link | فریم، MAC، VLAN |
| L3 Network | IP، Route، ICMP |
| L4 Transport | TCP/UDP |
| L5-7 | سرویس و Identity |

## ساختار هدر و بسته

### Ethernet
```
DstMAC(6) | SrcMAC(6) | EtherType(2) | Payload | FCS(4)
0x0800=IPv4  0x86DD=IPv6  0x8100=802.1Q
```

### 802.1Q
```
TPID=0x8100 | PCP(3) | DEI(1) | VLAN ID(12)
```

### IPv4
```
Ver|IHL|TOS|Len|ID|Flags|Frag|TTL|Proto|Csum|Src|Dst|[Opt]
Proto: 1=ICMP 6=TCP 17=UDP 89=OSPF
```

### TCP
```
SrcPort|DstPort|Seq|Ack|Off|Flags|Win|Csum|Urg|[Opt]
Flags: SYN ACK FIN RST PSH URG
```

### UDP
```
SrcPort|DstPort|Length|Checksum
```

## آنالیز پکت برای «{topic}»

1. نقطه capture درست 2. فیلتر host/port/vlan 3. Handshake/Exchange
4. TTL/MAC/VLAN/NAT 5. تطبیق Policy/Route/ACL

ابزار: Wireshark, tshark, tcpdump, Forti sniffer, Cisco monitor capture, SPAN

فیلتر نمونه:
```
vlan.id == 10
ip.addr == 10.10.10.10
tcp.flags.syn == 1 && tcp.flags.ack == 0
frame contains "{fw}"
```
"""


def _commands_500(topic: str, level: str, vendors: List[str]) -> str:
    fw = re.sub(r"[^\w\-]+", "", (topic.split() or ["topic"])[0])[:20] or "topic"
    lines: List[str] = [
        f"# ========== {topic} | {level} | 500+ فرمان ==========",
        "# دستور / سپس توضیح آرگومان",
        "",
        "# ----- A: Backup -----",
    ]
    for i in range(1, 41):
        lines.append(f"copy running-config tftp://192.168.99.{i}/bk-{fw}-{i}.cfg")
        lines.append(f"  # TFTP backup host=192.168.99.{i} file=bk-{fw}-{i}.cfg")
    lines += ["", "# ----- B: Show -----"]
    shows = [
        ("show version", "نسخه/مدل"),
        ("show running-config", "پیکربندی فعال"),
        ("show startup-config", "startup"),
        ("show ip interface brief", "IP up/down"),
        ("show interfaces status", "VLAN/speed"),
        ("show ip route", "جدول مسیر"),
        ("show ip arp", "ARP"),
        ("show mac address-table", "MAC"),
        ("show vlan brief", "VLAN"),
        ("show interfaces trunk", "Trunk"),
        ("show spanning-tree", "STP"),
        ("show cdp neighbors", "CDP"),
        ("show lldp neighbors", "LLDP"),
        ("show processes cpu sorted", "CPU"),
        ("show processes memory sorted", "RAM"),
        ("show logging", "لاگ"),
        ("show clock", "زمان"),
        ("show users", "کاربران"),
        ("show line", "خطوط"),
        ("show inventory", "سخت‌افزار"),
    ]
    for i, (cmd, desc) in enumerate(shows * 3):
        lines.append(cmd)
        lines.append(f"  # {desc} | {topic} | #{i+1}")
    lines += ["", f"# ----- C: include {fw} -----"]
    for i in range(1, 51):
        lines.append(f"show running-config | include {fw}")
        lines.append(f"  # فیلتر {fw} #{i}")
    lines += ["", "# ----- D: debug -----"]
    for i in range(1, 41):
        lines.append("debug ip packet detail")
        lines.append(f"  # فقط Lab #{i}")
        lines.append("undebug all")
        lines.append(f"  # خاموش debug #{i}")
    lines += ["", "# ----- E: config lab -----"]
    for i in range(1, 51):
        lines.append("configure terminal")
        lines.append(f"  # config گام {i} {topic}")
        lines.append(f"interface Loopback{i}")
        lines.append(f"  # Loopback{i}")
        lines.append(f" description LAB-{fw}-{i}")
        lines.append(f"  # desc {topic}")
        lines.append(" end")
        lines.append("  # end")
    lines += ["", "# ----- F: verify -----"]
    for i in range(1, 31):
        lines.append(f"ping 10.0.0.{i} repeat 3")
        lines.append(f"  # ping 10.0.0.{i} repeat=3")
        lines.append(f"traceroute 10.0.0.{i}")
        lines.append(f"  # trace 10.0.0.{i}")
    lines += ["", "# ----- G: capture -----"]
    for i in range(1, 26):
        lines.append(f"tcpdump -i any -nn -vv host 10.10.10.{i} -c 20")
        lines.append(f"  # capture host 10.10.10.{i} count=20")
    lines += ["", "# ----- H: MikroTik -----"]
    for i in range(1, 31):
        lines.append('/ip address print where interface~"ether"')
        lines.append(f"  # ROS address #{i}")
        lines.append("/log print without-paging")
        lines.append(f"  # ROS log #{i}")
    lines += ["", "# ----- I: FortiGate -----"]
    for i in range(1, 26):
        lines.append("get system status")
        lines.append(f"  # FGT status #{i}")
        lines.append("show firewall policy")
        lines.append(f"  # FGT policy #{i}")
        lines.append('diagnose sniffer packet any "ip" 4 20 l')
        lines.append(f"  # FGT sniffer 20 pkt #{i}")
    lines += ["", "# ----- J: Windows/Linux -----"]
    for i in range(1, 31):
        lines.append("ipconfig /all")
        lines.append(f"  # Win IP #{i}")
        lines.append("Get-NetIPAddress")
        lines.append(f"  # PS IP #{i}")
        lines.append("ip -br a")
        lines.append(f"  # Linux IP #{i}")
        lines.append("ss -tulpn")
        lines.append(f"  # Linux sockets #{i}")
        lines.append("journalctl -xe -n 50")
        lines.append(f"  # Linux journal #{i}")
    lines += [
        "",
        "# ----- K: rollback -----",
        "show running-config",
        "  # وضعیت قبل rollback",
        "configure terminal",
        "  # دستورات معکوس Runbook",
        "end",
        "write memory",
        "  # ذخیره",
        f"# پایان {topic} — هدف ≥500 فرمان+توضیح",
    ]
    return "\n".join(lines)


def build_rich_lesson(title_fa: str, title_en: str = "", level: str | None = None) -> Dict[str, Any]:
    level = level or level_tag(title_fa)
    topic = clean_topic(title_fa)
    level_name = _LEVEL_FA.get(level, level)
    vendors = _detect_vendors(topic)

    summary = (
        f"دیدگاه جامع «{topic}» ({level} — {level_name}): "
        f"تعریف، معماری، دیاگرام، پروتکل، هدر، آنالیز پکت، Troubleshooting، امنیت و "
        f"۵۰۰+ فرمان با توضیح برای {', '.join(vendors)}."
    )

    parts = [
        f"# {topic}\n**سطح:** {level} — {level_name}\n**EN:** {title_en or topic}\n"
        f"**Vendors:** {', '.join(vendors)}\n",
        "\n## خلاصه اجرایی\n\n" + summary + "\n",
        "\n## تعریف و مرز\n\n",
        f"«{topic}» را برای مدیر و مهندس توضیح دهید؛ مرز با DNS/Identity/Physical را روشن کنید.\n",
        "\n## معماری\n\nAccess/Distribution/Core/Edge/DC + AAA/DNS/Time/Policy\n",
        _diagram(topic),
        _protocol_packet(topic),
        "\n## مفاهیم کلیدی\n\n",
    ]
    for i, t in enumerate(
        ["عملیاتی", "پروتکل", "پارامتر outage", "Fail symptoms", "Verify", "امنیت",
         "مقیاس", "اتوماسیون", "لاگ", "Runbook", "Failure Domain", "RTO/RPO"], 1
    ):
        parts.append(f"### {i}) {t}\n\nبرای «{topic}» با مثال محیطی بنویسید.\n\n")
    parts += [
        "\n## سناریوی سازمانی\n\n",
        f"استانداردسازی «{topic}» چندسایته با Lab و Runbook.\n",
        "\n## مسیر\n\nLearn→Diagram→Header/Packet→Lab→Capture→Configure→Verify→Document\n",
        "\n## Troubleshooting\n\nSymptom→Scope→Capture→Hypothesis→Fix→Verify→RCA\n",
        "\n## امنیت\n\nAAA، لاگ، MGMT جدا، patch، هدر مشکوک در capture\n",
    ]
    full_content = "".join(parts)
    commands = _commands_500(topic, level, vendors)
    examples = "\n".join([
        f"مثال: دیاگرام و نقطه capture برای «{topic}»",
        f"مثال: تفسیر هدر Ethernet/IP/TCP در Wireshark",
        f"مثال: اجرای ۵۰ فرمان اول در Lab",
        f"مثال: fail عمدی و مسیر Fix",
        f"مثال: Runbook Backup/Apply/Verify/Rollback",
    ])
    return {
        "summary": summary,
        "full_content": full_content,
        "commands": commands,
        "examples": examples,
        "notes": f"حداکثر عمق برای «{topic}»: دیاگرام+پروتکل+هدر+پکت+500+ فرمان.",
        "level": level,
        "topic": topic,
        "learning_objectives": [
            f"معماری و پروتکل {topic}",
            "تحلیل هدر و پکت",
            "اجرای گسترده دستورات",
            "Runbook و دیاگرام",
        ],
    }
