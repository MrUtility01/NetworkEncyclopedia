# -*- coding: utf-8 -*-
"""بانک دستورات، خطاها و داستان‌های سازمانی برای محتوای عمیق."""
from __future__ import annotations

COMMON = [
    ("show version", "نسخه IOS/نرم‌افزار و uptime"),
    ("show running-config", "پیکربندی فعلی"),
    ("show ip interface brief", "وضعیت و IP اینترفیس‌ها"),
    ("show ip route", "جدول مسیریابی"),
    ("show logging | last 50", "۵۰ خط آخر لاگ"),
    ("copy running-config startup-config", "ذخیره پایدار"),
    ("configure terminal", "ورود به حالت پیکربندی"),
    ("end", "خروج به privileged"),
    ("terminal length 0", "خروجی بدون صفحه‌بندی"),
    ("show processes cpu sorted", "مصرف CPU"),
]

_BASE = [
    ("show vlan brief", "لیست VLAN و پورت‌ها"),
    ("show interfaces trunk", "وضعیت trunk و allowed"),
    ("show ip ospf neighbor", "همسایه‌های OSPF"),
    ("show ip bgp summary", "خلاصه peerهای BGP"),
    ("show ip nat translations", "ترجمه‌های NAT فعال"),
    ("show crypto isakmp sa", "Phase1 IKE"),
    ("show crypto ipsec sa", "Phase2 IPsec"),
    ("show access-lists", "ACLها و hit count"),
    ("show spanning-tree", "وضعیت STP"),
    ("show spanning-tree vlan 10", "STP برای VLAN خاص"),
    ("show etherchannel summary", "وضعیت Port-Channel"),
    ("ip -br a", "آدرس‌های لینوکس (کوتاه)"),
    ("ss -tulpn", "سوکت‌های گوش‌دهنده"),
    ("tcpdump -i any -nn -c 20", "۲۰ پکت نمونه"),
    ("ipconfig /all", "جزئیات IP ویندوز"),
    ("Get-NetTCPConnection", "اتصالات TCP ویندوز"),
    ("ansible all -m ping", "دسترسی SSH انسیبل"),
    ("ansible-playbook site.yml --check", "dry-run پلی‌بوک"),
    ("terraform plan", "پیش‌نمایش تغییرات IaC"),
    ("from netmiko import ConnectHandler", "اتصال Netmiko"),
]

BANKS = {k: list(_BASE) for k in (
    "vlan", "ospf", "bgp", "nat", "vpn", "dhcp", "firewall", "stp", "linux",
    "windows", "ha", "acl", "qos", "wireless", "ansible", "terraform",
    "python", "sql", "general", "mpls", "multicast", "vxlan", "security",
    "tcpip", "storage", "virtualization",
)}

BANKS["vlan"] = [
    ("show vlan brief", "VLAN ID و پورت‌های access"),
    ("show interfaces trunk", "encapsulation و allowed VLANs"),
    ("show interfaces switchport", "mode و access/trunk"),
    ("show running-config interface Gi0/1", "پیکربندی یک پورت"),
    ("interface Gi0/1\n switchport mode access\n switchport access vlan 10", "پورت access VLAN10"),
    ("interface Gi0/24\n switchport mode trunk\n switchport trunk allowed vlan 10,20,30", "trunk محدود"),
    ("interface Vlan10\n ip address 10.10.10.1 255.255.255.0\n no shutdown", "SVI gateway"),
    ("show mac address-table vlan 10", "MACهای یادگرفته در VLAN"),
] + BANKS["vlan"]

BANKS["stp"] = [
    ("show spanning-tree", "Root و نقش پورت‌ها"),
    ("show spanning-tree vlan 10 detail", "جزئیات یک VLAN"),
    ("spanning-tree mode rapid-pvst", "فعال‌سازی RSTP"),
    ("spanning-tree vlan 10 root primary", "این سوییچ Root شود"),
    ("interface Gi0/1\n spanning-tree portfast\n spanning-tree bpduguard enable", "PortFast + BPDU Guard"),
    ("show spanning-tree inconsistentports", "پورت‌های ناسازگار"),
] + BANKS["stp"]

BANKS["ospf"] = [
    ("show ip ospf neighbor", "وضعیت adjacency"),
    ("show ip ospf interface brief", "اینترفیس‌های OSPF"),
    ("show ip ospf database", "LSAها"),
    ("show ip route ospf", "مسیرهای آموخته از OSPF"),
    ("router ospf 1\n network 10.0.0.0 0.0.0.255 area 0", "اعلان شبکه"),
    ("interface Gi0/0\n ip ospf cost 10", "تنظیم cost"),
] + BANKS["ospf"]

BANKS["bgp"] = [
    ("show ip bgp summary", "peerها و state"),
    ("show ip bgp", "جدول BGP"),
    ("show ip bgp neighbors 1.2.3.4", "جزئیات یک peer"),
    ("router bgp 65001\n neighbor 1.2.3.4 remote-as 65002", "تعریف peer"),
    ("ip prefix-list PL-OUT permit 10.0.0.0/8 le 24", "prefix-list"),
    ("clear ip bgp * soft out", "اعمال سیاست بدون reset کامل"),
] + BANKS["bgp"]

BANKS["dhcp"] = [
    ("show ip dhcp binding", "Leaseهای فعال (سیسکو)"),
    ("show ip dhcp pool", "وضعیت pool"),
    ("ip helper-address 10.10.10.5", "DHCP Relay"),
    ("Get-DhcpServerv4Lease -ScopeId 10.10.10.0", "Lease ویندوز"),
    ("Get-DhcpServerv4Scope", "Scopeهای ویندوز"),
] + BANKS["dhcp"]

BANKS["dns"] = [
    ("nslookup example.local", "پرسش ساده"),
    ("dig @10.10.10.5 internal.corp A", "پرسش به سرور مشخص"),
    ("Get-DnsServerResourceRecord -ZoneName corp.local", "رکوردهای ویندوز"),
    ("resolvectl query example.com", "systemd-resolved"),
] + BANKS["dns"]

BANKS["vpn"] = [
    ("show crypto isakmp sa", "Phase1"),
    ("show crypto ipsec sa", "Phase2 و ترافیک"),
    ("show crypto session", "جلسات"),
    ("diagnose vpn ike gateway list", "FortiGate IKE"),
    ("diagnose vpn tunnel list", "FortiGate تونل‌ها"),
] + BANKS["vpn"]

BANKS["firewall"] = [
    ("show access-lists", "ACL و hit"),
    ("diagnose firewall policy list", "سیاست FortiGate"),
    ("get system session list", "sessionهای FortiGate"),
    ("iptables -L -n -v", "قوانین iptables"),
] + BANKS["firewall"]

BANKS["ha"] = [
    ("show standby", "HSRP"),
    ("show vrrp", "VRRP"),
    ("show failover", "ASA failover"),
    ("get system ha status", "FortiGate HA"),
] + BANKS["ha"]

BANKS["linux"] = [
    ("ip -br a", "آدرس‌ها"),
    ("ss -tulpn", "پورت‌های گوش‌دهنده"),
    ("ip route", "مسیرها"),
    ("journalctl -u NetworkManager -n 50", "لاگ شبکه"),
    ("tcpdump -i eth0 -nn host 10.10.10.5", "فیلتر پکت"),
] + BANKS["linux"]

BANKS["windows"] = [
    ("ipconfig /all", "جزئیات کامل"),
    ("Get-NetIPConfiguration", "پیکربندی شبکه"),
    ("Resolve-DnsName corp.local", "DNS"),
    ("Test-NetConnection 10.10.10.1 -Port 443", "تست پورت"),
] + BANKS["windows"]

BANKS["acl"] = [
    ("show access-lists", "همه ACLها"),
    ("access-list 100 permit tcp any host 10.10.10.5 eq 443", "اجازه HTTPS"),
    ("ip access-group 100 in", "اعمال inbound"),
] + BANKS["acl"]

BANKS["security"] = [
    ("show port-security", "وضعیت Port-Security"),
    ("show authentication sessions", "جلسات 802.1X"),
    ("show dot1x all", "وضعیت dot1x"),
] + BANKS["security"]

BANKS["ansible"] = [
    ("ansible --version", "نسخه"),
    ("ansible all -m ping", "تست دسترسی"),
    ("ansible-playbook site.yml --check --diff", "dry-run با diff"),
] + BANKS["ansible"]

BANKS["python"] = [
    ("python -m venv .venv", "محیط مجازی"),
    ("pip install netmiko nornir scrapli", "نصب کتابخانه"),
    ("from netmiko import ConnectHandler", "ورود"),
] + BANKS["python"]

ERRORS = {
    "vlan": [
        ("کلاینت‌های VLAN10 به هم پینگ نمی‌زنند", "پورت در VLAN اشتباه یا shutdown", "show vlan brief / show interfaces status"),
        ("بین دو سوییچ ترافیک VLAN نمی‌رود", "trunk نیست یا allowed VLAN کم است", "show interfaces trunk"),
        ("Native VLAN mismatch لاگ می‌شود", "native دو طرف یکی نیست", "show interfaces trunk"),
        ("SVI بالا نیست", "هیچ پورت access در آن VLAN up نیست", "show vlan brief + show ip interface brief"),
        ("کلاینت IP می‌گیرد ولی gateway ندارد", "SVI یا DHCP option اشتباه", "ipconfig /all + show run interface VlanX"),
    ],
    "stp": [
        ("broadcast storm / CPU سوییچ ۱۰۰٪", "loop لایه ۲، STP غیرفعال یا لینک جدید بدون STP", "show spanning-tree / show processes cpu"),
        ("پورت access ناگهان err-disabled", "BPDU Guard فعال و BPDU دریافت شده", "show interfaces status err-disabled"),
        ("Root Bridge مدام عوض می‌شود", "اولویت یکسان یا لینک flapping", "show spanning-tree root"),
        ("بعد از وصل لینک backup ترافیک قطع شد", "reconvergence طولانی (STP کلاسیک)", "show spanning-tree"),
    ],
    "ospf": [
        ("Neighbor stuck in 2-Way", "دو طرف DR نمی‌شوند یا p2p اشتباه", "show ip ospf neighbor / show ip ospf interface"),
        ("Neighbor down بعد از چند دقیقه", "timer mismatch یا authentication", "show ip ospf neighbor detail"),
        ("مسیر Area1 در Area0 نیست", "virtual-link یا ABR اشتباه", "show ip ospf database / show ip route ospf"),
    ],
    "bgp": [
        ("Peer Idle / Active", "reachability یا AS number اشتباه", "show ip bgp summary / ping update-source"),
        ("مسیر دریافت می‌شود ولی نصب نمی‌شود", "next-hop unreachable یا route-map", "show ip bgp / show ip route"),
        ("بعد از قطع ISP1 ترافیک سوییچ نشد", "local-pref یا weight اشتباه", "show ip bgp / show route-map"),
    ],
    "dhcp": [
        ("کلاینت APIPA می‌گیرد", "Scope پر یا Relay نیست", "show ip dhcp pool / Get-DhcpServerv4Scope"),
        ("فقط یک VLAN IP نمی‌گیرد", "helper-address روی SVI آن VLAN نیست", "show run interface VlanX"),
        ("آدرس تکراری", "reservation تداخل یا rogue DHCP", "show ip dhcp conflict / dhcp snooping"),
    ],
    "dns": [
        ("نام داخلی از بیرون resolve می‌شود", "Split-Horizon پیاده نشده", "dig از خارج + zone config"),
        ("بعضی کلاینت‌ها resolve نمی‌کنند", "DNS کلاینت اشتباه یا cache خراب", "nslookup / ipconfig /flushdns"),
    ],
    "vpn": [
        ("Phase1 up ولی Phase2 down", "PFS یا transform-set یا interesting traffic", "show crypto ipsec sa / debug"),
        ("تونل برقرار ولی ترافیک یک‌طرفه", "NAT یا ACL یا routing برگشت", "show crypto ipsec sa packets"),
    ],
    "firewall": [
        ("سرویس بعد از policy جدید قطع شد", "rule order یا object اشتباه", "diagnose firewall policy list"),
        ("sessionها بعد از failover drop شدند", "session sync غیرفعال", "get system ha status"),
    ],
    "ha": [
        ("دو Active هم‌زمان (split-brain)", "لینک heartbeat قطع", "show standby / get system ha status"),
        ("Failover شد ولی VIP جواب نمی‌دهد", "gratuitous ARP یا switch CAM", "show standby brief"),
    ],
    "linux": [
        ("پورت گوش نمی‌دهد", "سرویس down یا bind اشتباه", "ss -tulpn / systemctl status"),
        ("forward کار نمی‌کند", "ip_forward=0 یا firewall", "sysctl net.ipv4.ip_forward"),
    ],
    "windows": [
        ("Login با clock skew", "زمان بیش از ۵ دقیقه اختلاف", "w32tm /query /status"),
        ("GPO اعمال نمی‌شود", "replication یا امنیته لینک", "gpresult /r / gpupdate /force"),
    ],
    "general": [
        ("سرویس قطع کامل", "لایه فیزیکی یا gateway", "show interface / ping gateway"),
        ("فقط بعضی کلاینت‌ها", "VLAN / ACL / DNS خاص", "مقایسه کلاینت خوب و بد"),
        ("بعد از reboot برگشت", "startup ≠ running", "show startup-config"),
        ("کندی نه قطعی", "congestion / duplex / QoS", "show interface counters"),
        ("قطع متناوب", "flapping / reconvergence", "log | include UPDOWN"),
    ],
}

SCENARIO_HOOKS = {
    "vlan": [
        "سازمانی با ۴ طبقه و VLAN جدا برای کاربران، سرور، VoIP و مهمان. بعد از جابجایی یک سوییچ طبقه ۳، کاربران VLAN10 به فایل‌سرور VLAN20 دسترسی ندارند؛ ARP ناقص و gateway گاهی timeout می‌دهد.",
    ],
    "stp": [
        "بعد از وصل شدن یک کابل backup بین دو سوییچ access، ناگهان broadcast storm و CPU سوییچ‌ها ۱۰۰٪ شد. تلفن‌های VoIP قطع و دوربین‌ها از شبکه خارج شدند.",
    ],
    "ospf": [
        "سایت فرعی (Area1) به Area0 وصل است ولی مسیرهای Area1 در هسته دیده نمی‌شوند. Neighbor در حالت 2-Way گیر کرده و تیم فکر می‌کند لینک خراب است.",
    ],
    "bgp": [
        "دو ISP دارید. ISP1 قطع شد ولی ترافیک به ISP2 سوییچ نشد. کاربران اینترنت ندارند و مانیتورینگ فقط «peer down» نشان می‌دهد.",
    ],
    "dhcp": [
        "صبح روز کاری، کلاینت‌های جدید در طبقه ۲ همه APIPA می‌گیرند. Scope آن VLAN پر شده و Relay هم روی SVI تنظیم نشده بود.",
    ],
    "dns": [
        "نام داخلی از اینترنت resolve می‌شود و ساختار AD از بیرون قابل مشاهده است. Split-Horizon پیاده نشده.",
    ],
    "vpn": [
        "تونل Site-to-Site Phase1 سبز است ولی Phase2 نمی‌آید. ترافیک بین دو سایت برقرار نیست و تیم فقط «SA up» می‌بیند.",
    ],
    "firewall": [
        "بعد از اعمال یک policy جدید برای محدود کردن RDP، سرویس HTTPS داخلی هم قطع شد چون object گروه اشتباه بود.",
    ],
    "ha": [
        "لینک heartbeat بین دو فایروال قطع شد و هر دو Active شدند (split-brain). VIP تکراری و ترافیک نصفه‌نیمه.",
    ],
    "linux": [
        "سرور لینوکس بعد از reboot دیگر به شبکه جواب نمی‌دهد. IP روی اینترفیس نیست چون netplan اعمال نشده.",
    ],
    "windows": [
        "کاربران سایت فرعی نمی‌توانند لاگین کنند؛ خطای clock skew. زمان DC فرعی بیش از ۵ دقیقه عقب است.",
    ],
    "security": [
        "پورت access بعد از تعویض NIC کاربر err-disabled شد (Port-Security). کاربر می‌گوید «فقط کارت شبکه عوض کردم».",
    ],
    "tcpip": [
        "اپلیکیشن TCP بزرگ fail می‌شود ولی ping کوچک OK است. مشکوک به MTU blackhole در مسیر VPN.",
    ],
    "storage": [
        "VMها کند شده‌اند؛ CPU و RAM عادی است ولی latency دیسک بالا رفته. مشکوک به RAID degraded یا کنترلر.",
    ],
    "general": [
        "سازمانی با چند سایت و حدود ۸۰۰ کاربر. NOC گزارش می‌دهد سرویس حیاتی کند یا قطع است. باید از L1 تا L7 ایزوله کنید و با حداقل قطعی رفع کنید.",
    ],
}
