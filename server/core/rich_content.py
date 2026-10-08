# -*- coding: utf-8 -*-
"""محتوای بسیار عمیق: دستورات واقعی چند‌وندر، عیب‌یابی، Lab، امنیت."""
from __future__ import annotations
import re
from typing import Any, Dict, List, Tuple
from core.rich_data import BANKS, ERRORS, COMMON

def level_tag(title: str) -> str:
    m = re.match(r"\[(L[0-4])\]", title or "")
    return m.group(1) if m else "L0"

def clean_topic(title: str) -> str:
    t = re.sub(r"^\[L[0-4]\]\s*", "", title or "").strip()
    t = re.sub(r"\s*[—\-]\s*(آشنایی|مقدماتی|ادمین|مهندس|خبره|Intro|Junior|Admin|Senior|Architect)\s*$", "", t, flags=re.I)
    return t.strip() or (title or "موضوع")

_LEVEL_FA = {"L0": "آشنایی / مقدماتی", "L1": "Junior", "L2": "Administrator", "L3": "Engineer / Senior", "L4": "Architect"}

_CATS = [
    ("vlan", ["vlan", "trunk", "access", "802.1q", "dot1q", "سگمنت", "tag", "native"]),
    ("stp", ["stp", "spanning", "rstp", "mst", "bpdu", "loop", "portfast"]),
    ("ospf", ["ospf", "area", "lsa", "dr", "bdr", "nssa"]),
    ("bgp", ["bgp", "as path", "prefix-list", "route-map", "ebgp", "ibgp"]),
    ("acl", ["acl", "access-list", "extended", "standard", "filter"]),
    ("nat", ["nat", "pat", "overload", "snat", "dnat", "masquerade"]),
    ("vpn", ["vpn", "ipsec", "ike", "tunnel", "gre", "ssl vpn", "dmvpn"]),
    ("dhcp", ["dhcp", "scope", "lease", "relay", "helper"]),
    ("dns", ["dns", "resolver", "zone", "forwarder"]),
    ("wireless", ["wifi", "wireless", "ssid", "wlc", "802.11", "wpa"]),
    ("firewall", ["firewall", "fortigate", "asa", "policy", "utm", "ngfw"]),
    ("ha", ["hsrp", "vrrp", "glbp", "ha", "failover"]),
    ("qos", ["qos", "dscp", "policing", "shaping", "priority"]),
    ("linux", ["linux", "iptables", "nftables", "systemd", "bash", "sshd"]),
    ("windows", ["windows", "powershell", "gpo", "active directory", "kerberos", "nps"]),
    ("storage", ["raid", "nvme", "ssd", "iops", "san", "iscsi"]),
    ("virtualization", ["vmware", "esxi", "vcenter", "hyper-v", "kvm"]),
    ("security", ["aaa", "radius", "tacacs", "certificate", "tls", "802.1x"]),
    ("tcpip", ["tcp", "udp", "icmp", "mtu", "fragment"]),
    ("boot", ["bios", "uefi", "boot", "pxe", "grub"]),
    ("cpu", ["cpu", "processor", "core", "thread"]),
    ("memory", ["ram", "ddr", "ecc", "memory"]),
]

def _cat(topic: str) -> str:
    t = topic.lower()
    for c, keys in _CATS:
        if any(k in t for k in keys):
            return c
    return "general"

def _vendors(topic: str) -> List[str]:
    t = topic.lower()
    found = []
    for name, keys in [
        ("cisco", "cisco ios nx-os vlan ospf bgp stp hsrp acl catalyst"),
        ("mikrotik", "mikrotik routeros"),
        ("fortigate", "forti fortigate fortinet"),
        ("windows", "windows powershell gpo active directory kerberos"),
        ("linux", "linux bash iptables nftables systemd"),
        ("vmware", "vmware esxi vcenter"),
        ("wireless", "wifi wireless wlc ssid"),
    ]:
        if any(k in t for k in keys.split()):
            found.append(name)
    d = {"vlan": ["cisco", "mikrotik"], "ospf": ["cisco", "mikrotik", "linux"], "bgp": ["cisco", "linux"],
         "firewall": ["fortigate", "linux"], "linux": ["linux"], "windows": ["windows"], "vpn": ["cisco", "fortigate"]}
    return found or d.get(_cat(topic), ["cisco", "linux", "windows"])

def _fmt_cmds(pairs):
    lines = []
    for cmd, desc in pairs:
        lines.append(f"```\n{cmd}\n```\n→ {desc}\n")
    return "\n".join(lines)

def _commands_block(cat, topic, vendors, level):
    lines = [
        f"# دستورات عمیق — {topic} | {level} | {cat}",
        "",
        "## پایه و Verify",
        _fmt_cmds(COMMON),
        f"## تخصصی {cat}",
        _fmt_cmds(BANKS.get(cat, BANKS.get("linux", [])[:15])),
    ]
    if "mikrotik" in vendors and cat not in BANKS:
        lines += ["## MikroTik", _fmt_cmds([
            ("/ip address print", "آدرس"), ("/ip route print", "مسیر"),
            ("/log print without-paging", "لاگ"), ("/system resource print", "منبع"),
        ])]
    if level in ("L3", "L4"):
        lines += ["## Engineer — Capture", _fmt_cmds([
            ("show running-config | redirect flash:pre-change.cfg", "backup قبل change"),
            ("monitor capture CAP interface GigabitEthernet0/0 both match any", "EPC"),
            ("monitor capture CAP start", "start capture"),
            ("monitor capture CAP stop", "stop"),
            ("show monitor capture CAP buffer brief", "buffer"),
            ("tcpdump -i any -nn -w /tmp/lab.pcap host 10.10.10.10 -c 200", "pcap لینوکس"),
        ])]
    lines += ["## Verify E2E", _fmt_cmds([
        ("ping 10.0.0.1 repeat 20", "تست پایدار"),
        ("traceroute 10.0.0.1", "مسیر"),
        ("show logging | include %LINK|%LINEPROTO|%OSPF|%BGP|%HSRP", "رویدادها"),
    ]), "## Rollback",
        "```\nconfigure terminal\n! دستورات معکوس Runbook\nend\ncopy running-config startup-config\n```\n→ برگشت + ذخیره\n"]
    return "\n".join(lines)

def _errors_md(cat, topic):
    rows = ERRORS.get(cat, [
        (f"سرویس {topic} قطع", "ایزوله L1→L7", "ping / show interface / traceroute"),
        ("بعد reboot برگشت", "startup≠running", "show startup-config"),
    ])
    lines = [f"\n## عیب‌یابی — {topic}\n", "| علامت | علت | اقدام |", "|---|---|---|"]
    for a,b,c in rows:
        lines.append(f"| {a} | {b} | `{c}` |")
    lines.append("""
### RCA اجباری L2+
1. Symptom 2. Scope 3. Evidence (log/capture/counter) 4. Hypothesis OSI
5. Test 6. Fix + backup 7. Verify کلاینت 8. Document Runbook
""")
    return "\n".join(lines)

def build_rich_lesson(title_fa: str, title_en: str = "", level: str | None = None) -> Dict[str, Any]:
    level = level or level_tag(title_fa)
    topic = clean_topic(title_fa)
    cat = _cat(topic)
    vendors = _vendors(topic)
    level_name = _LEVEL_FA.get(level, level)
    summary = (
        f"«{topic}» ({level} — {level_name}): معماری، پروتکل، دستورات عمیق چند‌وندر "
        f"({', '.join(vendors)})، جدول خطا، Lab، امنیت و RCA."
    )
    depth = {
        "L0": "مفهوم و show پایه",
        "L1": "پیکربندی Lab و Verify",
        "L2": "Configure→Verify→Troubleshoot→Document",
        "L3": "طراحی، failure domain، capture پیشرفته",
        "L4": "معماری چندسایته و Runbook سازمانی",
    }.get(level, "")

    arch = f"""
## معماری
```
[Client] → [Access] → [{topic}] → [Core/WAN] → [Service]
```
Control Plane در برابر Data Plane را جدا تحلیل کنید.
"""
    proto = f"""
## پروتکل و هدر — {topic}
| لایه | نقش | ابزار |
|------|-----|-------|
| L1 | مدیا/SFP | show interface, ethtool |
| L2 | MAC/VLAN/STP | show vlan, Wireshark |
| L3 | IP/Route | show ip route, ping |
| L4 | TCP/UDP | ss, netstat |
| L7 | DNS/HTTP/AAA | dig, logs |

```
Ethernet: DstMAC|SrcMAC|EtherType|Payload|FCS
802.1Q: TPID=0x8100|PCP|DEI|VLAN-ID
IPv4: Ver|IHL|TOS|Len|ID|Flags|Frag|TTL|Proto|Csum|Src|Dst
TCP: Sport|Dport|Seq|Ack|Flags|Win|Csum
```
فیلتر Wireshark: `vlan.id==10` · `ip.addr==10.10.10.10` · `tcp.flags.syn==1`
"""
    lab = f"""
## Lab — {topic}
### توپولوژی
```
[PC-A]--[Access SW]==trunk==[Dist/Router/FW]--[WAN]
```
### اهداف
1. Backup اولیه 2. پیکربندی {topic} 3. Verify از کلاینت
4. Fail عمدی 5. تشخیص با capture 6. Rollback Runbook

### Checklist
- [ ] copy run tftp یا archive
- [ ] نقطه SPAN/tcpdump آماده
- [ ] کلاینت تست مشخص

### Capture
```
tcpdump -i eth0 -nn -w /tmp/{cat}.pcap host 10.10.10.10
monitor capture CAP interface Gi0/0 both match any
monitor capture CAP start
```
"""
    sec = f"""
## امنیت — {topic}
- MGMT جدا (VRF/OOB)
- AAA RADIUS/TACACS+
- فقط SSH/HTTPS
- SNMPv3، NTP، syslog مرکزی
- ACL روی vty
- backup + peer review قبل از change
"""
    sources = [
        ("Cisco Docs", "https://www.cisco.com/c/en/us/support/index.html"),
        ("RFC Editor", "https://www.rfc-editor.org/"),
        ("MikroTik Wiki", "https://wiki.mikrotik.com/"),
        ("Fortinet Docs", "https://docs.fortinet.com/"),
        ("Microsoft Learn", "https://learn.microsoft.com/"),
        ("Linux man-pages", "https://man7.org/linux/man-pages/"),
        ("Wireshark Wiki", "https://wiki.wireshark.org/"),
        ("IANA", "https://www.iana.org/assignments/"),
        ("NIST SP 800", "https://csrc.nist.gov/publications/sp800"),
        ("NetworkLessons", "https://networklessons.com/"),
    ]
    src_md = "## منابع رسمی\n" + "\n".join(f"- [{a}]({b})" for a,b in sources)

    full = "\n".join([
        f"# {topic}",
        f"**سطح:** {level} — {level_name}",
        f"**EN:** {title_en or topic}",
        f"**دسته:** {cat} | **Vendors:** {', '.join(vendors)}",
        f"**عمق سطح:** {depth}",
        "",
        "## خلاصه اجرایی", summary, "",
        "## تعریف و مرز",
        f"«{topic}» را در Access/Distribution/Core/Edge/DC قرار دهید. مرز با L1–L7 و Identity را روشن کنید.",
        arch, proto, _errors_md(cat, topic), lab, sec,
        "## اهداف یادگیری",
        f"1. معماری {topic}",
        "2. دستورات Configure/Verify عمیق",
        "3. عیب‌یابی با شواهد",
        "4. Lab و Runbook",
        "5. Hardening",
        "", src_md,
    ])
    commands = _commands_block(cat, topic, vendors, level)
    return {
        "summary": summary,
        "full_content": full,
        "commands": commands,
        "examples": lab,
        "notes": f"دسته={cat} | سطح={level} | دستورات چند‌وندر + RCA",
        "level": level, "topic": topic, "category": cat,
        "learning_objectives": [f"معماری {topic}", "دستورات عمیق", "عیب‌یابی", "Lab/Runbook", "امنیت"],
    }
