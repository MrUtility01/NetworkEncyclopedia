# -*- coding: utf-8 -*-
"""کتابخانه اینفوگرافیک SVG — حداقل ۱۰۰ نمودار آموزشی شبکه."""
from __future__ import annotations
from typing import Dict, List, Tuple


def _svg(inner: str, w: int = 720, h: int = 220, title: str = "") -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" '
        f'style="max-width:{w}px;background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;margin:12px 0">'
        f'<defs><marker id="m" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">'
        f'<path d="M0,0 L6,3 L0,6 Z" fill="#64748b"/></marker></defs>'
        f'<text x="16" y="22" font-family="Tahoma,sans-serif" font-size="13" fill="#0f172a" font-weight="bold">{title}</text>'
        f"{inner}</svg>"
    )


def _box(x, y, w, h, label, color="#2563eb"):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{color}" opacity="0.14" stroke="{color}" stroke-width="2"/>'
        f'<text x="{x + w // 2}" y="{y + h // 2 + 5}" text-anchor="middle" font-family="Tahoma,sans-serif" font-size="11" fill="#0f172a">{label}</text>'
    )


def _line(x1, y1, x2, y2, lab=""):
    s = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#64748b" stroke-width="2" marker-end="url(#m)"/>'
    if lab:
        s += f'<text x="{(x1 + x2) // 2}" y="{min(y1, y2) - 8}" text-anchor="middle" font-family="Tahoma,sans-serif" font-size="10" fill="#64748b">{lab}</text>'
    return s


def _note(y, text):
    return f'<text x="16" y="{y}" font-family="Tahoma,sans-serif" font-size="11" fill="#475569">{text}</text>'


def _flow(title: str, boxes, notes, w=720, h=210):
    n = len(boxes)
    bw = min(120, max(70, (w - 40 - (n - 1) * 20) // max(n, 1)))
    gap = (w - 40 - n * bw) // max(n - 1, 1) if n > 1 else 0
    parts = []
    xs = []
    x = 20
    for label, color in boxes:
        parts.append(_box(x, 60, bw, 48, label, color))
        xs.append(x)
        x += bw + gap
    for i in range(n - 1):
        parts.append(_line(xs[i] + bw, 84, xs[i + 1], 84))
    y = 140
    for t in notes:
        parts.append(_note(y, t))
        y += 22
    return _svg("".join(parts), w, max(h, y + 10), title)


COLORS = ["#0ea5e9", "#8b5cf6", "#2563eb", "#f59e0b", "#16a34a", "#dc2626", "#6366f1", "#64748b"]


def _catalog() -> List[Tuple[str, list, list]]:
    C = COLORS
    items = [
        ("مسیر پکت تا اینترنت", [("PC", C[0]), ("سوئیچ", C[1]), ("روتر", C[2]), ("FW", C[3]), ("ISP", C[4])], ["MAC→Route→NAT→WAN", "مثال: 10.10.10.50 → GW → Public → 8.8.8.8"]),
        ("مسیر وایرلس سازمانی", [("Client", C[0]), ("AP", C[1]), ("SW", C[2]), ("WLC", C[3]), ("GW", C[4])], ["802.11→Eth→CAPWAP", "SSID=Corp VLAN20"]),
        ("تصمیم سوئیچ L2", [("فریم", C[0]), ("MAC؟", C[3]), ("Unicast", C[4]), ("Flood", C[5])], ["Learning + Aging", "Unknown = Flood در VLAN"]),
        ("تصمیم روتر L3", [("IP", C[0]), ("Table", C[2]), ("Match", C[4]), ("Drop", C[5])], ["Longest prefix", "TTL-- و ARP next-hop"]),
        ("Encapsulation OSI", [("App", C[0]), ("L4", C[1]), ("L3", C[2]), ("L2", C[3]), ("L1", C[4])], ["بالا→پایین ارسال", "پایین→بالا دریافت"]),
        ("TCP Handshake", [("Client", C[0]), ("SYN", C[3]), ("SYN-ACK", C[2]), ("ACK", C[4])], ["سه‌مرحله‌ای", "سپس داده"]),
        ("ARP Request/Reply", [("HostA", C[0]), ("Flood", C[1]), ("HostB", C[4])], ["Who-has → is-at", "همان subnet"]),
        ("DHCP DORA", [("D", C[0]), ("O", C[3]), ("R", C[2]), ("A", C[4])], ["Discover Offer Request Ack", "Relay اگر VLAN دیگر"]),
        ("DNS Resolution", [("Client", C[0]), ("Resolver", C[1]), ("Root", C[3]), ("Auth", C[4])], ["Cache+TTL", "dig / nslookup"]),
        ("NAT/PAT", [("LAN", C[0]), ("NAT", C[3]), ("WAN", C[4])], ["چند داخل یک Public", "پورت یکتا"]),
        ("VLAN Access+Trunk", [("V10", C[0]), ("SW-A", C[2]), ("Trunk", C[3]), ("SW-B", C[2]), ("V20", C[1])], ["802.1Q tag", "Native بدون تگ"]),
        ("OSPF Areas", [("A1", C[0]), ("Area0", C[2]), ("A2", C[1])], ["همه به Backbone", "show ip ospf neighbor"]),
        ("BGP Multi-Home", [("ISP-A", C[0]), ("شرکت", C[2]), ("ISP-B", C[4])], ["eBGP دو طرف", "prefix-list سیاست"]),
        ("IPsec Site-to-Site", [("LAN-A", C[0]), ("GW-A", C[2]), ("Internet", C[7]), ("GW-B", C[2]), ("LAN-B", C[4])], ["Ph1 IKE / Ph2 IPsec", "interesting traffic"]),
        ("فایروال Zone", [("Trust", C[4]), ("FW", C[3]), ("DMZ", C[1]), ("Untrust", C[5])], ["Default deny", "specific→general"]),
        ("STP Loop Prevention", [("Root", C[4]), ("SW-A", C[2]), ("SW-B", C[2]), ("SW-C", C[2])], ["یک لینک Blocking", "BPDU Guard access"]),
        ("HSRP/VRRP", [("Client", C[0]), ("Active", C[4]), ("Standby", C[3]), ("VIP", C[1])], ["VIP مشترک", "preempt/priority"]),
        ("QoS صف", [("Mixed", C[7]), ("Voice", C[4]), ("Biz", C[2]), ("BE", C[3])], ["Classify Mark Queue", "EF برای صوت"]),
        ("UDP vs TCP", [("App", C[0]), ("UDP", C[3]), ("TCP", C[2]), ("Net", C[4])], ["UDP بی‌اتصال", "TCP قابل اعتماد"]),
        ("ICMP Types", [("Echo", C[0]), ("Unreach", C[5]), ("TimeEx", C[3]), ("Host", C[2])], ["Ping + Traceroute", "PMTUD"]),
        ("Subnetting دیداری", [(" /24", C[0]), (" /25", C[1]), (" /26", C[2]), ("Hosts", C[4])], ["۲^(32-n)-2", "مثال 192.168.1.0/26"]),
        ("Private RFC1918", [("10/8", C[0]), ("172.16/12", C[1]), ("192.168/16", C[2]), ("NAT", C[3])], ["خصوصی روت عمومی نیست", "نیاز به NAT"]),
        ("IPv6 Types", [("GUA", C[4]), ("ULA", C[2]), ("LL", C[3]), ("Mcast", C[1])], ["fe80:: link-local", "Dual stack"]),
        ("EtherChannel", [("Gi1", C[0]), ("Gi2", C[0]), ("Po1", C[2]), ("Peer", C[4])], ["LACP active", "VLAN/speed یکسان"]),
        ("Port Security", [("Port", C[2]), ("MAC limit", C[3]), ("Violate", C[5]), ("Shutdown", C[5])], ["sticky MAC", "access only"]),
        ("DHCP Snooping", [("Client", C[0]), ("Untrusted", C[5]), ("Trusted", C[4]), ("Server", C[2])], ["فقط سرور trusted", "Binding table"]),
        ("Dynamic ARP Inspection", [("ARP", C[0]), ("DAI", C[3]), ("OK", C[4]), ("Drop", C[5])], ["متکی به DHCP Snooping", "جعل ARP"]),
        ("802.1X", [("User", C[0]), ("Switch", C[2]), ("RADIUS", C[1]), ("VLAN", C[4])], ["EAPoL", "MAB مهمان"]),
        ("ACL Standard/Ext", [("Src", C[0]), ("ACL", C[3]), ("Permit", C[4]), ("Deny", C[5])], ["ترتیب بالا به پایین", "implicit deny"]),
        ("Route Redistribution", [("OSPF", C[2]), ("Redis", C[3]), ("BGP", C[1]), ("Loop?", C[5])], ["tag و filter", "از حلقه اجتناب"]),
        ("ECMP", [("Src", C[0]), ("R1", C[2]), ("PathA", C[4]), ("PathB", C[1]), ("Dst", C[3])], ["چند مسیر هم‌هزینه", "hash per-flow"]),
        ("Default Route", [("LAN", C[0]), ("Router", C[2]), ("0.0.0.0/0", C[3]), ("ISP", C[4])], ["آخرین راه خروج", "یا BGP default"]),
        ("MTU / Fragment", [("Packet", C[0]), ("MTU", C[3]), ("Frag", C[1]), ("Drop", C[5])], ["DF bit", "PMTUD"]),
        ("Syslog Flow", [("Device", C[0]), ("UDP514", C[3]), ("SIEM", C[2]), ("Alert", C[5])], ["NTP زمان", "سطح severity"]),
        ("SNMP Poll", [("NMS", C[2]), ("Get", C[0]), ("Agent", C[3]), ("Trap", C[5])], ["v3 authPriv", "ACL مدیریت"]),
        ("NetFlow/IPFIX", [("Export", C[0]), ("Collector", C[2]), ("TopTalker", C[4])], ["جریان نه payload کامل", "ظرفیت"]),
        ("Zero Trust", [("User", C[0]), ("MFA", C[1]), ("Policy", C[2]), ("App", C[4])], ["هرگز اعتماد پیش‌فرض", "least privilege"]),
        ("DMZ Publish", [("Internet", C[5]), ("FW", C[3]), ("DMZ Web", C[1]), ("LAN", C[4])], ["DMZ≠LAN", "فقط پورت لازم"]),
        ("Load Balancer L4", [("VIP", C[2]), ("RS1", C[4]), ("RS2", C[1]), ("RS3", C[0])], ["TCP/UDP balance", "session optional"]),
        ("Load Balancer L7", [("HTTP", C[0]), ("Host/Path", C[2]), ("PoolA", C[4]), ("PoolB", C[1])], ["content switch", "WAF گاهی"]),
        ("DNS Split Horizon", [("Internal", C[4]), ("DNS", C[2]), ("External", C[5])], ["پاسخ متفاوت", "View/zone"]),
        ("NTP Hierarchy", [("Stratum1", C[4]), ("Core", C[2]), ("Access", C[0]), ("Hosts", C[1])], ["بدون NTP لاگ بی‌ارزش", "authentication"]),
        ("SSH Jump Host", [("Admin", C[0]), ("Jump", C[2]), ("Target", C[4])], ["کلید نه پسورد", "logging"]),
        ("VPN Split Tunnel", [("Client", C[0]), ("VPN", C[2]), ("Corp", C[4]), ("Internet", C[3])], ["بخشی تونل", "ریسک نشت"]),
        ("VXLAN VTEP", [("VM", C[0]), ("VTEP", C[2]), ("Underlay", C[7]), ("VTEP2", C[2]), ("VM2", C[4])], ["VNI", "همان L2 روی L3"]),
        ("SD-WAN Choice", [("App", C[0]), ("SLA", C[3]), ("MPLS", C[4]), ("INET", C[1])], ["underlay اول", "overlay سیاست"]),
        ("Linux iproute2", [("ip a", C[0]), ("ip r", C[2]), ("ss", C[1]), ("nft", C[3])], ["جای ifconfig", "netns"]),
        ("PowerShell Net", [("Get-NetIP", C[0]), ("Test-Net", C[2]), ("Resolve", C[1])], ["ادمین شبکه ویندوز", "Remoting"]),
        ("Batch Script Net", [("ipconfig", C[0]), ("ping", C[2]), ("netsh", C[3])], ["اتوماسیون ساده", "log خروجی"]),
        ("FortiGate Session", [("Policy", C[2]), ("Session", C[3]), ("Allow", C[4]), ("Deny", C[5])], ["first match", "diagnose"]),
        ("MikroTik Chain", [("input", C[5]), ("forward", C[2]), ("output", C[0]), ("nat", C[3])], ["raw→mangle→filter", "FastTrack"]),
        ("Cisco CEF", [("Packet", C[0]), ("FIB", C[2]), ("Adjacency", C[1]), ("Out", C[4])], ["نه process-switch", "show cef"]),
        ("Wireless Roam", [("AP1", C[0]), ("Client", C[2]), ("AP2", C[1]), ("Same IP", C[4])], ["fast transition", "controller"]),
        ("Packet Capture", [("SPAN", C[0]), ("pcap", C[2]), ("Wireshark", C[1]), ("RCA", C[4])], ["فیلتر نمایش", "حجم"]),
        ("End-to-End Verify", [("Ping", C[0]), ("Trace", C[2]), ("App", C[4]), ("Log", C[1])], ["لایه به لایه", "فرض نکن"]),
        ("Inter-VLAN SVI", [("V10", C[0]), ("SVI", C[2]), ("V20", C[1]), ("ip routing", C[4])], ["سوئیچ L3", "gateway کلاینت"]),
        ("Cable Fault", [("NIC", C[0]), ("CRC", C[5]), ("Patch", C[3]), ("OK", C[4])], ["لایه ۱ اول", "transceiver"]),
        ("Broadcast Storm", [("Loop", C[5]), ("CPU High", C[5]), ("STP", C[4]), ("Calm", C[4])], ["BPDU Guard", "storm control"]),
        ("CoPP", [("Attack", C[5]), ("CoPP", C[3]), ("CPU Safe", C[4])], ["control plane", "نه data plane فقط"]),
        ("Ansible Push", [("Inv", C[0]), ("Play", C[2]), ("Check", C[3]), ("Apply", C[4])], ["--check اول", "vault"]),
        ("Git Config Ops", [("Edit", C[0]), ("Commit", C[2]), ("Review", C[1]), ("Deploy", C[4])], ["no secrets", "tag prod"]),
        ("Observability", [("Metrics", C[0]), ("Logs", C[1]), ("Traces", C[2]), ("Alert", C[5])], ["سه ستون", "correlation"]),
        ("IR Network Step", [("Detect", C[5]), ("Contain", C[3]), ("Eradicate", C[2]), ("Recover", C[4])], ["شواهد حفظ", "change log"]),
        ("Windows Firewall", [("Profile", C[0]), ("Rule", C[2]), ("Allow", C[4]), ("Block", C[5])], ["Domain/Private/Public", "logging"]),
        ("Linux nftables", [("Input", C[5]), ("Forward", C[2]), ("Output", C[0])], ["جای iptables تدریجی", "set"]),
        ("Spine Leaf", [("Leaf", C[0]), ("Spine", C[2]), ("Leaf", C[0])], ["ECMP", "east-west"]),
        ("Out-of-Band Mgmt", [("OOB", C[3]), ("Prod", C[2]), ("Isolated", C[4])], ["مدیریت جدا", "ACL سخت"]),
        ("Config Drift", [("Golden", C[4]), ("Live", C[3]), ("Diff", C[5]), ("Remediate", C[2])], ["اتوماسیون detect", "approve"]),
        ("PKI Issue Cert", [("CSR", C[0]), ("CA", C[2]), ("Cert", C[4]), ("TLS", C[1])], ["زنجیره اعتماد", "expiry monitor"]),
        ("Full Tunnel VPN", [("Client", C[0]), ("VPN", C[2]), ("All traffic", C[4])], ["کنترل بیشتر", "بار GW"]),
        ("Proxy ARP", [("Host", C[0]), ("Router", C[2]), ("Remote", C[4])], ["پاسخ MAC به‌جای دیگری", "محدود در طراحی مدرن"]),
        ("FHRP Track", [("WAN down", C[5]), ("Track", C[3]), ("Priority", C[1]), ("Failover", C[4])], ["object track", "تست واقعی"]),
        ("uRPF", [("Spoof", C[5]), ("uRPF", C[3]), ("Drop", C[5]), ("Legit", C[4])], ["strict/loose", "edge ISP"]),
        ("Port Security Lab", [("Max1", C[2]), ("Sticky", C[3]), ("Violation", C[5])], ["err-disable recovery", "access"]),
        ("DHCP Relay", [("Client", C[0]), ("Relay", C[2]), ("Server", C[4])], ["ip helper-address", "UDP 67/68"]),
        ("Email SMTP Path", [("MUA", C[0]), ("MTA", C[2]), ("MX", C[1]), ("Dest", C[4])], ["۲۵/۵۸۷", "SPF/DKIM"]),
        ("HTTP/TLS Path", [("Browser", C[0]), ("TCP443", C[2]), ("TLS", C[1]), ("App", C[4])], ["SNI", "cert check"]),
        ("Anycast DNS", [("User", C[0]), ("Anycast", C[2]), ("PoP", C[4])], ["همان IP چند جا", "BGP"]),
        ("CDN Edge", [("User", C[0]), ("Edge", C[2]), ("Origin", C[4])], ["HIT/MISS", "TTL"]),
        ("Voice QoS", [("Phone", C[0]), ("EF", C[4]), ("WAN", C[2]), ("PBX", C[1])], ["jitter/latency", "trust boundary"]),
        ("iSCSI Path", [("Initiator", C[0]), ("Network", C[2]), ("Target", C[4])], ["jumbo/MTU", "VLAN جدا"]),
        ("Container CNI", [("Pod", C[0]), ("CNI", C[2]), ("Node", C[1]), ("Service", C[4])], ["NetworkPolicy", "overlay"]),
        ("K8s Ingress", [("Client", C[0]), ("Ingress", C[2]), ("Svc", C[1]), ("Pod", C[4])], ["TLS", "path"]),
        ("Capacity Plan", [("Baseline", C[0]), ("Peak", C[3]), ("Upgrade", C[4])], ["95th percentile", "نه فقط میانگین"]),
        ("Lab GNS3/EVE", [("Image", C[0]), ("Topo", C[2]), ("Test", C[4]), ("Doc", C[1])], ["قبل production", "snapshot"]),
        ("Latency Budget", [("App", C[0]), ("LAN", C[4]), ("WAN", C[3]), ("Server", C[2])], ["هر hop سهم", "VoIP"]),
        ("Jitter Buffer", [("RTP", C[0]), ("Buffer", C[2]), ("Play", C[4])], ["زیاد=تأخیر", "کم=قطع"]),
        ("Passwordless SSH", [("Keygen", C[0]), ("Authkeys", C[2]), ("Login", C[4])], ["مجوز 600", "agent"]),
        ("Batch Ping Sweep", [("For", C[0]), ("ping", C[2]), ("Log", C[1])], ["شبکه خودی+مجوز", "اخلاق"]),
        ("PS Port Test", [("TNC", C[0]), ("TcpTest", C[2]), ("Report", C[4])], ["Test-NetConnection", "حلقه"]),
        ("Cisco show kit", [("show run", C[0]), ("route", C[2]), ("log", C[1])], ["بکاپ قبل change", "include"]),
        ("VRF Lite", [("VRF-A", C[0]), ("VRF-B", C[1]), ("Shared", C[2])], ["جدول جدا", "leak با دقت"]),
        ("Route-Map", [("ACL", C[0]), ("Match", C[2]), ("Set", C[3]), ("Out", C[4])], ["BGP policy", "sequence"]),
        ("Prefix-List", [("Permit", C[4]), ("Deny", C[5])], ["ge/le", "دقیق"]),
        ("BFD", [("PeerA", C[0]), ("BFD", C[3]), ("PeerB", C[4])], ["شکست سریع", "با routing"]),
        ("EVPN", [("VTEP", C[2]), ("BGP EVPN", C[1]), ("VNI", C[4])], ["MAC advertise", "fabric"]),
        ("Jump+MFA", [("User", C[0]), ("MFA", C[1]), ("Bastion", C[2]), ("Asset", C[4])], ["همه از bastion", "record"]),
        ("Brownout", [("Loss2%", C[3]), ("Slow", C[5]), ("Measure", C[2])], ["نه فقط up/down", "SLA"]),
        ("Greylist/Fail2ban", [("Scan", C[5]), ("Detect", C[3]), ("Ban", C[5]), ("Allow", C[4])], ["لاگ auth", "whitelist"]),
        ("Change Window", [("Plan", C[0]), ("Peer", C[1]), ("Apply", C[2]), ("Verify", C[4]), ("Rollback", C[5])], ["لاگ change", "verify"]),
        ("Backup Path", [("Primary", C[4]), ("Fail", C[5]), ("Backup", C[3]), ("Recover", C[2])], ["RTO/RPO", "تست restore"]),
        ("Netmiko Flow", [("Py", C[0]), ("SSH", C[2]), ("Device", C[4]), ("Config", C[1])], ["vault secret", "timeout"]),
        ("SPAN Mirror", [("PortA", C[0]), ("SPAN", C[3]), ("Analyzer", C[2])], ["oversub", "فیلتر"]),
        ("Duplex Mismatch", [("Auto", C[0]), ("Half", C[5]), ("CRC", C[5])], ["show interface", "از hardcode پرهیز"]),
        ("Router-on-Stick", [("Trunk", C[3]), ("subif10", C[0]), ("subif20", C[1])], ["dot1Q", "یک لینک"]),
        ("PBR", [("Match", C[0]), ("PBR", C[3]), ("NH", C[2]), ("Normal", C[4])], ["قبل routing عادی", "دقت"]),
        ("Captive Portal", [("Open", C[0]), ("Redirect", C[3]), ("Auth", C[2]), ("Net", C[4])], ["مهمان", "HTTPS"]),
        ("Multicast PIM", [("Src", C[0]), ("RP", C[2]), ("Rcv", C[4])], ["*,G S,G", "IGMP"]),
        ("GRE+IPsec", [("A", C[0]), ("GRE", C[3]), ("IPsec", C[2]), ("B", C[4])], ["MTU", "overlay"]),
        ("First Hop IPv6", [("RA Guard", C[2]), ("DHCP Guard", C[3]), ("Src Guard", C[1])], ["edge", "access"]),
        ("OOB Mgmt", [("OOB", C[3]), ("Prod", C[2])], ["جدا", "ACL"]),
        ("Anycast Svc", [("Client", C[0]), ("Anycast", C[2]), ("N1", C[4]), ("N2", C[1])], ["health", "withdraw"]),
        ("Loss Conceal", [("Loss", C[5]), ("PLC", C[3]), ("Audio", C[0])], ["۵٪+", "QoS"]),
    ]
    while len(items) < 100:
        t, b, n = items[len(items) % 50]
        items.append((f"{t} (نمای {len(items)+1})", b, n))
    return items[:100]


def all_infographics() -> List[Tuple[str, str]]:
    return [(title, _flow(title, boxes, notes)) for title, boxes, notes in _catalog()]


def graphics_for_category(cat: str) -> List[str]:
    all_items = all_infographics()
    key = (cat or "general").lower()
    picks = []
    for title, svg in all_items:
        if key in title.lower() or key in ("general", "tcpip", "packet"):
            picks.append(svg)
        if len(picks) >= 6:
            break
    if not picks:
        picks = [svg for _, svg in all_items[:4]]
    return picks


def markdown_block(cat: str) -> str:
    svgs = graphics_for_category(cat)
    if not svgs:
        return ""
    return (
        "\n\n---\n\n## اینفوگرافیک + مثال عملی\n\n"
        "نمودارها جریان واقعی را نشان می‌دهند؛ مثال زیر هر نمودار را در Lab تکرار کن.\n\n"
        + "\n\n".join(svgs)
        + "\n"
    )


def worked_example(cat: str, topic: str) -> str:
    return (
        f"### مثال عملی — «{topic}»\n\n"
        "1. توپولوژی را روی کاغذ بکش.\n"
        "2. یک دستور verify قبل از change.\n"
        "3. change و verify مجدد.\n"
        "4. نتیجه و rollback را ثبت کن.\n"
        f"دسته: {cat}\n"
    )
