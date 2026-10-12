# -*- coding: utf-8 -*-
"""عمق تخصصی vendor/domain — متن بلند + دستورات کامل + Lab + RCA.
این فایل نباید کوتاه شود؛ هر vendor باید محتوای واقعی و پرحجم داشته باشد.
"""
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
        ("mikrotik", ["mikrotik", "routeros", "winbox", "ros ", "queue tree", "pcq", "hotspot", "pppoe", "mangle"]),
        ("fortigate", ["fortigate", "fortinet", "fortios", "policy route", "sd-wan", "vip "]),
        ("cisco_l3", ["cisco", "ios-xe", "nx-os", "eigrp", "ospfv3", "bgp", "vrf", "mpls", "dmvpn", "sd-access", "cef"]),
        ("security", ["امنیت", "security", "ids", "ips", "zero trust", "802.1x", "radius", "tacacs", "hardening", "ethical", "acl"]),
        ("android_net", ["android", "اندروید", "adb", "mobile device", "mdm"]),
        ("wireless", ["wireless", "wifi", "wlc", "capwap", "ssid", "wpa3", "roaming", "وایرلس", "802.11"]),
        ("automation", ["ansible", "terraform", "paramiko", "netmiko", "napalm", "python", "automation", "اتوماسیون", "scrapli"]),
        ("voip", ["issabel", "asterisk", "sip", "rtp", "pbx", "voip", "ایزابل"]),
        ("windows_net", ["powershell", "active directory", "gpo", "hyper-v", "dns windows", "kerberos", "batch", "cmd.exe", "netsh", "windows server"]),
    ]
    for name, keys in rules:
        if any(k in blob for k in keys):
            return name
    return ""


def specialized_block(title_fa: str, title_en: str = "", level: str = "L2") -> Dict[str, str]:
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
        "android_net": _android_net,
    }
    fn = builders.get(sp)
    return fn(topic, level) if fn else {"extra_full": "", "extra_commands": "", "extra_lab": "", "extra_notes": ""}


def _mikrotik(topic: str, level: str) -> Dict[str, str]:
    full = f"""
---
## عمق تخصصی MikroTik / RouterOS — «{topic}»

### مدل ذهنی
RouterOS سیستم‌عامل شبکه است. مسیر پکت:
raw → track → mangle → filter → routing → nat → out → queue

**اصل طلایی:** FastTrack زود accept = queue/mangle دیده نمی‌شوند.

### سناریوی سازمانی
شعبه 10.20.20.0/24 | مرکز 10.10.0.0/16 | PPPoE اینترنت | تونل به مرکز
masquerade فقط روی WAN نه تونل.

### تله‌ها
| تله | علامت |
|-----|--------|
| FastTrack قبل queue | queue بی‌اثر |
| masquerade روی تونل | دسترسی یک‌طرفه |
| MSS/MTU PPPoE | HTTPS نیمه‌باز |
| accept all WAN | اسکن اینترنت |
"""
    cmds = f"""# MikroTik کامل — {topic}

```
/interface print
/interface bridge print
/ip address print
/ip route print detail
```

```
/ip firewall raw print without-paging
/ip firewall mangle print without-paging
/ip firewall filter print without-paging
/ip firewall nat print without-paging
/ip firewall filter print stats
/ip firewall connection print
/ip firewall address-list print
```

```
/ip firewall filter print where action=fasttrack-connection
/ip firewall nat print where chain=srcnat
```

```
/tool torch interface=ether1
/tool sniffer quick interface=ether1 port=53
/ping 8.8.8.8 count=5
/ip arp print
/log print follow where topics~"firewall|l2tp|ipsec|pppoe"
```

```
/ip dhcp-server print
/ip dhcp-server lease print
/ip dns print
/queue simple print
/queue tree print
/ip service print
/user print
/export file=backup-before-change
```

```
/ip firewall filter add chain=input connection-state=established,related action=accept
/ip firewall filter add chain=input connection-state=invalid action=drop
/ip firewall filter add chain=input in-interface-list=WAN action=drop
/ip firewall nat add chain=srcnat out-interface-list=WAN action=masquerade
```
"""
    lab = f"""# Lab MikroTik — {topic}
1. export قبل از change
2. rule مرتبط اضافه کن
3. ترافیک از PC
4. print stats باید بالا برود
5. disable عمدی + Rollback
"""
    notes = f"## RCA MikroTik — {topic}\nIP؟ Route؟ Connection؟ Filter hit؟ FastTrack؟ Torch؟"
    return {"extra_full": full, "extra_commands": cmds, "extra_lab": lab, "extra_notes": notes}


def _fortigate(topic: str, level: str) -> Dict[str, str]:
    full = f"""
---
## عمق تخصصی FortiGate — «{topic}»

بدون policy منطبق session ساخته نمی‌شود.
سه سؤال: کدام policy؟ کدام session؟ کدام route؟

### سناریو
LAN 10.10.10.0/24 | DMZ 10.50.50.0/24 | WAN
LAN→Internet با NAT+IPS | WAN→VIP HTTPS | DMZ→LAN deny

### تله‌ها
VIP بدون policy | catch-all بالاتر | SSL inspection بدون cert | SD-WAN بدون health-check
"""
    cmds = f"""# FortiGate کامل — {topic}

```
get system status
get system interface physical
execute ping 8.8.8.8
execute traceroute 1.1.1.1
```

```
get router info routing-table all
show router static
show firewall policy
show firewall vip
show firewall ippool
```

```
diagnose sys session list
diagnose sys session filter src 10.10.10.50
diagnose firewall iprope lookup 10.10.10.50 8.8.8.8 1 443
```

```
diagnose debug reset
diagnose debug flow filter saddr 10.10.10.50
diagnose debug flow show function-name enable
diagnose debug flow show console enable
diagnose debug enable
diagnose debug flow trace start 50
# diagnose debug disable
```

```
diagnose sniffer packet any "host 10.10.10.50 and port 443" 4 20
execute log filter category 0
execute log display
diagnose sys sdwan health-check
```
"""
    lab = f"""# Lab FortiGate — {topic}
1. policy LAN→WAN + browse
2. session list
3. disable policy → قطع
4. debug flow بخوان
"""
    notes = f"## RCA FortiGate — {topic}\npolicy hit؟ session؟ route؟ VIP؟ SSL؟ asymmetric؟"
    return {"extra_full": full, "extra_commands": cmds, "extra_lab": lab, "extra_notes": notes}


def _cisco_l3(topic: str, level: str) -> Dict[str, str]:
    full = f"""
---
## Cisco L3 — «{topic}»
Control ≠ Data. BGP FULL با CEF خراب = drop.
مسیر عیب‌یابی: interface → route → neighbor → CEF → ACL → NAT
"""
    cmds = f"""# Cisco — {topic}
```
show ip interface brief
show interfaces
show ip route
show ip route <dest>
show ip ospf neighbor
show ip ospf database
show ip bgp summary
show ip bgp
show ip cef <dest> detail
show ip protocols
show running-config | section router
show ip access-lists
show ip nat translations
```
"""
    lab = f"# Lab Cisco — {topic}\nFULL → پینگ → shut → همگرایی → CEF"
    notes = "Control سبز ≠ Data سالم."
    return {"extra_full": full, "extra_commands": cmds, "extra_lab": lab, "extra_notes": notes}


def _security(topic: str, level: str) -> Dict[str, str]:
    full = f"""
---
## امنیت — «{topic}»
لبه + دسترسی (802.1X) + هویت (AAA) + بخش‌بندی + لاگ.
قبل از قطع local: RADIUS تست → fallback local → بعد سخت‌گیری.
"""
    cmds = f"""# Security — {topic}
```
show aaa servers
show authentication sessions
show ip access-lists
show logging | include DENY|AUTH|fail
show running-config | include aaa|radius|tacacs
show port-security
show ip dhcp snooping
```
"""
    lab = f"# Lab — {topic}\nallow و deny هر دو تست + لاگ deny"
    notes = "مسیر بازگشت ادمین را قبل از AAA سخت باز بگذار."
    return {"extra_full": full, "extra_commands": cmds, "extra_lab": lab, "extra_notes": notes}


def _wireless(topic: str, level: str) -> Dict[str, str]:
    full = f"""
---
## Wireless — «{topic}»
RF → Associate → Auth → DHCP → GW → DNS → App
SSID نیست | وصل بدون IP | IP بدون اینترنت | قطع در حرکت
"""
    cmds = f"""# Wireless — {topic}
```
show ap summary
show client summary
show client detail <mac>
show wlan summary
/interface wireless registration-table print
/interface wireless scan 0
```
"""
    lab = f"# Lab WiFi — {topic}\nAssociate + DHCP + ping + roaming"
    notes = "یک لایه را ایزوله کن؛ همزمان RF و IP را عوض نکن."
    return {"extra_full": full, "extra_commands": cmds, "extra_lab": lab, "extra_notes": notes}


def _automation(topic: str, level: str) -> Dict[str, str]:
    full = f"""
---
## Automation — «{topic}»
Inventory → Playbook → Idempotent → Verify → Drift
"""
    cmds = f"""# Automation — {topic}
```
ansible all -m ping
ansible-playbook site.yml --check
terraform init
terraform plan
terraform apply
```
"""
    lab = f"# Lab — {topic}\nInventory + dry-run + apply lab + Verify"
    notes = "بدون Verify بعد از apply، فقط سریع‌تر خراب می‌کنی."
    return {"extra_full": full, "extra_commands": cmds, "extra_lab": lab, "extra_notes": notes}


def _voip(topic: str, level: str) -> Dict[str, str]:
    full = f"""
---
## VoIP / Issabel / Asterisk — «{topic}»

| لایه | نقش | پورت |
|------|-----|------|
| SIP | سیگنالینگ | 5060 |
| RTP | صدا | بازه دینامیک |

زنگ بدون صدا = SIP OK، RTP/NAT/FW مشکل دارد.
Issabel: Extensions → Trunks → Routes → CDR
"""
    cmds = f"""# Issabel / Asterisk کامل — {topic}

```
asterisk -rvvv
sip show peers
sip show registry
sip show channelstats
pjsip show endpoints
pjsip show registrations
core show channels
core show calls
rtp set debug on
```

```
systemctl status asterisk
tail -f /var/log/asterisk/full
tail -f /var/log/asterisk/messages
```

```
tcpdump -ni any port 5060
tcpdump -ni any udp portrange 10000-20000
ss -ulnp | grep -E '5060|asterisk'
```

```
Test-NetConnection PBX_IP -Port 5060
ping PBX_IP
```
"""
    lab = f"""# Lab Issabel — {topic}
1. دو داخلی تماس
2. sip show peers
3. tcpdump 5060
4. بستن RTP → قطع صدا
5. CDR
"""
    notes = "signaling را از media جدا فکر کن."
    return {"extra_full": full, "extra_commands": cmds, "extra_lab": lab, "extra_notes": notes}


def _windows_net(topic: str, level: str) -> Dict[str, str]:
    full = f"""
---
## Windows / PowerShell / Batch — «{topic}»

DNS دامنه را با فقط 8.8.8.8 عوض نکن — login/GPO می‌شکند.
PowerShell = تشخیص عمیق | Batch = مانیتور ساده | netsh = رابط/فایروال/WLAN
"""
    cmds = f"""# PowerShell کامل — {topic}

```
Get-NetIPConfiguration
Get-NetIPAddress | Format-Table InterfaceAlias, IPAddress, PrefixLength
Get-NetRoute -AddressFamily IPv4 | Format-Table
Get-DnsClientServerAddress
Get-NetAdapter | Format-Table Name, Status, LinkSpeed
```

```
Test-NetConnection 8.8.8.8 -InformationLevel Detailed
Test-NetConnection dc01 -Port 389
Test-NetConnection dc01 -Port 53
Resolve-DnsName www.example.com
Resolve-DnsName _ldap._tcp.dc._msdcs.contoso.local -Type SRV
```

```
Get-NetFirewallProfile | Format-Table Name, Enabled
Test-ComputerSecureChannel -Verbose
nltest /dsgetdc:contoso.local
gpupdate /force
gpresult /r
```

# Batch / CMD کامل — {topic}

```
ipconfig /all
ipconfig /flushdns
ipconfig /release
ipconfig /renew
ping -n 4 8.8.8.8
tracert 1.1.1.1
nslookup example.com
netstat -ano | findstr :443
route print
arp -a
netsh interface ip show config
netsh wlan show profiles
netsh advfirewall show allprofiles
```

```
:: batch مانیتور گیتوی
@echo off
set GW=10.10.10.1
set LOG=C:\temp\gw-check.txt
echo ==== %date% %time% ==== >> %LOG%
ping -n 2 %GW% >nul
if errorlevel 1 (echo GW DOWN >> %LOG%) else (echo GW OK >> %LOG%)
```
"""
    lab = f"""# Lab PowerShell/Batch — {topic}
1. Get-NetIPConfiguration ذخیره
2. DNS غلط → علامت
3. برگردان + Test-ComputerSecureChannel
4. .bat برای پینگ GW + log
"""
    notes = "خرابی AD اغلب DNS است."
    return {"extra_full": full, "extra_commands": cmds, "extra_lab": lab, "extra_notes": notes}


def _android_net(topic: str, level: str) -> Dict[str, str]:
    full = f"""
---
## Android — «{topic}»

Wi‑Fi / Cellular / VPN / Private DNS را جدا ایزوله کن.
وصل بدون اینترنت ≠ همیشه مقصر ISP — captive portal و DNS را چک کن.
"""
    cmds = f"""# Android / ADB کامل — {topic}

```
adb devices
adb shell ip addr
adb shell ip route
adb shell dumpsys wifi | head -n 80
adb shell dumpsys connectivity | head -n 80
adb shell ping -c 4 8.8.8.8
adb shell nslookup example.com
```

```
# Settings → Network → Private DNS
# Settings → Network → VPN
# MikroTik: /ip dhcp-server lease print
```
"""
    lab = f"""# Lab Android — {topic}
1. IP/GW روی SSID
2. Private DNS عوض کن
3. VPN on/off
"""
    notes = "captive portal + Private DNS + VPN قبل از مقصر دانستن اینترنت."
    return {"extra_full": full, "extra_commands": cmds, "extra_lab": lab, "extra_notes": notes}
