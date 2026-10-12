# -*- coding: utf-8 -*-
"""عمق اضافه برای فصل‌های تخصصی: MikroTik, Cisco L3, FortiGate, Security, Automation."""
from __future__ import annotations
import re
from typing import Any, Dict, List, Tuple


def _topic(title: str) -> str:
    t = re.sub(r"^\[L[0-4]\]\s*", "", title or "").strip()
    t = re.sub(r"\s*[—\-]\s*(آشنایی|مقدماتی|ادمین|مهندس|خبره).*$", "", t, flags=re.I)
    return t.strip() or (title or "موضوع")


def detect_specialty(title_fa: str, title_en: str = "") -> str:
    blob = f"{title_fa or ''} {title_en or ''}".lower()
    rules: List[Tuple[str, List[str]]] = [
        ("mikrotik", ["mikrotik", "routeros", "winbox", "ros ", "queue tree", "pcq", "hotspot", "pppoe"]),
        ("fortigate", ["fortigate", "fortinet", "fortios", "policy route", "sd-wan"]),
        ("cisco_l3", ["cisco", "ios-xe", "nx-os", "eigrp", "ospfv3", "bgp", "vrf", "mpls", "dmvpn", "sd-access"]),
        ("security", ["امنیت", "security", "ids", "ips", "zero trust", "802.1x", "radius", "tacacs", "hardening", "ethical"]),
        ("wireless", ["wireless", "wifi", "wlc", "capwap", "ssid", "wpa3", "roaming", "وایرلس"]),
        ("automation", ["ansible", "terraform", "paramiko", "netmiko", "napalm", "python", "automation", "اتوماسیون"]),
        ("voip", ["issabel", "asterisk", "sip", "rtp", "pbx", "voip"]),
        ("windows_net", ["powershell", "active directory", "gpo", "hyper-v", "dns windows"]),
    ]
    for name, keys in rules:
        if any(k in blob for k in keys):
            return name
    return ""


def specialized_block(title_fa: str, title_en: str = "", level: str = "L2") -> Dict[str, str]:
    """برمی‌گرداند: extra_full, extra_commands, extra_lab, extra_notes"""
    sp = detect_specialty(title_fa, title_en)
    topic = _topic(title_fa)
    if not sp:
        return {"extra_full": "", "extra_commands": "", "extra_lab": "", "extra_notes": ""}

    builders = {
        "mikrotik": _mikrotik,
        "fortigate": _fortigate,
        "cisco_l3": _cisco_l3,
        "security": _security,
        "wireless": _wireless,
        "automation": _automation,
        "voip": _voip,
        "windows_net": _windows_net,
    }
    fn = builders.get(sp)
    if not fn:
        return {"extra_full": "", "extra_commands": "", "extra_lab": "", "extra_notes": ""}
    return fn(topic, level)


def _mikrotik(topic: str, level: str) -> Dict[str, str]:
    full = f"""
---

## عمق تخصصی MikroTik / RouterOS — «{topic}»

### مدل ذهنی RouterOS
- **همه چیز path دارد:** `/ip firewall filter`، `/interface bridge`، `/queue tree`
- **ترتیب زنجیره فایروال:** raw → mangle → filter → nat (و connection tracking)
- **FastPath / FastTrack:** سرعت در برابر قابلیت‌های خاص (queue پیچیده، markهای خاص)

### سناریوی سازمانی واقعی
دفتر مرکزی + ۲ شعبه. شعبه با PPPoE به اینترنت وصل است؛ تونل L2TP/IPsec به مرکز.
نیاز: دسترسی کاربران شعبه به فایل‌سرور مرکز (10.10.10.20) و اولویت Voice روی Queue.

### طراحی پیشنهادی
| بخش | مقدار نمونه |
|------|-------------|
| LAN شعبه | 10.20.20.0/24 |
| PPPoE client | ether1 |
| L2TP out | به 203.0.113.10 |
| مشتی جالب تونل | 10.20.20.0/24 ↔ 10.10.10.0/24 |
| Queue | PCQ برای دانلود کاربران + priority برای VoIP |

### مسیر پکت (مفهومی)
کلاینت LAN → bridge/LAN IP → firewall filter forward → mangle (mark) → routing (جدول main یا policy) → out-interface (PPPoE یا tunnel)

### اشتباهات رایج
1. FastTrack قبل از ruleهای لازم → queue/mark بی‌اثر
2. NAT masquerade روی ترافیک تونل → break شدن دسترسی به مرکز
3. Accept all در input از WAN
4. MTU/MSS clamp برای PPPoE فراموش شود

### Verify حرفه‌ای
```
/ip address print
/ip route print detail
/ip firewall filter print stats
/ip firewall connection print
/interface print stats
/tool torch interface=ether1
/log print where topics~"l2tp|ipsec|firewall"
```
"""
    cmds = f"""# MikroTik — {topic}
```
/ip firewall filter print without-paging
/ip firewall nat print
/ip route print
/interface pppoe-client print
/queue tree print
/ip ipsec active-peers print
```
→ همیشه stats را بعد از تولید ترافیک تست ببین.
"""
    lab = f"""# Lab MikroTik — {topic}
1. Baseline: `/export compact` قبل از change
2. یک rule فیلتر یا route اضافه کن
3. از کلاینت ترافیک تولید کن
4. `print stats` را چک کن
5. Rollback با import backup
"""
    notes = "MikroTik: ترتیب rule و FastTrack را قبل از بهینه‌سازی بررسی کن."
    return {"extra_full": full, "extra_commands": cmds, "extra_lab": lab, "extra_notes": notes}


def _fortigate(topic: str, level: str) -> Dict[str, str]:
    full = f"""
---

## عمق تخصصی FortiGate — «{topic}»

### مدل Policy
- **Policy = هویت ترافیک:** srcintf / dstintf / srcaddr / dstaddr / service / action
- **Profileها:** IPS، Web Filter، App Control روی policy اعمال می‌شوند نه جدا از جریان
- **Session table:** وضعیت اتصال؛ برای RCA حیاتی است

### سناریو
LAN (port2) → WAN (port1) با اینترنت؛ سرور DMZ روی port3 فقط 443 از اینترنت.

| Policy | از | به | سرویس | NAT |
|--------|----|----|--------|-----|
| 10 | LAN | WAN | ALL | enable |
| 20 | WAN | DMZ | HTTPS | disable (VIP) |
| 30 | DMZ | LAN | DENY | - |

### دیاگNOS مسیر
Ingress → RPF/IP integrity → DNAT (VIP) → Policy lookup → UTM → Routing → SNAT → Egress

### دستورات تشخیص
```
diagnose firewall session list
diagnose debug flow filter addr 10.10.10.50
diagnose debug flow trace start 100
diagnose sniffer packet any 'host 10.10.10.50' 4
get router info routing-table all
```

### تله‌ها
- Policy بالا deny ضمنی ندارد ولی ترتیب policy مهم است
- VIP بدون policy = کار نمی‌کند
- SSL inspection بدون certificate روی کلاینت = شکست HTTPS
"""
    cmds = f"""# FortiGate — {topic}
```
show firewall policy
diagnose firewall session clear
get system status
```
"""
    lab = f"""# Lab FortiGate — {topic}
1. یک policy LAN→WAN بساز
2. session list را هنگام browse ببین
3. policy را disable کن و علامت را ثبت کن
4. برگردان و Verify
"""
    return {"extra_full": full, "extra_commands": cmds, "extra_lab": lab, "extra_notes": "Session + debug flow = چشم FortiGate"}


def _cisco_l3(topic: str, level: str) -> Dict[str, str]:
    full = f"""
---

## عمق تخصصی مسیریابی Cisco — «{topic}»

### Control vs Data
- **Control:** OSPF/BGP همسایگی، LSA/UPDATE، RIB
- **Data:** CEF/FIB، adjacency، forwarding واقعی

### سناریوی چندمسیره
دو لینک به HQ: Primary 100M و Backup 20M. باید failover زیر ۵ ثانیه و بدون blackhole باشد.

| پروتکل | ابزار | نکته |
|--------|------|------|
| OSPF | cost | لینک backup cost بالاتر |
| BGP | local-pref | primary ترجیح |
| Static | floating | AD بالاتر برای backup |

### مسیر عیب‌یابی
1. `show ip interface brief` — لینک up؟
2. `show ip route` — مسیر هست؟
3. `show ip ospf neighbor` / `show ip bgp summary` — control سالم؟
4. `show ip cef <dst> detail` — data plane؟
5. ACL/NAT روی مسیر؟

### مثال OSPF + توزیع
```
router ospf 1
 passive-interface default
 no passive-interface GigabitEthernet0/0
 network 10.0.0.0 0.0.0.255 area 0
default-information originate
```
"""
    cmds = f"""# Cisco L3 — {topic}
```
show ip route
show ip protocols
show ip ospf neighbor
show ip bgp summary
show ip cef
show running-config | section router
```
"""
    lab = f"""# Lab Cisco — {topic}
1. دو روتر Area 0
2. همسایگی FULL
3. لینک را shut کن و همگرایی را زمان‌گیر
4. cost را جابه‌جا کن و مسیر را ببین
"""
    return {"extra_full": full, "extra_commands": cmds, "extra_lab": lab, "extra_notes": "همیشه Control را از Data جدا ایزوله کن"}


def _security(topic: str, level: str) -> Dict[str, str]:
    full = f"""
---

## عمق تخصصی امنیت شبکه — «{topic}»

### دفاع لایه‌ای
1. **لبه:** فایروال، IPS، VPN
2. **دسترسی:** 802.1X، NAC، Port-Security
3. **هویت:** AAA (RADIUS/TACACS+)
4. **دید:** لاگ متمرکز، NetFlow، SIEM

### سناریو
کاربر Guest نباید به VLAN مالی برسد. کاربر داخلی فقط RDP به jump host.

| کنترل | پیاده‌سازی |
|--------|-------------|
| جداسازی | VLAN + ACL/FW |
| احراز | 802.1X + RADIUS |
| مدیریت | TACACS+ command authorize |
| دید | Syslog + alert روی deny |

### چک‌لیست Hardening
- غیرفعال کردن Telnet/HTTP
- SSH v2 + key
- AAA جدید قبل از قطع local (ترتيب حیاتی)
- Control-plane policing
- NTP + لاگ با timestamp
"""
    cmds = f"""# Security — {topic}
```
show aaa servers
show authentication sessions
show logging | include DENY
show ip access-lists
```
"""
    lab = f"""# Lab Security — {topic}
1. ACL/policy محدود بساز
2. ترافیک مجاز و غیرمجاز را تست کن
3. لاگ deny را تأیید کن
4. Rollback
"""
    return {"extra_full": full, "extra_commands": cmds, "extra_lab": lab, "extra_notes": "قبل از AAA از قفل شدن بیرون از دستگاه جلوگیری کن"}


def _wireless(topic: str, level: str) -> Dict[str, str]:
    full = f"""
---

## عمق تخصصی Wireless — «{topic}»

### زنجیره سرویس
RF → Association → Auth (PSK/802.1X) → DHCP → Gateway → DNS → App

### ایزوله‌سازی عیب
| علامت | لایه مشکوک |
|--------|-------------|
| اصلاً SSID نمی‌بیند | RF / AP down |
| وصل می‌شود IP ندارد | DHCP / VLAN |
| IP دارد اینترنت نه | GW / NAT / ACL |
| بعضی اپ‌ها نه | DNS / MTU / firewall |

### طراحی کانال
- 2.4GHz شلوغ: کانال 1/6/11
- 5GHz ترجیح داده شود برای ظرفیت
- Power بیش از حد = co-channel interference
"""
    cmds = f"""# Wireless — {topic}
```
show ap summary
show client summary
show wlan summary
```
"""
    lab = f"""# Lab WiFi — {topic}
1. کلاینت را وصل کن و IP بگیر
2. gateway را پینگ کن
3. AP را جابه‌جا کن (roaming)
4. لاگ controller را ببین
"""
    return {"extra_full": full, "extra_commands": cmds, "extra_lab": lab, "extra_notes": "همیشه RF را از IP جدا ایزوله کن"}


def _automation(topic: str, level: str) -> Dict[str, str]:
    full = f"""
---

## عمق تخصصی Automation — «{topic}»

### هرم اتوماسیون
1. **CLI دستی** با Runbook
2. **اسکریپت** (Python/Netmiko) برای backup و audit
3. **Ansible** برای پیکربندی اعلامی
4. **CI** برای تست قبل از apply

### اصل ایمنی
- Dry-run / check mode
- Inventory دقیق
- Backup قبل از هر playbook
- Change در پنجره مشخص

### مثال جریان
```
# backup
netmiko ... send_command('show run')
# intent
ansible-playbook -i inv site.yml --check
# apply
ansible-playbook -i inv site.yml
```
"""
    cmds = f"""# Automation — {topic}
```
ansible --version
ansible-playbook site.yml --check
python -c "import netmiko; print('ok')"
```
"""
    lab = f"""# Lab Automation — {topic}
1. از یک دستگاه backup بگیر
2. یک تغییر کوچک با اسکریپت/انسیبل
3. diff را ببین
4. rollback
"""
    return {"extra_full": full, "extra_commands": cmds, "extra_lab": lab, "extra_notes": "هرگز بدون backup و check mode در production"}


def _voip(topic: str, level: str) -> Dict[str, str]:
    full = f"""
---

## عمق تخصصی VoIP / PBX — «{topic}»

### مسیر تماس
SIP Signaling (5060) جدا از RTP مدیا است. قطع صدا بعد از ring معمولاً RTP/NAT/Firewall است نه اکانت SIP.

### چک‌لیست
- Codec سازگار
- NAT traversal (external IP)
- QoS EF برای RTP
- پورت‌های RTP باز در بازه مشخص
"""
    cmds = f"""# VoIP — {topic}
```
sipsak -vv -s sip:user@pbx
# روی Issabel/Asterisk: asterisk -rvvv
```
"""
    lab = f"""# Lab VoIP — {topic}
1. ثبت یک extension
2. تماس داخلی
3. tcpdump rtp/sip
4. یک rule فایروال را تنگ کن و علامت را ببین
"""
    return {"extra_full": full, "extra_commands": cmds, "extra_lab": lab, "extra_notes": "SIP≠RTP — جدا عیب‌یابی کن"}


def _windows_net(topic: str, level: str) -> Dict[str, str]:
    full = f"""
---

## عمق تخصصی Windows Networking — «{topic}»

### ابزارهای پایه
```
Get-NetIPConfiguration
Test-NetConnection 8.8.8.8 -TraceRoute
Resolve-DnsName example.com
Get-NetFirewallRule | Where Enabled -eq $true
```

### AD + DNS
بیشتر خطاهای «دامنه» در حقیقت DNS است. کلاینت باید DNS دامنه را ببیند نه فقط 8.8.8.8.
"""
    cmds = f"""# PowerShell — {topic}
```
Get-NetRoute
Get-DnsClientServerAddress
Test-ComputerSecureChannel -Verbose
```
"""
    lab = f"""# Lab Windows — {topic}
1. IP/DNS را ثبت کن
2. Test-NetConnection به DC
3. DNS را اشتباه کن و علامت را ببین
4. برگردان
"""
    return {"extra_full": full, "extra_commands": cmds, "extra_lab": lab, "extra_notes": "DNS دامنه را با اینترنت قاطی نکن"}
