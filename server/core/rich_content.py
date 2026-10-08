# -*- coding: utf-8 -*-
"""محتوای عمیق: دستورات واقعی، عیب‌یابی، خطاهای رایج، منابع رسمی."""
from __future__ import annotations
import re
from typing import Any, Dict, List, Tuple

def level_tag(title: str) -> str:
    m = re.match(r"\[(L[0-4])\]", title or "")
    return m.group(1) if m else "L0"

def clean_topic(title: str) -> str:
    t = re.sub(r"^\[L[0-4]\]\s*", "", title or "").strip()
    t = re.sub(r"\s*[—\-]\s*(آشنایی|مقدماتی|ادمین|مهندس|خبره|Intro|Junior|Admin|Senior|Architect)\s*$", "", t, flags=re.I)
    return t.strip() or (title or "موضوع")

_LEVEL_FA = {"L0": "آشنایی", "L1": "Junior", "L2": "Admin", "L3": "Senior", "L4": "Architect"}

_CATS: List[Tuple[str, List[str]]] = [
    ("vlan", ["vlan", "trunk", "access", "802.1q", "سگمنت"]),
    ("stp", ["stp", "spanning", "rstp", "bpdu", "loop"]),
    ("ospf", ["ospf", "area", "lsa", "dr"]),
    ("bgp", ["bgp", "as path", "prefix-list", "ebgp", "ibgp"]),
    ("acl", ["acl", "access-list", "filter"]),
    ("nat", ["nat", "pat", "overload", "snat"]),
    ("vpn", ["vpn", "ipsec", "ike", "tunnel"]),
    ("dhcp", ["dhcp", "scope", "lease", "relay"]),
    ("dns", ["dns", "resolver", "zone"]),
    ("firewall", ["firewall", "fortigate", "policy", "utm"]),
    ("ha", ["hsrp", "vrrp", "ha", "failover"]),
    ("qos", ["qos", "dscp", "policing", "shaping"]),
    ("linux", ["linux", "iptables", "nftables", "systemd"]),
    ("windows", ["windows", "powershell", "gpo", "kerberos"]),
    ("wireless", ["wifi", "wireless", "ssid", "wlc"]),
    ("storage", ["raid", "nvme", "ssd", "iops"]),
    ("boot", ["bios", "uefi", "boot", "pxe"]),
]

def _cat(topic: str) -> str:
    t = topic.lower()
    for c, keys in _CATS:
        if any(k in t for k in keys):
            return c
    return "general"

def _vendors(topic: str) -> List[str]:
    t = topic.lower()
    out = []
    for name, keys in [
        ("cisco", "cisco ios vlan ospf bgp stp hsrp acl"),
        ("mikrotik", "mikrotik routeros"),
        ("fortigate", "forti fortigate"),
        ("windows", "windows powershell gpo active directory"),
        ("linux", "linux bash iptables nftables"),
    ]:
        if any(k in t for k in keys.split()):
            out.append(name)
    return out or ["cisco", "linux", "windows"]

_CMDS = {
    "vlan": [("show vlan brief", "لیست VLAN"), ("show interfaces trunk", "ترانک‌ها"), ("vlan 10", "ایجاد VLAN"), ("name USERS", "نام VLAN"), ("switchport mode access", "حالت access"), ("switchport access vlan 10", "عضویت VLAN 10"), ("switchport mode trunk", "ترانک"), ("switchport trunk allowed vlan 10,20,30", "VLANهای مجاز"), ("show mac address-table vlan 10", "جدول MAC")],
    "ospf": [("show ip ospf neighbor", "همسایه‌ها"), ("show ip ospf database", "LSA DB"), ("show ip route ospf", "مسیرهای OSPF"), ("router ospf 1", "فرآیند OSPF"), ("router-id 1.1.1.1", "Router-ID"), ("network 10.0.0.0 0.0.0.255 area 0", "اعلان Area 0"), ("passive-interface default", "Passive پیش‌فرض")],
    "bgp": [("show ip bgp summary", "خلاصه peer"), ("show ip bgp", "جدول BGP"), ("router bgp 65001", "فرآیند BGP"), ("neighbor 203.0.113.2 remote-as 65002", "eBGP peer"), ("network 192.0.2.0 mask 255.255.255.0", "اعلان پیشوند")],
    "nat": [("show ip nat translations", "جدول NAT"), ("show ip nat statistics", "آمار"), ("ip nat inside source list NAT-ACL interface Gi0/0 overload", "PAT"), ("ip nat inside", "علامت inside"), ("ip nat outside", "علامت outside")],
    "vpn": [("show crypto isakmp sa", "Phase-1"), ("show crypto ipsec sa", "Phase-2"), ("crypto isakmp policy 10", "سیاست IKE"), ("encryption aes", "AES"), ("hash sha256", "SHA256")],
    "dhcp": [("show ip dhcp binding", "Leaseها"), ("show ip dhcp pool", "Poolها"), ("ip dhcp pool USERS", "ایجاد pool"), ("network 10.0.0.0 255.255.255.0", "شبکه"), ("default-router 10.0.0.1", "Gateway"), ("ip helper-address 10.0.0.10", "Relay")],
    "stp": [("show spanning-tree", "وضعیت STP"), ("spanning-tree mode rapid-pvst", "Rapid-PVST"), ("spanning-tree portfast", "PortFast"), ("spanning-tree bpduguard enable", "BPDU Guard")],
    "firewall": [("get system status", "وضعیت Forti"), ("show firewall policy", "سیاست‌ها"), ("diagnose sniffer packet any 'host 10.10.10.10' 4 50 l", "اسنیفر"), ("diagnose debug flow trace start 50", "flow debug")],
    "linux": [("ip -br a", "آدرس‌ها"), ("ss -tulpn", "سوکت‌ها"), ("journalctl -xe -n 100", "لاگ"), ("nft list ruleset", "nftables"), ("tcpdump -i any -nn -c 30", "capture")],
    "windows": [("ipconfig /all", "IP کامل"), ("Test-NetConnection 8.8.8.8 -Port 443", "تست پورت"), ("gpresult /r", "نتیجه GPO"), ("Get-NetRoute", "مسیرها")],
    "ha": [("show standby brief", "HSRP"), ("standby 1 ip 10.0.0.1", "VIP"), ("standby 1 priority 110", "اولویت"), ("standby 1 preempt", "Preempt")],
}

_ERRORS = {
    "vlan": [("کلاینت VLAN اشتباه", "access vlan / native", "show vlan brief"), ("ترانک down", "mode و allowed یکسان", "show interfaces trunk")],
    "ospf": [("Neighbor نه full", "area/timer/MTU", "show ip ospf neighbor"), ("مسیر نیست", "LSA/filter", "show ip ospf database")],
    "bgp": [("Idle/Active", "TCP 179 / AS", "show ip bgp summary"), ("اعلان نمی‌شود", "network/route-map", "show ip bgp")],
    "nat": [("بدون translation", "inside/outside و ACL", "show ip nat statistics")],
    "dhcp": [("APIPA", "relay/pool/excluded", "show ip dhcp binding")],
    "vpn": [("Phase1 down", "PSK/proposal/UDP500", "show crypto isakmp sa")],
    "firewall": [("policy hit=0", "ترتیب/آدرس/پورت", "diagnose debug flow")],
    "linux": [("سرویس down", "systemctl/journal", "journalctl -u SERVICE")],
    "windows": [("GPO اعمال نشد", "OU/link/gpupdate", "gpresult /r")],
}

_COMMON = [("show version", "نسخه و uptime"), ("show running-config", "پیکربندی فعال"), ("show ip interface brief", "IP اینترفیس‌ها"), ("show logging", "لاگ"), ("copy running-config startup-config", "ذخیره")]

_SOURCES = [
    {"title": "Cisco Documentation", "url": "https://www.cisco.com/c/en/us/support/index.html", "note": "راهنمای رسمی Cisco"},
    {"title": "RFC Editor", "url": "https://www.rfc-editor.org/", "note": "استانداردهای IETF"},
    {"title": "MikroTik Wiki", "url": "https://wiki.mikrotik.com/", "note": "RouterOS"},
    {"title": "Fortinet Docs", "url": "https://docs.fortinet.com/", "note": "FortiGate"},
    {"title": "Microsoft Learn", "url": "https://learn.microsoft.com/", "note": "Windows/AD"},
    {"title": "Linux man-pages", "url": "https://man7.org/linux/man-pages/", "note": "دستورات Linux"},
    {"title": "Wireshark Wiki", "url": "https://wiki.wireshark.org/", "note": "پروتکل و capture"},
    {"title": "IANA", "url": "https://www.iana.org/assignments/", "note": "شماره پروتکل/پورت"},
    {"title": "NIST SP 800", "url": "https://csrc.nist.gov/publications/sp800", "note": "امنیت"},
    {"title": "Cloudflare Learning", "url": "https://www.cloudflare.com/learning/", "note": "DNS/TLS"},
    {"title": "NetworkLessons", "url": "https://networklessons.com/", "note": "آموزش عملی"},
    {"title": "Packet Life", "url": "https://packetlife.net/library/cheat-sheets/", "note": "Cheat sheet"},
]

def build_rich_lesson(title_fa: str, title_en: str = "", level: str | None = None) -> Dict[str, Any]:
    level = level or level_tag(title_fa)
    topic = clean_topic(title_fa)
    cat = _cat(topic)
    vendors = _vendors(topic)
    level_name = _LEVEL_FA.get(level, level)
    summary = f"«{topic}» ({level} — {level_name}): معماری، دستورات چند‌وندر، عیب‌یابی خطاهای رایج، Lab و منابع رسمی. Vendors: {', '.join(vendors)}."

    cmds = list(_COMMON) + list(_CMDS.get(cat, _CMDS.get("linux", [])))
    if "mikrotik" in vendors or cat in ("vlan", "ospf", "nat"):
        cmds += [("/ip address print", "آدرس ROS"), ("/ip route print", "مسیر ROS"), ("/log print", "لاگ ROS")]
    cmd_txt = [f"# دستورات — {topic} ({cat})", ""]
    for c, d in cmds:
        cmd_txt += [f"```\n{c}\n```", f"→ {d}\n"]
    cmd_txt += ["## Verify", "```\nping 10.0.0.1 repeat 5\ntraceroute 10.0.0.1\nshow ip route\n```", "## Rollback", "```\nconfigure terminal\n! دستورات معکوس Runbook\nend\ncopy running-config startup-config\n```"]

    errs = _ERRORS.get(cat, [("سرویس قطع", "ایزوله OSI از L1", "ping / show interface")])
    err_lines = [f"\n## عیب‌یابی — {topic}\n", "| علامت | علت | اقدام |", "|---|---|---|"]
    for a, b, c in errs:
        err_lines.append(f"| {a} | {b} | `{c}` |")
    err_lines.append("\n### RCA: Symptom→Scope→Evidence→RootCause→Fix→Verify→Document\n")

    parts = [
        f"# {topic}\n**سطح:** {level} — {level_name}\n**دسته:** {cat}\n**Vendors:** {', '.join(vendors)}\n\n",
        "## خلاصه\n" + summary + "\n\n",
        "## معماری\nAccess → Distribution/Policy → Core/WAN → Service\n\n",
        f"## دیاگرام\n```\n[Client] → [Access] → [{topic}] → [Core] → [Service]\n```\n\n",
        "## پروتکل\nEthernet/802.1Q/IPv4/TCP — capture با Wireshark/tshark/tcpdump/SPAN\n\n",
        "".join(err_lines),
        f"## مثال Lab\n1) توپولوژی مینیمال برای «{topic}»\n2) Backup قبل از change\n3) Configure → Verify → Fail عمدی → Fix\n4) مستند Runbook\n\n",
        "## امنیت\nMGMT جدا، AAA، syslog، NTP، حداقل privilege، بدون Telnet/HTTP plain\n\n",
        "## منابع رسمی\n",
    ]
    for s in _SOURCES:
        parts.append(f"- [{s['title']}]({s['url']}) — {s['note']}\n")

    return {
        "summary": summary,
        "full_content": "".join(parts),
        "commands": "\n".join(cmd_txt),
        "examples": f"Lab + capture + Verify برای «{topic}»",
        "notes": f"دسته={cat} | منابع در تنظیمات برنامه قابل ویرایش",
        "level": level,
        "topic": topic,
        "category": cat,
        "sources": _SOURCES,
        "learning_objectives": [f"معماری {topic}", "Configure/Verify", "عیب‌یابی با شواهد", "Runbook و Rollback"],
    }
