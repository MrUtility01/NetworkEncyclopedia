# -*- coding: utf-8 -*-
"""عمق تخصصی vendor/domain — دستورات کامل MikroTik، FortiGate، Issabel، PowerShell، Batch، Android."""
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

مسیر پکت: raw → track → mangle → filter → routing → nat → out → queue
FastTrack را مراقب باش؛ queue/mangle را دور می‌زند.
"""
    cmds = f"""# MikroTik RouterOS — {topic}

```
/interface print
/ip address print
/ip route print
```

```
/ip firewall filter print without-paging
/ip firewall nat print without-paging
/ip firewall mangle print without-paging
/ip firewall raw print without-paging
/ip firewall connection print
/ip firewall address-list print
```

```
/ip firewall filter print where action=fasttrack-connection
/ip firewall nat print where chain=srcnat
/ip firewall filter print stats
```

```
/tool torch interface=ether1
/tool sniffer quick interface=ether1 port=53
/log print follow where topics~"firewall"
/ping 8.8.8.8 count=5
/ip arp print
```

```
/ip dhcp-server print
/ip dhcp-server lease print
/ip dns print
/queue simple print
/queue tree print
/ip service print
/export file=backup-before-change
```
"""
    lab = f"""# Lab MikroTik — {topic}
1. /export قبل از تغییر
2. rule مرتبط با «{topic}» اضافه کن
3. از کلاینت ترافیک بساز
4. print stats همان rule باید بالا برود
5. Rollback با import
"""
    notes = "MikroTik: اول stats و مسیر پکت، بعد بهینه‌سازی. FastTrack دشمن خاموش queue است."
    return {"extra_full": full, "extra_commands": cmds, "extra_lab": lab, "extra_notes": notes}


def _fortigate(topic: str, level: str) -> Dict[str, str]:
    full = f"""
---
## عمق تخصصی FortiGate — «{topic}»

بدون policy منطبق، session ساخته نمی‌شود. همیشه: کدام policy؟ کدام session؟ کدام route؟
"""
    cmds = f"""# FortiGate FortiOS CLI — {topic}

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
diagnose debug flow filter saddr 10.10.10.50
diagnose debug flow show console enable
diagnose debug enable
diagnose debug flow trace start 20
# diagnose debug disable
```

```
execute log filter category 0
execute log display
diagnose sys sdwan health-check
```
"""
    lab = f"""# Lab FortiGate — {topic}
1. policy LAN→WAN بساز و browse کن
2. session list را ببین
3. policy را disable کن — باید قطع شود
4. debug flow برای یک IP
"""
    notes = "FortiGate: بدون session و policy hit حدس نزن — flow را بخوان."
    return {"extra_full": full, "extra_commands": cmds, "extra_lab": lab, "extra_notes": notes}


def _cisco_l3(topic: str, level: str) -> Dict[str, str]:
    full = f"""
---
## Cisco L3 — «{topic}»
Control Plane ≠ Data Plane. همیشه CEF را هم ببین.
"""
    cmds = f"""# Cisco — {topic}
```
show ip interface brief
show ip route
show ip ospf neighbor
show ip bgp summary
show ip cef <dest> detail
show ip protocols
```
"""
    lab = f"# Lab Cisco — {topic}\nهمسایگی FULL → پینگ → shut لینک → همگرایی"
    notes = "Control سبز ≠ Data سالم."
    return {"extra_full": full, "extra_commands": cmds, "extra_lab": lab, "extra_notes": notes}


def _security(topic: str, level: str) -> Dict[str, str]:
    full = f"""
---
## امنیت شبکه — «{topic}»
لبه + دسترسی + هویت + بخش‌بندی + دید (لاگ).
"""
    cmds = f"""# Security — {topic}
```
show aaa servers
show authentication sessions
show ip access-lists
show logging | include DENY|AUTH
```
"""
    lab = f"# Lab — {topic}\nallow و deny را هر دو تست کن"
    notes = "قبل از سخت‌گیری AAA مسیر بازگشت ادمین را باز بگذار."
    return {"extra_full": full, "extra_commands": cmds, "extra_lab": lab, "extra_notes": notes}


def _wireless(topic: str, level: str) -> Dict[str, str]:
    full = f"""
---
## Wireless — «{topic}»
RF → Associate → Auth → DHCP → GW → DNS → App
"""
    cmds = f"""# Wireless — {topic}
```
show ap summary
show client summary
show wlan summary
```
"""
    lab = f"# Lab WiFi — {topic}\nAssociate + DHCP + ping GW + roaming"
    notes = "یک لایه از زنجیره را ایزوله کن."
    return {"extra_full": full, "extra_commands": cmds, "extra_lab": lab, "extra_notes": notes}


def _automation(topic: str, level: str) -> Dict[str, str]:
    full = f"""
---
## Automation — «{topic}»
Inventory + Idempotent + Verify
"""
    cmds = f"""# Automation — {topic}
```
ansible all -m ping
terraform plan
```
"""
    lab = f"# Lab — {topic}\nیک playbook کوچک + dry-run"
    notes = "بدون Inventory و Verify، اتوماسیون خطرناک است."
    return {"extra_full": full, "extra_commands": cmds, "extra_lab": lab, "extra_notes": notes}


def _voip(topic: str, level: str) -> Dict[str, str]:
    full = f"""
---
## VoIP / Issabel / Asterisk — «{topic}»

| لایه | نقش | پورت |
|------|-----|------|
| SIP | سیگنالینگ | 5060 |
| RTP | صدا | بازه دینامیک |

زنگ بدون صدا = RTP/NAT/فایروال.
"""
    cmds = f"""# Issabel / Asterisk — {topic}

```
asterisk -rvvv
sip show peers
sip show registry
pjsip show endpoints
core show channels
rtp set debug on
```

```
systemctl status asterisk
tail -f /var/log/asterisk/full
```

```
tcpdump -ni any port 5060
tcpdump -ni any udp portrange 10000-20000
ss -ulnp | grep -E '5060|asterisk'
```

```
Test-NetConnection PBX_IP -Port 5060
```
"""
    lab = f"""# Lab Issabel — {topic}
1. دو داخلی تماس
2. sip show peers
3. tcpdump 5060
4. بستن RTP روی فایروال → قطع صدا
5. CDR را چک کن
"""
    notes = "signaling را از media جدا فکر کن."
    return {"extra_full": full, "extra_commands": cmds, "extra_lab": lab, "extra_notes": notes}


def _windows_net(topic: str, level: str) -> Dict[str, str]:
    full = f"""
---
## Windows / PowerShell / Batch — «{topic}»

DNS دامنه را با 8.8.8.8 عوض نکن روی کلاینت AD.
"""
    cmds = f"""# PowerShell — {topic}

```
Get-NetIPConfiguration
Get-NetIPAddress | Format-Table
Get-NetRoute -AddressFamily IPv4
Get-DnsClientServerAddress
```

```
Test-NetConnection 8.8.8.8 -InformationLevel Detailed
Test-NetConnection dc01 -Port 389
Resolve-DnsName www.example.com
Resolve-DnsName _ldap._tcp.dc._msdcs.contoso.local -Type SRV
```

```
Get-NetFirewallProfile | Format-Table Name, Enabled
Get-NetAdapter
Test-ComputerSecureChannel -Verbose
nltest /dsgetdc:contoso.local
```

# Batch / CMD — {topic}

```
ipconfig /all
ipconfig /flushdns
ipconfig /release & ipconfig /renew
ping -n 4 8.8.8.8
tracert 1.1.1.1
nslookup example.com
netstat -ano | findstr :443
route print
arp -a
```

```
:: batch بررسی گیتوی
@echo off
set GW=10.10.10.1
ping -n 2 %GW% >nul
if errorlevel 1 (echo GW DOWN) else (echo GW OK)
```

```
netsh interface ip show config
netsh wlan show profiles
netsh advfirewall show allprofiles
```
"""
    lab = f"""# Lab PowerShell/Batch — {topic}
1. Get-NetIPConfiguration ذخیره کن
2. DNS غلط → علامت را ببین
3. برگردان + Test-ComputerSecureChannel
4. یک .bat برای پینگ GW بنویس
"""
    notes = "Batch برای مانیتور ساده؛ PowerShell برای تشخیص عمیق."
    return {"extra_full": full, "extra_commands": cmds, "extra_lab": lab, "extra_notes": notes}


def _android_net(topic: str, level: str) -> Dict[str, str]:
    full = f"""
---
## Android شبکه — «{topic}»

Wi‑Fi / Cellular / VPN / Private DNS را جدا ایزوله کن.
"""
    cmds = f"""# Android / ADB — {topic}

```
adb devices
adb shell ip addr
adb shell ip route
adb shell dumpsys wifi | head
adb shell dumpsys connectivity | head
adb shell ping -c 4 8.8.8.8
```

```
# Settings → Network → Private DNS
# Settings → Network → VPN
# MikroTik lease: /ip dhcp-server lease print
```
"""
    lab = f"""# Lab Android — {topic}
1. IP/GW روی SSID تست
2. Private DNS عوض کن
3. VPN on/off و مسیر
"""
    notes = "captive portal و Private DNS و VPN را قبل از مقصر دانستن اینترنت چک کن."
    return {"extra_full": full, "extra_commands": cmds, "extra_lab": lab, "extra_notes": notes}
