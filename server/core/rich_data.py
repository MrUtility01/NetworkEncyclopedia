# -*- coding: utf-8 -*-
"""Densify banks: COMMON/BANKS = (cmd,desc); ERRORS = (symptom,cause,evidence)."""
from __future__ import annotations

COMMON = [
    ("show version", "نسخه و uptime"),
    ("show ip interface brief", "رابط‌ها و IP"),
    ("show running-config | include hostname", "hostname"),
    ("show logging | last 50", "آخرین لاگ"),
    ("ping 8.8.8.8", "تست پایه"),
    ("traceroute 8.8.8.8", "مسیر"),
    ("show ip route", "جدول مسیر"),
    ("show arp", "ARP"),
    ("show cdp neighbors", "همسایه"),
    ("show interfaces status", "وضعیت لینک"),
]

BANKS = {
    "vlan": [
        ("show vlan brief", "فهرست VLAN"),
        ("show interfaces trunk", "trunk"),
        ("show interfaces switchport", "mode پورت"),
        ("interface Gi0/1\n switchport mode access\n switchport access vlan 10", "access VLAN10"),
        ("interface Gi0/24\n switchport mode trunk\n switchport trunk allowed vlan 10,20", "trunk محدود"),
    ],
    "ospf": [
        ("show ip ospf neighbor", "neighbor"),
        ("show ip route ospf", "مسیر OSPF"),
        ("show ip ospf interface brief", "رابط OSPF"),
    ],
    "bgp": [
        ("show ip bgp summary", "peer"),
        ("show ip bgp", "جدول BGP"),
    ],
    "nat": [
        ("show ip nat translations", "ترجمه"),
        ("show ip nat statistics", "آمار"),
    ],
    "vpn": [
        ("show crypto session", "session"),
        ("show crypto isakmp sa", "Phase1"),
        ("show crypto ipsec sa", "Phase2"),
    ],
    "dhcp": [
        ("show ip dhcp binding", "lease"),
        ("show ip dhcp pool", "pool"),
    ],
    "firewall": [
        ("show access-lists", "ACL"),
    ],
    "stp": [
        ("show spanning-tree", "STP"),
        ("show spanning-tree root", "Root"),
    ],
    "dns": [
        ("nslookup example.com", "resolve"),
        ("dig +short example.com", "dig"),
    ],
    "wireless": [
        ("netsh wlan show interfaces", "Wi-Fi Win"),
        ("netsh wlan show networks", "scan"),
        ("iw dev", "Linux iface"),
        ("iw dev wlan0 link", "link"),
    ],
    "python": [("python -c \"print('ok')\"", "test"), ("from netmiko import ConnectHandler", "netmiko")],
    "ansible": [("ansible all -m ping", "ping"), ("ansible-playbook site.yml --check", "check")],
    "linux": [("ip a", "addr"), ("ss -tulpn", "sockets"), ("journalctl -xe", "log")],
    "windows": [("ipconfig /all", "ipconfig"), ("Get-NetTCPConnection", "TCP")],
    "ha": [("show standby", "HSRP"), ("show vrrp", "VRRP")],
    "security": [("show aaa servers", "AAA"), ("show authentication sessions", "802.1X")],
    "tcpip": [("ping 8.8.8.8", "ping"), ("traceroute 8.8.8.8", "trace")],
    "storage": [("# disk latency", "storage")],
    "virtualization": [("# esxcli network", "virt")],
    "mikrotik": [("/ip address print", "addr"), ("/interface print", "iface")],
    "fortigate": [("get system status", "status")],
    "ad": [("repadmin /showrepl", "repl")],
    "kubernetes": [("kubectl get pods -A", "pods")],
    "general": COMMON[:6],
}

# (Symptom, Cause, Evidence command)
ERRORS = {
    "vlan": [
        ("کلاینت‌های VLAN10 پینگ نمی‌زنند", "پورت VLAN اشتباه یا shutdown", "show vlan brief"),
        ("ترافیک بین VLANها قطع", "SVI یا routing مشکل", "show ip interface brief"),
        ("trunk up ولی VLAN نمی‌آید", "allowed VLAN ناقص", "show interfaces trunk"),
    ],
    "stp": [
        ("شبکه بعد از کابل جدید قطع شد", "loop / Root اشتباه", "show spanning-tree"),
        ("پورت مدام blocking", "BPDU از سمت کلاینت", "show spanning-tree interface"),
    ],
    "ospf": [
        ("neighbor نمی‌آید", "area/timer/network mismatch", "show ip ospf neighbor"),
        ("مسیر در جدول نیست", "advertise نشدن network", "show ip route ospf"),
    ],
    "bgp": [
        ("peer Idle", "ASN یا reachability", "show ip bgp summary"),
        ("مسیر پذیرفته نمی‌شود", "prefix-list/route-map", "show ip bgp"),
    ],
    "dhcp": [
        ("کلاینت APIPA", "pool/relay/snooping", "show ip dhcp binding"),
        ("IP تکراری", "conflict یا static overlap", "show ip dhcp conflict"),
    ],
    "dns": [
        ("نام resolve نمی‌شود", "forwarder یا zone", "nslookup"),
        ("پاسخ کند", "timeout upstream", "dig"),
    ],
    "vpn": [
        ("تونل down", "Phase1 proposal", "show crypto isakmp sa"),
        ("Phase1 up Phase2 down", "proxy-id mismatch", "show crypto ipsec sa"),
    ],
    "firewall": [
        ("اپ کار نمی‌کند", "policy order/object", "show access-lists"),
    ],
    "ha": [
        ("Failover طول کشید", "hello/preempt/tracking", "show standby"),
    ],
    "linux": [
        ("سرویس بالا نمی‌آید", "unit fail / dependency", "journalctl -xe"),
    ],
    "windows": [
        ("GPO اعمال نشده", "replication / scope", "gpresult /r"),
    ],
    "wireless": [
        ("وصل می‌شود IP ندارد", "VLAN/DHCP نگاشت SSID", "netsh wlan show interfaces"),
        ("سیگنال خوب سرعت کم", "تداخل کانال / retry", "iw dev wlan0 link"),
    ],
    "general": [
        ("سرویس قطع کامل", "لایه فیزیکی یا gateway", "show interface / ping gateway"),
        ("فقط بعضی کلاینت‌ها", "VLAN / ACL / DNS خاص", "مقایسه کلاینت خوب و بد"),
        ("بعد از reboot برگشت", "startup ≠ running", "show startup-config"),
    ],
    "mikrotik": [("اینترنت کند", "queue/fasttrack", "/queue simple print")],
    "fortigate": [("VPN SSL fail", "portal/group", "get system status")],
    "ad": [("لاگین کند", "DC/DNS", "repadmin /showrepl")],
    "security": [("802.1X fail", "RADIUS/cert", "show authentication sessions")],
    "tcpip": [("انتقال کند", "loss/MTU", "ping -l / pathmtu")],
    "storage": [("VM کند", "datastore latency", "# storage monitor")],
    "virtualization": [("VM بدون شبکه", "portgroup/uplink", "# esxcli")],
    "python": [("اسکریپت fail", "auth/timeout", "python -c print")],
    "ansible": [("host unreachable", "inventory/ssh", "ansible all -m ping")],
    "kubernetes": [("Pod CrashLoop", "CNI/DNS", "kubectl get pods -A")],
}

SCENARIO_HOOKS = {
    "vlan": ["کاربران VLAN مهمان به سرور مالی دسترسی پیدا کردند."],
    "stp": ["پس از افزودن سوییچ، شبکه فلج شد."],
    "ospf": ["دو سایت adjacency نمی‌گیرند."],
    "bgp": ["مسیر ISP دوم برنمی‌گردد."],
    "dhcp": ["کلاینت‌ها APIPA می‌گیرند."],
    "dns": ["نام داخلی resolve نمی‌شود."],
    "vpn": ["تونل گاهی up می‌شود."],
    "firewall": ["اپ جدید کار نمی‌کند."],
    "ha": ["Failover طول کشید."],
    "linux": ["سرویس بعد از reboot بالا نمی‌آید."],
    "windows": ["GPO جدید دیده نمی‌شود."],
    "wireless": ["به SSID وصل می‌شود ولی IP ندارد."],
    "security": ["لاگین 802.1X fail."],
    "tcpip": ["انتقال فایل کند است."],
    "storage": ["VM کند شده."],
    "virtualization": ["VM شبکه ندارد."],
    "python": ["اسکریپت backup fail."],
    "ansible": ["playbook روی نیمی از hostها fail."],
    "general": ["سرویس قطع؛ Symptom→Evidence→Fix."],
    "mikrotik": ["اینترنت کند است."],
    "fortigate": ["VPN SSL وصل نمی‌شود."],
    "ad": ["لاگین دامنه کند است."],
    "kubernetes": ["Pod CrashLoop."],
    "cloud": ["Security group ترافیک را می‌بندد."],
    "backup": ["آخرین backup موفق نیست."],
    "monitoring": ["Alert طوفانی."],
    "voip": ["تماس یک‌طرفه."],
    "soc": ["هشدار SIEM بدون context."],
}

for _k in list(BANKS.keys()):
    if isinstance(_k, str) and _k != _k.upper():
        BANKS[_k.upper()] = BANKS[_k]
