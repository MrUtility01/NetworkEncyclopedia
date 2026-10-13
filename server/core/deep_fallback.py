# -*- coding: utf-8 -*-
"""کتاب جامع برای هر درس — نمودار، دستورات گسترده، مثال، Lab، RCA."""
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
        (("window", "active directory", "gpo", "powershell", "dns server", "batch"), "windows"),
        (("backup", "snapshot", "restore", "dr ", "rpo", "rto"), "backup"),
        (("sdn", "sd-wan", "overlay", "underlay", "controller", "vxlan"), "sdn"),
        (("fortigate", "fortinet", "fortios"), "fortigate"),
        (("pfsense", "opnsense", "issabel", "asterisk", "sip", "voip"), "edge_apps"),
        (("mpls", "label", "l3vpn", "l2vpn", "vrf"), "mpls"),
        (("ipv6", "slaac", "ndp", "ra ", "dad"), "ipv6"),
    ]
    for keys, cat in rules:
        if any(k in t for k in keys):
            return cat
    return "general"

def _level_depth(level: str) -> str:
    return {
        "L0": "آشنایی",
        "L1": "مقدماتی",
        "L2": "ادمین",
        "L3": "مهندس",
        "L4": "خبره",
    }.get(level, "عمومی")

def _diagrams(topic: str, cat: str) -> str:
    t = topic.replace("<", "").replace(">", "")[:40]
    topo = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 160" width="100%" '
        'style="max-width:640px;background:#f8fafc;border-radius:8px">'
        '<rect x="10" y="50" width="90" height="50" rx="8" fill="#dbeafe" stroke="#2563eb"/>'
        '<text x="55" y="80" text-anchor="middle" font-size="12" fill="#1e3a8a">Client</text>'
        '<line x1="100" y1="75" x2="140" y2="75" stroke="#64748b" stroke-width="2"/>'
        '<rect x="140" y="50" width="100" height="50" rx="8" fill="#dcfce7" stroke="#16a34a"/>'
        '<text x="190" y="80" text-anchor="middle" font-size="12" fill="#14532d">Access</text>'
        '<line x1="240" y1="75" x2="280" y2="75" stroke="#64748b" stroke-width="2"/>'
        '<rect x="280" y="50" width="110" height="50" rx="8" fill="#fef9c3" stroke="#ca8a04"/>'
        '<text x="335" y="80" text-anchor="middle" font-size="12" fill="#713f12">L3/Core</text>'
        '<line x1="390" y1="75" x2="430" y2="75" stroke="#64748b" stroke-width="2"/>'
        '<rect x="430" y="50" width="100" height="50" rx="8" fill="#ffe4e6" stroke="#e11d48"/>'
        '<text x="480" y="80" text-anchor="middle" font-size="12" fill="#881337">Edge/FW</text>'
        '<line x1="530" y1="75" x2="570" y2="75" stroke="#64748b" stroke-width="2"/>'
        '<rect x="570" y="50" width="60" height="50" rx="8" fill="#ede9fe" stroke="#7c3aed"/>'
        '<text x="600" y="80" text-anchor="middle" font-size="11" fill="#4c1d95">WAN</text>'
        f'<text x="320" y="28" text-anchor="middle" font-size="13" fill="#0f172a">Topology: {t}</text>'
        '</svg>'
    )
    flow = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 110" width="100%" '
        'style="max-width:640px;background:#f8fafc;border-radius:8px">'
        '<rect x="20" y="35" width="100" height="44" rx="8" fill="#e0f2fe" stroke="#0284c7"/>'
        '<text x="70" y="62" text-anchor="middle" font-size="12">Baseline</text>'
        '<text x="130" y="62" font-size="16" fill="#64748b">-></text>'
        '<rect x="150" y="35" width="100" height="44" rx="8" fill="#dcfce7" stroke="#16a34a"/>'
        '<text x="200" y="62" text-anchor="middle" font-size="12">Config</text>'
        '<text x="260" y="62" font-size="16" fill="#64748b">-></text>'
        '<rect x="280" y="35" width="100" height="44" rx="8" fill="#fef9c3" stroke="#ca8a04"/>'
        '<text x="330" y="62" text-anchor="middle" font-size="12">Verify</text>'
        '<text x="390" y="62" font-size="16" fill="#64748b">-></text>'
        '<rect x="410" y="35" width="100" height="44" rx="8" fill="#ffe4e6" stroke="#e11d48"/>'
        '<text x="460" y="62" text-anchor="middle" font-size="12">Monitor</text>'
        '<text x="520" y="62" font-size="16" fill="#64748b">-></text>'
        '<rect x="540" y="35" width="80" height="44" rx="8" fill="#ede9fe" stroke="#7c3aed"/>'
        '<text x="580" y="62" text-anchor="middle" font-size="12">RCA</text>'
        '</svg>'
    )
    return "### نمودار توپولوژی\n" + topo + "\n\n### نمودار چرخه کار\n" + flow + "\n"

def _vendor_cmds(topic: str, cat: str) -> str:
    blocks = []
    blocks.append(f"""### Cisco IOS/IOS-XE — {topic}
```
terminal length 0
show running-config
show startup-config
show version
show ip interface brief
show interfaces status
show interfaces counters errors
show ip route
show ip cef
show ip protocols
show logging | last 80
show processes cpu sorted | exclude 0.00
copy running-config startup-config
ping <gateway> repeat 20
ping 8.8.8.8 repeat 20
traceroute 1.1.1.1
show ip arp
show mac address-table
show vlan brief
show interfaces trunk
show spanning-tree summary
show access-lists
show ip nat translations
show crypto isakmp sa
show crypto ipsec sa
show ip ospf neighbor
show ip bgp summary
show etherchannel summary
show cdp neighbors detail
show ip dhcp binding
show standby brief
```""")
    blocks.append(f"""### MikroTik RouterOS — {topic}
```
/system resource print
/interface print detail
/interface bridge print
/interface vlan print
/ip address print
/ip route print detail
/ip arp print
/ip dns print
/ip dhcp-server print
/ip dhcp-server lease print
/ip firewall filter print without-paging
/ip firewall filter print stats
/ip firewall nat print without-paging
/ip firewall mangle print without-paging
/ip firewall raw print without-paging
/ip firewall connection print
/ip firewall address-list print
/queue simple print
/queue tree print
/ip service print
/export file=backup-before-change
/ping 8.8.8.8 count=20
/tool traceroute 1.1.1.1
/tool torch interface=ether1
/tool sniffer quick interface=ether1 port=53
/interface wireguard print
/ip ipsec active-peers print
/routing ospf neighbor print
/interface bridge vlan print
/interface bridge port print
```""")
    blocks.append(f"""### FortiGate FortiOS — {topic}
```
get system status
get system performance status
get system interface physical
get router info routing-table all
show router static
show firewall policy
show firewall vip
show firewall ippool
show firewall address
diagnose sys session list
diagnose firewall iprope lookup 10.10.10.50 8.8.8.8 1 443
execute ping 8.8.8.8
execute traceroute 1.1.1.1
execute log display
diagnose debug flow filter saddr 10.10.10.50
diagnose debug flow show console enable
diagnose debug enable
diagnose debug flow trace start 50
diagnose debug disable
diagnose sniffer packet any "host 10.10.10.50" 4 30
diagnose sys sdwan health-check
diagnose vpn ike gateway list
diagnose vpn tunnel list
get system ha status
```""")
    blocks.append(f"""### Linux — {topic}
```
ip -br a
ip -br link
ip route show table all
ip rule show
ss -tulpn
ss -s
ping -c 20 8.8.8.8
traceroute -n 1.1.1.1
mtr -r -c 20 1.1.1.1
dig example.com +short
resolvectl status
nft list ruleset
iptables -L -n -v
sysctl net.ipv4.ip_forward
journalctl -u NetworkManager -n 100 --no-pager
tcpdump -ni any icmp -c 40
tcpdump -ni any port 53 -c 40
```""")
    blocks.append(f"""### Windows PowerShell / Batch — {topic}
```
Get-NetIPConfiguration | Format-List
Get-NetIPAddress | Format-Table
Get-NetRoute -AddressFamily IPv4 | Format-Table
Get-DnsClientServerAddress
Get-NetAdapter | Format-Table Name, Status, LinkSpeed
Test-NetConnection 8.8.8.8 -InformationLevel Detailed
Test-NetConnection example.com -Port 443
Resolve-DnsName example.com -Type A
Get-NetFirewallProfile
Get-NetTCPConnection -State Established | Select-Object -First 30
Test-ComputerSecureChannel -Verbose
ipconfig /all
ipconfig /flushdns
arp -a
route print
netstat -ano
netsh interface ip show config
netsh wlan show interfaces
netsh advfirewall show allprofiles
```
```
@echo off
set GW=10.10.10.1
ping -n 2 %GW% >nul && echo GW OK || echo GW DOWN
ping -n 2 8.8.8.8 >nul && echo WAN OK || echo WAN DOWN
```""")
    if cat == "edge_apps" or "sip" in topic.lower() or "issabel" in topic.lower():
        blocks.append(f"""### Issabel / Asterisk — {topic}
```
asterisk -rvvv
sip show peers
sip show registry
pjsip show endpoints
core show channels
rtp set debug on
tcpdump -ni any port 5060
tcpdump -ni any udp portrange 10000-20000
systemctl status asterisk
tail -f /var/log/asterisk/full
```""")
    return "\n\n".join(blocks)

def _extra_examples(topic: str) -> str:
    return f"""## مثال‌های حل‌شده بیشتر — {topic}

### مثال ۱ دفتر ۲۰ نفره
علائم: اینترنت هست، سرور داخلی نه.
فرضیه: ACL/policy بین VLAN کاربر و سرور.
اقدام: پینگ GW -> پینگ سرور -> بررسی policy -> اصلاح -> Verify.

### مثال ۲ شعبه VPN
علائم: تونل up، فایل‌شرینگ قطع.
فرضیه: interesting traffic / NAT روی تونل / DNS.
اقدام: SA -> route مرکز -> DNS داخلی -> تست SMB.

### مثال ۳ Wi-Fi ناقص
علائم: بعضی موبایل‌ها IP نمی‌گیرند.
فرضیه: pool پر / scope / isolation.
اقدام: lease -> scope -> لاگ DHCP -> کلاینت جدید.

### مثال ۴ بعد از change خراب
Rollback فوری -> diff -> اعمال مرحله‌ای با Verify.

### مثال ۵ کندی بدون قطعی
errors اینترفیس -> latency GW و 1.1.1.1 -> زمان DNS.
"""

def _book_body(topic: str, cat: str, level: str) -> str:
    L = level or "L0"
    parts: List[str] = []
    parts.append(f"# کتاب جامع: {topic}\n\n**سطح:** {L} — {_level_depth(L)} | **دسته:** `{cat}`\n\n---\n")
    parts.append(f"## فصل ۱ — چرا «{topic}» حیاتی است؟\n\nقطع کامل / قطع جزئی / کندی / حفره امنیتی.\n\nقبل از تغییر: دامنه اثر | معیار موفقیت | Rollback\n\n---\n")
    parts.append(f"## فصل ۲ — واژه‌نامه\n\nInterface | Policy | Session | Control/Data Plane | Baseline | Verify | Rollback | Failure Domain\n\n---\n")
    parts.append(f"## فصل ۳ — معماری و نمودار\n\n```\nClient -> Access -> L3/Core -> Edge/FW -> WAN\n```\n\n{_diagrams(topic, cat)}\n\n---\n")
    parts.append(f"## فصل ۴ — مبانی\n\n«{topic}» قرارداد مجاز/ممنوع/پیش‌فرض است.\nلایه: فیزیک -> L2 -> L3 -> Transport -> Policy\n\n---\n")
    parts.append(f"## فصل ۵ — پیکربندی\n\nA Baseline  B Config حداقلی  C Verify دستگاه+کلاینت  D مانیتور و مستند\n\n---\n")
    parts.append(f"## فصل ۶ — دستورات چندسکو\n\n{_vendor_cmds(topic, cat)}\n\n---\n")
    parts.append(f"## فصل ۷ — سناریوها\n\nدفتر کوچک | شرکت چندطبقه | چندسایت VPN/SD-WAN\n\n---\n")
    parts.append(f"## فصل ۸ — Lab\n\nLab A پیاده‌سازی | Lab B خراب‌کاری RCA | Lab C بار | Lab D مستند\n\n---\n")
    parts.append(f"## فصل ۹ — عیب‌یابی\n\nعلامت -> احتمال -> اقدام اول\nRCA: علامت | آخرین change | لایه به لایه | یک فرضیه | مانیتور\n\n---\n")
    parts.append(f"## فصل ۱۰ — امنیت\n\nLeast Privilege | مدیریت از شبکه مدیریت | لاگ | Backup خارج دستگاه\n\n---\n")
    parts.append(f"## فصل ۱۱ — مقیاس\n\nFailure Domain | HA | Shared Fate | Observability\n\n---\n")
    parts.append(f"## فصل ۱۲ — Trade-off و مصاحبه\n\nسادگی در برابر انعطاف | Policy ریز | اتوماسیون | SLO\n\n---\n")
    parts.append(f"## فصل ۱۳ — ضدالگوها\n\nبدون Baseline | Verify فقط دستگاه | NAT روی تونل | DNS عمومی روی AD | FastTrack | ترتیب ACL | MTU VPN\n\n---\n")
    parts.append(f"## فصل ۱۴ — آزمون\n\nBaseline اول؟ Verify خوب؟ Failure Domain؟ RCA بعد change؟\n\n---\n")
    parts.append(_extra_examples(topic))
    parts.append(f"## فصل ۱۵ — چک‌لیست\n\nقبل: توپولوژی IP Backup معیار | بعد: Verify کلاینت لاگ مانیتور مستند\n\n**سطح:** {_level_depth(L)}\n")
    return "\n".join(parts)

def _commands_book(topic: str, cat: str, level: str) -> str:
    return f"# مرجع دستورات «{topic}»\n\n{_vendor_cmds(topic, cat)}\n"

def _lab_book(topic: str, cat: str, level: str) -> str:
    return f"""# Lab — {topic}

## Lab1 پایه: توپولوژی -> Config -> Verify دستگاه/کلاینت
## Lab2 RCA: اشتباه عمدی -> ماتریس -> Rollback
## Lab3 پایداری: بار -> CPU/Session
## Lab4 چندسکو: Cisco / MikroTik / FortiGate / Linux
"""

def _notes_book(topic: str, cat: str, level: str) -> str:
    return f"# RCA — {topic}\n\n1 علامت 2 آخرین change 3 لایه به لایه 4 یک فرضیه 5 مانیتور\n"

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
    body = _book_body(topic, cat, level)
    if spec.get("extra_full"):
        body += "\n\n---\n## پیوست تخصصی\n" + spec["extra_full"]
    commands = _commands_book(topic, cat, level)
    if spec.get("extra_commands"):
        commands += "\n\n" + spec["extra_commands"]
    examples = _lab_book(topic, cat, level) + "\n" + _extra_examples(topic)
    if spec.get("extra_lab"):
        examples += "\n\n" + spec["extra_lab"]
    notes = _notes_book(topic, cat, level)
    if spec.get("extra_notes"):
        notes += "\n\n" + spec["extra_notes"]
    return {
        "summary": f"کتاب «{topic}» | {level} — {_level_depth(level)} | نمودار+دستورات چندسکو+Lab+RCA",
        "full_content": body,
        "commands": commands,
        "examples": examples,
        "notes": notes,
        "level": level,
        "topic": topic,
        "category": cat,
    }
