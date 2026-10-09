# -*- coding: utf-8 -*-
"""Banks of reusable lesson fragments for densify engine.
BANKS[cat] = list of (command, description) tuples
COMMON = list of (command, description) tuples
"""
from __future__ import annotations

COMMON = [
    ("show version", "نسخه نرم‌افزار و uptime"),
    ("show ip interface brief", "وضعیت رابط‌ها و IP"),
    ("show running-config | include hostname", "نام دستگاه"),
    ("show logging | last 50", "آخرین رخدادها"),
    ("ping 8.8.8.8", "تست دسترس‌پذیری پایه"),
    ("traceroute 8.8.8.8", "مسیر لایه ۳"),
    ("show ip route", "جدول مسیریابی"),
    ("show arp", "نگاشت IP به MAC"),
    ("show cdp neighbors", "همسایه‌های کشف‌شده"),
    ("show interfaces status", "وضعیت لینک و VLAN"),
]

BANKS = {
    "vlan": [
        ("show vlan brief", "فهرست VLAN و پورت‌ها"),
        ("show interfaces trunk", "وضعیت trunk"),
        ("show interfaces switchport", "mode پورت"),
        ("interface Gi0/1\n switchport mode access\n switchport access vlan 10", "پورت access"),
        ("interface Gi0/24\n switchport mode trunk\n switchport trunk allowed vlan 10,20", "trunk محدود"),
        ("interface Vlan10\n ip address 10.10.10.1 255.255.255.0", "SVI"),
        ("show mac address-table vlan 10", "جدول MAC"),
    ],
    "ospf": [
        ("show ip ospf neighbor", "همسایه‌ها"),
        ("show ip route ospf", "مسیرهای OSPF"),
        ("show ip ospf interface brief", "رابط‌های OSPF"),
        ("router ospf 1\n network 10.0.0.0 0.0.0.255 area 0", "فعال‌سازی area 0"),
    ],
    "bgp": [
        ("show ip bgp summary", "وضعیت peer"),
        ("show ip bgp", "جدول BGP"),
        ("router bgp 65001\n neighbor 192.0.2.1 remote-as 65002", "تعریف peer"),
    ],
    "nat": [
        ("show ip nat translations", "ترجمه‌ها"),
        ("show ip nat statistics", "آمار"),
        ("ip nat inside source list 1 interface Gi0/0 overload", "PAT"),
    ],
    "vpn": [
        ("show crypto session", "نشست"),
        ("show crypto isakmp sa", "Phase1"),
        ("show crypto ipsec sa", "Phase2"),
    ],
    "dhcp": [
        ("show ip dhcp binding", "اجاره‌ها"),
        ("show ip dhcp pool", "استخر"),
        ("ip dhcp pool LAN\n network 10.0.0.0 255.255.255.0", "تعریف pool"),
    ],
    "firewall": [
        ("show access-lists", "ACLها"),
        ("access-list 100 permit tcp any any eq 443", "نمونه قانون"),
    ],
    "stp": [
        ("show spanning-tree", "وضعیت STP"),
        ("show spanning-tree root", "Root bridge"),
        ("spanning-tree vlan 1 root primary", "اولویت Root"),
    ],
    "dns": [
        ("nslookup example.com", "resolve"),
        ("dig +short example.com", "پاسخ کوتاه"),
    ],
    "wireless": [
        ("netsh wlan show interfaces", "وضعیت وای‌فای ویندوز"),
        ("netsh wlan show networks", "شبکه‌های دیده‌شده"),
        ("iw dev", "رابط بی‌سیم لینوکس"),
        ("iw dev wlan0 link", "لینک فعلی"),
    ],
    "python": [
        ("python -c \"print('ok')\"", "تست پایتون"),
        ("from netmiko import ConnectHandler", "ورود Netmiko"),
    ],
    "ansible": [
        ("ansible all -m ping", "تست inventory"),
        ("ansible-playbook site.yml --check", "dry-run"),
    ],
    "linux": [
        ("ip a", "آدرس‌ها"),
        ("ss -tulpn", "سوکت‌ها"),
        ("journalctl -xe", "لاگ"),
    ],
    "windows": [
        ("ipconfig /all", "پیکربندی IP"),
        ("Get-NetTCPConnection", "اتصالات TCP"),
    ],
    "ha": [
        ("show standby", "HSRP"),
        ("show vrrp", "VRRP"),
    ],
    "security": [
        ("show aaa servers", "AAA"),
        ("show authentication sessions", "نشست 802.1X"),
    ],
    "tcpip": [
        ("ping 8.8.8.8", "ICMP"),
        ("traceroute 8.8.8.8", "مسیر"),
    ],
    "storage": [("# check disk latency", "مانیتورینگ دیسک")],
    "virtualization": [("# esxcli network", "شبکه ESXi")],
    "mikrotik": [
        ("/ip address print", "آدرس‌ها"),
        ("/interface print", "رابط‌ها"),
        ("/ip route print", "مسیرها"),
    ],
    "fortigate": [
        ("get system status", "وضعیت"),
        ("diagnose firewall", "فایروال"),
    ],
    "ad": [("repadmin /showrepl", "replication")],
    "kubernetes": [("kubectl get pods -A", "پادها")],
    "general": COMMON[:6],
}

ERRORS = {
    "vlan": ["VLAN mismatch روی trunk", "Native VLAN متفاوت", "پورت هنوز access است"],
    "stp": ["Root اشتباه", "BPDU filter ناخواسته", "Loop کابل"],
    "ospf": ["Neighbor گیر کرده", "Area mismatch", "Timer متفاوت"],
    "bgp": ["Peer Idle", "ASN اشتباه", "Update-source نادرست"],
    "dhcp": ["Pool پر", "Relay نادرست", "Conflict آدرس"],
    "dns": ["Forwarder قطع", "Zone fail", "Cache کهنه"],
    "vpn": ["Phase1 fail", "proxy-id mismatch", "NAT-T"],
    "firewall": ["order اشتباه", "object ناقص", "بدون hit"],
    "ha": ["اولویت اشتباه", "preempt", "heartbeat قطع"],
    "linux": ["سرویس fail", "Permission", "Route گم"],
    "windows": ["GPO اعمال نشده", "DNS اشتباه", "Firewall profile"],
    "wireless": ["SSID/VLAN", "تداخل کانال", "DHCP پس از association"],
    "general": ["پیکربندی با شواهد هم‌خوان نیست", "نسخه متفاوت", "محدوده مبهم"],
    "mikrotik": ["FastTrack conflict", "Route mark نادرست"],
    "fortigate": ["Policy hit صفر", "SSL inspection"],
    "ad": ["Replication lag", "DNS SRV"],
    "security": ["AAA timeout", "Certificate expired"],
    "tcpip": ["MTU", "Asymmetric routing"],
    "storage": ["Latency", "Path fail"],
    "virtualization": ["vSwitch uplink", "Resource contention"],
    "python": ["Auth fail", "Timeout"],
    "ansible": ["host unreachable", "Module missing"],
    "kubernetes": ["CNI", "endpoints خالی"],
}

SCENARIO_HOOKS = {
    "vlan": ["کاربران VLAN مهمان به سرور مالی دسترسی پیدا کردند — trunk و native را بررسی کنید."],
    "stp": ["پس از افزودن سوییچ، شبکه فلج شد — loop و Root."],
    "ospf": ["دو سایت adjacency نمی‌گیرند — area و timer."],
    "bgp": ["مسیر ISP دوم برنمی‌گردد — prefix-list."],
    "dhcp": ["کلاینت‌ها APIPA می‌گیرند — pool و relay."],
    "dns": ["نام داخلی resolve نمی‌شود — forwarder."],
    "vpn": ["تونل گاهی up می‌شود — Phase1."],
    "firewall": ["اپ جدید کار نمی‌کند — policy order."],
    "ha": ["Failover طول کشید — hello و tracking."],
    "linux": ["سرویس بعد از reboot بالا نمی‌آید."],
    "windows": ["GPO جدید دیده نمی‌شود."],
    "wireless": ["به SSID وصل می‌شود ولی IP ندارد."],
    "security": ["لاگین 802.1X fail."],
    "tcpip": ["انتقال فایل کند است."],
    "storage": ["VM کند — datastore latency."],
    "virtualization": ["VM شبکه ندارد."],
    "python": ["اسکریپت backup fail."],
    "ansible": ["playbook روی نیمی از hostها fail."],
    "general": ["سرویس قطع؛ Symptom→Evidence→Fix."],
    "mikrotik": ["اینترنت کند — queue و fasttrack."],
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
