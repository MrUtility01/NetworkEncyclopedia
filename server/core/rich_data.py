# -*- coding: utf-8 -*-
"""Banks of reusable lesson fragments for densify engine."""
from __future__ import annotations

COMMON = {
    "safety": "فقط در محیط آزمایشی مجاز کار کنید؛ از Production بدون Change Window دوری کنید.",
    "verify": "پس از هر تغییر Verify کنید: وضعیت قبل/بعد، لاگ، و تست سرویس.",
    "rca": "Symptom → Scope → Evidence → Hypothesis → Fix → Verify → Document",
}

BANKS = {
    "vlan": {"summary": "جداسازی منطقی لایه ۲.", "lab": "ساخت VLAN و assign پورت.", "cmds": "show vlan brief"},
    "ospf": {"summary": "مسیریابی لینک‌استیت.", "lab": "دو روتر OSPF area 0.", "cmds": "show ip ospf neighbor"},
    "bgp": {"summary": "مسیریابی بین‌دامنه‌ای.", "lab": "eBGP peer در Lab.", "cmds": "show ip bgp summary"},
    "nat": {"summary": "ترجمه آدرس.", "lab": "PAT روی لبه.", "cmds": "show ip nat translations"},
    "vpn": {"summary": "تونل امن.", "lab": "IPsec/WireGuard آزمایشی.", "cmds": "show crypto session"},
    "dhcp": {"summary": "تخصیص خودکار IP.", "lab": "pool و binding.", "cmds": "show ip dhcp binding"},
    "firewall": {"summary": "فیلتر ترافیک.", "lab": "قانون allow/deny.", "cmds": "show access-lists"},
    "stp": {"summary": "جلوگیری از حلقه لایه ۲.", "lab": "بررسی root و port role.", "cmds": "show spanning-tree"},
    "dns": {"summary": "نام به آدرس.", "lab": "query A/AAAA.", "cmds": "nslookup example.com"},
    "wireless": {"summary": "WLAN و امنیت Wi-Fi.", "lab": "مشاهده interface.", "cmds": "netsh wlan show interfaces"},
    "python": {"summary": "اتوماسیون شبکه.", "lab": "اتصال read-only.", "cmds": "python -c \"print('ok')\""},
    "ansible": {"summary": "پیکربندی اعلانی.", "lab": "ansible all -m ping.", "cmds": "ansible all -m ping"},
    "general": {"summary": "موضوع عمومی شبکه/IT.", "lab": "مشاهده و ثبت شواهد.", "cmds": "# read-only checks"},
}

ERRORS = {
    "vlan": ["VLAN mismatch روی trunk", "Native VLAN متفاوت دو طرف", "پورت هنوز access است"],
    "stp": ["Root اشتباه انتخاب شده", "BPDU filter ناخواسته", "Loop به‌خاطر کابل اضافی"],
    "ospf": ["Neighbor در Init/2-Way گیر کرده", "Area mismatch", "Timer hello/dead متفاوت"],
    "bgp": ["Peer Idle", "ASN اشتباه", "Update-source نادرست"],
    "dhcp": ["Pool پر شده", "Relay نادرست", "Conflict آدرس"],
    "dns": ["Forwarder در دسترس نیست", "Zone transfer شکست", "Cache مسموم/کهنه"],
    "vpn": ["Phase1 fail", "Phase2 proxy-id mismatch", "NAT-T مشکل"],
    "firewall": ["قانون اشتباه order", "Object گروه ناقص", "Log بدون hit"],
    "ha": ["اولویت HSRP اشتباه", "پیش‌فرض preempt", "لینک heartbeat قطع"],
    "linux": ["سرویس fail", "Permission", "Route پیش‌فرض گم"],
    "windows": ["GPO اعمال نشده", "DNS کلاینت اشتباه", "Firewall profile"],
    "wireless": ["SSID مخفی و discovery", "VLAN نگاشت SSID", "تداخل کانال"],
    "general": ["پیکربندی با شواهد هم‌خوان نیست", "نسخه/firmware متفاوت", "محدوده آزمون مبهم"],
    "mikrotik": ["FastTrack و Firewall conflict", "Route mark نادرست"],
    "fortigate": ["Policy hit count صفر", "SSL inspection مشکل"],
    "ad": ["Replication lag", "DNS SRV مشکل"],
    "security": ["AAA timeout", "Certificate expired"],
    "tcpip": ["MTU/fragmentation", "Asymmetric routing"],
    "storage": ["Latency بالا", "Path fail"],
    "virtualization": ["vSwitch uplink", "Resource contention"],
    "python": ["Auth fail", "Timeout device"],
    "ansible": ["Inventory host unreachable", "Module missing"],
    "kubernetes": ["CNI network", "Service endpoints خالی"],
}

SCENARIO_HOOKS = {
    "vlan": ["در یک شرکت، کاربران VLAN مهمان به سرور مالی دسترسی پیدا کردند — trunk و native را بررسی کنید."],
    "stp": ["پس از افزودن سوییچ جدید، شبکه فلج شد — احتمال loop و Root اشتباه."],
    "ospf": ["دو سایت adjacency نمی‌گیرند — area و timer و network statement را چک کنید."],
    "bgp": ["مسیر اینترنت از ISP دوم برنمی‌گردد — prefix-list و AS-path را ببینید."],
    "dhcp": ["کلاینت‌ها APIPA می‌گیرند — pool، relay و snooping."],
    "dns": ["نام داخلی resolve نمی‌شود — conditional forwarder و zone."],
    "vpn": ["تونل گاهی up می‌شود — Phase1 proposal و NAT-T."],
    "firewall": ["اپلیکیشن جدید کار نمی‌کند — policy order و object."],
    "ha": ["Failover طول کشید — hello و preempt و tracking."],
    "linux": ["سرویس بعد از reboot بالا نمی‌آید — systemd و network."],
    "windows": ["کاربر GPO جدید را نمی‌بیند — replication و gpresult."],
    "wireless": ["کاربر به SSID وصل می‌شود ولی IP ندارد — VLAN و DHCP."],
    "security": ["لاگین 802.1X fail — RADIUS و certificate."],
    "tcpip": ["انتقال فایل کند است — window و loss و MTU."],
    "storage": ["VM کند شده — datastore latency."],
    "virtualization": ["VM شبکه ندارد — portgroup و uplink."],
    "python": ["اسکریپت backup هر شب fail — auth و privilege."],
    "ansible": ["playbook روی نیمی از hostها fail — inventory و become."],
    "general": ["سرویس قطع شده؛ تیم باید با Symptom→Evidence→Fix پیش برود."],
    "mikrotik": ["کاربر می‌گوید اینترنت کند است — queue و fasttrack."],
    "fortigate": ["VPN SSL وصل نمی‌شود — portal و group."],
    "ad": ["لاگین دامنه کند است — DC و DNS."],
    "kubernetes": ["Pod CrashLoop — network policy و DNS."],
    "cloud": ["Security group ترافیک را می‌بندد."],
    "backup": ["آخرین backup موفق نیست — job log."],
    "monitoring": ["Alert طوفانی — threshold و silence."],
    "voip": ["تماس یک‌طرفه — NAT و RTP."],
    "soc": ["هشدار SIEM بدون context — correlation."],
}

for _k in list(BANKS.keys()):
    if isinstance(_k, str) and _k != _k.upper():
        BANKS[_k.upper()] = BANKS[_k]
