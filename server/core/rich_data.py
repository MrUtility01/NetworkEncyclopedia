# -*- coding: utf-8 -*-
"""Banks of reusable lesson fragments for densify engine."""
from __future__ import annotations

COMMON = {
    "safety": "فقط در محیط آزمایشی مجاز کار کنید؛ از Production بدون Change Window دوری کنید.",
    "verify": "پس از هر تغییر Verify کنید: وضعیت قبل/بعد، لاگ، و تست سرویس.",
    "rca": "Symptom → Scope → Evidence → Hypothesis → Fix → Verify → Document",
}

BANKS = {
    "vlan": {
        "summary": "جداسازی منطقی لایه ۲ برای امنیت و مقیاس.",
        "lab": "ساخت VLAN و assign پورت؛ بررسی show vlan.",
        "cmds": "show vlan brief\nconfigure terminal\nvlan 10\nname USERS",
    },
    "ospf": {
        "summary": "مسیریابی لینک‌استیت با Area و adjacency.",
        "lab": "دو روتر OSPF area 0؛ بررسی neighbor.",
        "cmds": "show ip ospf neighbor\nrouter ospf 1\nnetwork 10.0.0.0 0.0.0.255 area 0",
    },
    "bgp": {
        "summary": "مسیریابی بین‌دامنه‌ای با ASN و peer.",
        "lab": "eBGP peer در Lab؛ بررسی summary.",
        "cmds": "show ip bgp summary\nrouter bgp 65001\nneighbor 192.0.2.1 remote-as 65002",
    },
    "nat": {
        "summary": "ترجمه آدرس برای دسترسی خروجی و حفظ فضای عمومی.",
        "lab": "PAT روی لبه؛ بررسی translations.",
        "cmds": "show ip nat translations\nip nat inside source list 1 interface GigabitEthernet0/0 overload",
    },
    "vpn": {
        "summary": "تونل امن برای اتصال سایت یا کلاینت.",
        "lab": "IPsec یا WireGuard آزمایشی بین دو نقطه.",
        "cmds": "show crypto session\n# WireGuard: wg show",
    },
    "dhcp": {
        "summary": "تخصیص خودکار IP و گزینه‌های شبکه.",
        "lab": "pool و exclude؛ بررسی binding.",
        "cmds": "show ip dhcp binding\nip dhcp pool LAN\nnetwork 10.0.0.0 255.255.255.0",
    },
    "firewall": {
        "summary": "فیلتر ترافیک بر اساس سیاست امنیتی.",
        "lab": "قانون allow/deny آزمایشی؛ لاگ.",
        "cmds": "show access-lists\naccess-list 100 permit tcp any any eq 443",
    },
    "stp": {
        "summary": "جلوگیری از حلقه لایه ۲ با انتخاب Root.",
        "lab": "دو سوییچ؛ بررسی root و port role.",
        "cmds": "show spanning-tree\nspanning-tree vlan 1 root primary",
    },
    "dns": {
        "summary": "نام به آدرس و برعکس؛ رکوردها و resolver.",
        "lab": "query A/AAAA؛ بررسی cache.",
        "cmds": "nslookup example.com\ndig +short example.com",
    },
    "wireless": {
        "summary": "WLAN، SSID، باند و امنیت Wi-Fi.",
        "lab": "مشاهده interface و شبکه‌های مجاز.",
        "cmds": "netsh wlan show interfaces\niw dev",
    },
    "python": {
        "summary": "اتوماسیون شبکه با اسکریپت و API.",
        "lab": "اتصال read-only با Netmiko/Paramiko در Lab.",
        "cmds": "python -c \"import netmiko; print(netmiko.__version__)\"",
    },
    "ansible": {
        "summary": "پیکربندی اعلانی و idempotent.",
        "lab": "playbook gather facts روی inventory آزمایشی.",
        "cmds": "ansible all -m ping\nansible-playbook site.yml --check",
    },
}

# aliases for topic matching
for k in list(BANKS.keys()):
    BANKS[k.upper()] = BANKS[k]
