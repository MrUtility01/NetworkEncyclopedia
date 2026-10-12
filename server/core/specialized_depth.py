# -*- coding: utf-8 -*-
"""عمق تخصصی vendor/domain — متن بلند، سناریو، دستور، RCA، تله‌ها."""
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
        ("wireless", ["wireless", "wifi", "wlc", "capwap", "ssid", "wpa3", "roaming", "وایرلس", "802.11"]),
        ("automation", ["ansible", "terraform", "paramiko", "netmiko", "napalm", "python", "automation", "اتوماسیون", "scrapli"]),
        ("voip", ["issabel", "asterisk", "sip", "rtp", "pbx", "voip"]),
        ("windows_net", ["powershell", "active directory", "gpo", "hyper-v", "dns windows", "kerberos"]),
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
    }
    fn = builders.get(sp)
    return fn(topic, level) if fn else {"extra_full": "", "extra_commands": "", "extra_lab": "", "extra_notes": ""}


def _mikrotik(topic: str, level: str) -> Dict[str, str]:
    full = f"""
---

## عمق تخصصی MikroTik / RouterOS — «{topic}»

### ۱) مدل ذهنی واقعی RouterOS
RouterOS مثل یک سیستم‌عامل شبکه است نه فقط یک فایروال ساده:

| لایه | path نمونه | نقش |
|------|------------|-----|
| لایه ۲ | `/interface bridge` `/interface ethernet` | پورت، بریج، VLAN filtering |
| آدرس/مسیر | `/ip address` `/ip route` | L3 و جدول مسیر |
| فایروال | `/ip firewall raw/mangle/filter/nat` | علامت‌گذاری، فیلتر، NAT |
| صف | `/queue simple` `/queue tree` | محدودیت و اولویت |
| تونل/VPN | `/interface l2tp-client` `/ip ipsec` | ارتباط شعب |
| ابزار | `/tool torch` `/tool sniffer` `/log` | تشخیص زنده |

**اصل طلایی:** ترافیک قبل از اینکه «اینترنت برود» از زنجیره‌ای عبور می‌کند. اگر FastTrack زود accept کند، بسیاری از ruleهای بعدی هرگز دیده نمی‌شوند.

### ۲) مسیر پکت در RouterOS (Forward)
1. ورود به اینترفیس (ether/bridge/vlan)
2. **raw** (اختیاری — قبل از connection tracking)
3. Connection tracking
4. **mangle** (mark connection / mark packet / mark routing)
5. **filter** (accept/drop/reject)
6. Routing decision (main یا routing-mark)
7. **nat** (srcnat/dstnat در نقاط مناسب)
8. خروج از اینترفیس خروجی
9. در صورت فعال بودن: **queue** روی out یا global

### ۳) سناریوی سازمانی کامل
**محیط:**
- دفتر مرکزی: 10.10.0.0/16 — فایل‌سرور 10.10.10.20
- شعبه: 10.20.20.0/24 روی MikroTik
- اینترنت شعبه: PPPoE روی ether1
- تونل: L2TP/IPsec به IP عمومی مرکز 203.0.113.10
- نیاز: کاربران شعبه به فایل‌سرور؛ Voice (UDP 5060/RTP) اولویت بالاتر از دانلود

**طراحی منطقی:**
1. LAN روی bridge یا ether2 با IP 10.20.20.1/24
2. PPPoE client → مسیر default
3. تونل به مرکز + route 10.10.0.0/16 از تونل
4. NAT masquerade **فقط** برای ترافیک به اینترنت نه به تونل
5. mangle برای mark بسته‌های VoIP → queue tree با priority بهتر
6. filter: input از WAN محدود؛ forward LAN→WAN و LAN→tunnel مشخص

### ۴) پیکربندی مفهومی (الگو — نه کپی کور)
```
# آدرس LAN
/ip address add address=10.20.20.1/24 interface=bridge-lan

# NAT فقط اینترنت (نه تونل)
/ip firewall nat add chain=srcnat out-interface=pppoe-out1 action=masquerade

# مسیر شبکه مرکز از تونل
/ip route add dst-address=10.10.0.0/16 gateway=l2tp-out1

# جلوگیری از FastTrack برای ترافیک markشده یا تونل (بسته به طراحی)
# /ip firewall filter ... action=fasttrack-connection فقط برای ترافیک ساده LAN→WAN
```

### ۵) تله‌های خیلی رایج
| تله | علامت | رفع |
|-----|--------|-----|
| FastTrack قبل از queue/mangle | queue بی‌اثر است | استثنا در fasttrack یا mark قبل از آن |
| masquerade روی تونل | دسترسی به سرور مرکز یک‌طرفه/خراب | srcnat را محدود به out-interface اینترنت کن |
| MSS/MTU PPPoE | سایت‌های HTTPS نیمه‌باز | `change-mss` در mangle |
| accept all input WAN | اسکن و نفوذ | فقط ICMP/IPSec/L2TP لازم |
| bridge بدون VLAN filtering | قاطی شدن VLANها | vlan-filtering=yes |

### ۶) روش تشخیص حرفه‌ای (ترتیب)
1. `/ip address print` و `/interface print` — لینک و IP
2. `/ip route print detail` — مسیر به مقصد
3. از کلاینت: ping GW سپس ping 10.10.10.20 سپس ping 8.8.8.8
4. `/ip firewall connection print` — connection ساخته می‌شود؟
5. `/ip firewall filter print stats` — کدام rule می‌خورد؟
6. `/tool torch interface=...` — ترافیک زنده روی پورت
7. `/log print where topics~"l2tp|ipsec|pppoe|firewall"`

### ۷) ارتباط با موضوع درس «{topic}»
این درس را در RouterOS به یک **path مشخص + یک Verify + یک Rollback** وصل کن. اگر نتوانستی بگویی ترافیک از کدام rule رد می‌شود، هنوز مفهوم عملی نشده است.
"""
    cmds = f"""# MikroTik عمیق — {topic}
```
/export compact file=before-change
/ip address print
/ip route print detail
/ip firewall filter print stats without-paging
/ip firewall mangle print stats
/ip firewall nat print
/ip firewall connection print
/interface print stats
/tool torch interface=ether1
/log print where topics~"firewall|l2tp|ipsec|pppoe"
```
"""
    lab = f"""# Lab عمیق MikroTik — {topic}
## توپولوژی
PC — ether2(LAN) MikroTik ether1 — اینترنت/آزمایش

## مراحل
1. `/export compact` قبل از هر change
2. یک rule filter یا mangle مرتبط با «{topic}» اضافه کن
3. از PC ترافیک تولید کن (ping/curl/iperf)
4. `print stats` همان rule باید شمارنده بالا برود
5. عمداً rule را جابه‌جا یا disable کن و علامت را ثبت کن
6. import/بازگشت به export

## معیار قبولی
- بتوانی بگویی پکت از کدام chain رد شد
- NAT تونل را خراب نکرده باشد (اگر تونل داری)
"""
    notes = "MikroTik: اول مسیر پکت و stats، بعد بهینه‌سازی. FastTrack دشمن خاموش queue است."
    return {"extra_full": full, "extra_commands": cmds, "extra_lab": lab, "extra_notes": notes}


def _fortigate(topic: str, level: str) -> Dict[str, str]:
    full = f"""
---

## عمق تخصصی FortiGate / FortiOS — «{topic}»

### ۱) مدل فکری درست
FortiGate «روتر + فایروال stateful + UTM» است. ترافیک بدون **policy منطبق** (از interace به interface) forward نمی‌شود — حتی اگر route داشته باشی.

| مفهوم | معنی عملی |
|--------|-----------|
| Zone / Interface | مرز سیاست |
| Policy | مجوز عبور + NAT + UTM |
| Session | اتصال فعلی در جدول |
| VIP | DNAT برای انتشار سرور |
| SNAT / IP pool | ترجمه مبدأ به بیرون |
| Central NAT (نسخه‌ها) | مدل جایگزین NAT |

### ۲) مسیر پردازش (ساده شده)
Ingress → بررسی اولیه/RPF → DNAT(VIP) → **Policy lookup** → Authentication/SSL (در صورت نیاز) → IPS/App/Web → Routing → SNAT → Egress

اگر policy نباشد، session ساخته نمی‌شود و ترافیک drop می‌شود.

### ۳) سناریوی سازمانی
- port1 = WAN
- port2 = LAN 10.10.10.0/24
- port3 = DMZ 10.50.50.0/24 — وب‌سرور 10.50.50.10
- نیاز: LAN اینترنت آزاد (با لاگ) | اینترنت فقط HTTPS به وب‌سرور | DMZ به LAN ممنوع

| Policy ID | از | به | آدرس | سرویس | NAT | UTM |
|-----------|----|----|------|--------|-----|-----|
| 10 | LAN | WAN | all | ALL | enable | IPS پایه |
| 20 | WAN | DMZ | VIP-web | HTTPS | - | IPS |
| 30 | DMZ | LAN | all | ALL | - | DENY + log |

### ۴) تشخیص با ابزار خود FortiOS
```
# آیا session هست؟
diagnose firewall session list | grep 10.10.10.50

# جریان قدم‌به‌قدم
diagnose debug reset
diagnose debug flow filter addr 10.10.10.50
diagnose debug flow show function-name enable
diagnose debug flow trace start 50
diagnose debug enable
# ترافیک را تولید کن سپس:
diagnose debug disable

# sniffer
diagnose sniffer packet any "host 10.10.10.50 and port 443" 4 20
```

### ۵) تله‌ها
| تله | علامت |
|-----|--------|
| VIP بدون policy | از بیرون timeout |
| سیاست خیلی بالا hit نمی‌شود چون policy بالاتر catch-all است | reorder |
| SSL inspection بدون اعتماد گواهی | سایت‌ها باز نمی‌شوند |
| SD-WAN rule بدون health-check | مسیر مرده انتخاب می‌شود |

### ۶) پیوند با «{topic}»
هر تنظیم FortiGate را با این سه سؤال ببند: **کدام policy؟ کدام session؟ کدام route؟**
"""
    cmds = f"""# FortiGate عمیق — {topic}
```
show firewall policy
get router info routing-table all
diagnose firewall session list
diagnose debug flow filter addr x.x.x.x
diagnose debug flow trace start 100
diagnose sniffer packet any 'host x.x.x.x' 4
get system status
```
"""
    lab = f"""# Lab عمیق FortiGate — {topic}
1. policy LAN→WAN بساز و از کلاینت browse کن
2. session list را ببین
3. policy را disable کن — باید قطع شود
4. debug flow را برای یک IP روشن کن و یک درخواست بزن
5. خروجی flow را بخوان: در کدام مرحله drop/accept شد؟
"""
    notes = "FortiGate: بدون session و policy hit، حدس نزن — flow را بخوان."
    return {"extra_full": full, "extra_commands": cmds, "extra_lab": lab, "extra_notes": notes}


def _cisco_l3(topic: str, level: str) -> Dict[str, str]:
    full = f"""
---

## عمق تخصصی Cisco Routing — «{topic}»

### ۱) دو صفحه جدا: Control Plane و Data Plane
| صفحه | سؤال | ابزار |
|------|------|--------|
| Control | همسایه هست؟ مسیر تبلیغ شد؟ | `show ip ospf neighbor` `show ip bgp sum` |
| Data | پکت واقعاً از کجا بیرون می‌رود؟ | `show ip cef` `show ip adjacency` |

ممکن است BGP FULL باشد ولی CEF خراب → پکت drop می‌شود.

### ۲) سناریوی دو لینک به HQ
- R_Branch Gi0/0 به HQ لینک 100M
- R_Branch Gi0/1 به HQ لینک 20M (backup)
- LAN: 10.30.0.0/24

**هدف:** ترجیح لینک 100M؛ اگر قطع شد زیر چند ثانیه سراغ 20M.

| روش | پیاده‌سازی |
|------|-------------|
| OSPF | cost کمتر روی 100M |
| BGP | local-preference بالاتر برای primary |
| Static | floating route با AD بالاتر روی backup |

### ۳) مسیر عیب‌یابی استاندارد (به ترتیب)
1. `show ip interface brief` + `show interfaces` (errors, up/down)
2. `show ip route <dest>` — مسیر هست؟ از کدام پروتکل؟
3. همسایگی: OSPF/BGP/EIGRP
4. `show ip protocols` — network statement / passive
5. `show ip cef <dest> detail` — next-hop واقعی
6. ACL روی interface: `show ip access-lists` + `show ip interface`
7. NAT در لبه: `show ip nat translations`

### ۴) مثال OSPF حداقل
```
router ospf 1
 router-id 1.1.1.1
 passive-interface default
 no passive-interface GigabitEthernet0/0
 network 10.30.0.0 0.0.0.255 area 0
 network 10.0.0.0 0.0.0.3 area 0
```
Verify: `show ip ospf neighbor` = FULL/DR یا FULL/BDR | `show ip route ospf`

### ۵) Redistribution — منطقه خطر
وقتی OSPF و BGP یا static را متقابل redistribute می‌کنی:
- حلقه مسیر
- suboptimal path
- نیاز به route-map و tag
بدون طراحی، redistribution را در production لمس نکن.

### ۶) پیوند با «{topic}»
برای این درس یک **جدول: علامت → دستور control → دستور data** بنویس و در Lab پر کن.
"""
    cmds = f"""# Cisco L3 عمیق — {topic}
```
show ip interface brief
show ip route
show ip route <dest>
show ip ospf neighbor
show ip bgp summary
show ip bgp
show ip cef <dest> detail
show ip protocols
show running-config | section router
```
"""
    lab = f"""# Lab عمیق Cisco — {topic}
1. دو روتر Area 0 — همسایگی FULL
2. LANهای دو طرف را از هم پینگ کن
3. لینک را shut کن — زمان همگرایی را اندازه بگیر
4. `show ip cef` قبل و بعد
5. cost/preference را جابه‌جا کن و مسیر را ببین
"""
    notes = "Control سبز ≠ Data سالم. همیشه CEF/adjacency را هم ببین."
    return {"extra_full": full, "extra_commands": cmds, "extra_lab": lab, "extra_notes": notes}


def _security(topic: str, level: str) -> Dict[str, str]:
    full = f"""
---

## عمق تخصصی امنیت شبکه — «{topic}»

### ۱) دفاع لایه‌ای (نه یک جعبه جادو)
1. **لبه:** فایروال، IPS، VPN، Anti-DDoS
2. **دسترسی شبکه:** 802.1X، MAB، Port-Security، DHCP Snooping، DAI
3. **هویت:** RADIUS/TACACS+، MFA برای ادمین
4. **بخش‌بندی:** VLAN + FW بین محیط‌های حساس (مالی، OT، Guest)
5. **دید:** Syslog/NetFlow/SIEM — بدون لاگ، RCA نداری

### ۲) سناریو Zero-Trust سبک سازمانی
- Guest فقط اینترنت
- کاربر اداری به اینترنت + فایل‌سرور
- ادمین فقط از jump host به تجهیزات شبکه
- مدیریت تجهیزات فقط از VLAN مدیریت

| منبع | مقصد | کنترل |
|------|------|--------|
| Guest | Internet | allow |
| Guest | LAN | deny |
| User | FileServer | allow SMB از VLAN کاربر |
| Internet | LAN | deny |
| AdminJump | NetworkDevices | allow SSH/HTTPS |

### ۳) AAA — ترتیب نجات‌بخش
روی تجهیزات شبکه قبل از قطع local:
1. سرور RADIUS/TACACS را تست کن
2. method list را با **fallback local** بگذار
3. یک session جدید تست کن
4. بعد local را محدود کن
وگرنه از دستگاه قفل می‌شوی.

### ۴) ACL / Policy — روش فکر
- اول specific، بعد general
- هر rule یک هدف کسب‌وکار داشته باشد
- denyهای مهم را log کن
- بعد از apply: تست کاربر مجاز و غیرمجاز

### ۵) پیوند با «{topic}»
امنیت بدون **تأیید منفی** (اینکه حمله/دسترسی غیرمجاز fail می‌شود) کامل نیست. در Lab هم allow و هم deny را تست کن.
"""
    cmds = f"""# Security عمیق — {topic}
```
show aaa servers
show authentication sessions
show ip access-lists
show logging | include DENY|AUTH
show running-config | include aaa|radius|tacacs
```
"""
    lab = f"""# Lab امنیت — {topic}
1. یک دسترسی مجاز تعریف کن و Verify کن
2. یک دسترسی غیرمجاز بساز و باید fail شود
3. لاگ deny را پیدا کن
4. Rollback
"""
    notes = "همیشه مسیر بازگشت ادمین را قبل از سخت‌گیری AAA باز بگذار."
    return {"extra_full": full, "extra_commands": cmds, "extra_lab": lab, "extra_notes": notes}


def _wireless(topic: str, level: str) -> Dict[str, str]:
    full = f"""
---

## عمق تخصصی Wireless — «{topic}»

### ۱) زنجیره سرویس (به ترتیب ایزوله کن)
RF سالم؟ → Association؟ → Authentication/Association OK؟ → IP از DHCP؟ → Default Gateway پینگ؟ → DNS؟ → اپلیکیشن؟

### ۲) سناریو
SSID Corp روی VLAN 40، DHCP 10.40.40.0/24، GW 10.40.40.1، اینترنت از طریق NAT لبه.

| علامت کاربر | احتمال اول |
|-------------|------------|
| SSID را نمی‌بیند | AP/قدرت/ باند |
| وصل می‌شود ولی IP ندارد | VLAN/DHCP/helper/snooping |
| IP دارد سایت باز نمی‌شود | GW/NAT/DNS/ACL |
| قطع در حرکت | Roaming / coverage hole |

### ۳) طراحی RF خلاصه
- 2.4GHz: کانال 1/6/11 — شلوغ
- 5GHz: ظرفیت بیشتر
- توان بیش از حد AP = تداخل co-channel
- موقع‌یابی AP مهم‌تر از «قدرت حداکثر»

### ۴) پیوند با «{topic}»
هر مشکل وایرلس را در **یک لایه از زنجیره** قفل کن؛ همزمان RF و IP را عوض نکن.
"""
    cmds = f"""# Wireless عمیق — {topic}
```
show ap summary
show client summary
show client detail <mac>
show wlan summary
```
"""
    lab = f"""# Lab WiFi — {topic}
1. کلاینت Associate + DHCP
2. ping GW و 8.8.8.8 و یک دامنه
3. roaming بین دو AP
4. یک VLAN اشتباه روی SSID بگذار و علامت را ببین — بعد برگردان
"""
    notes = "وایرلس: اول زنجیره را جدا کن؛ RF را با DHCP قاطی نکن."
    return {"extra_full": full, "extra_commands": cmds, "extra_lab": lab, "extra_notes": notes}


def _automation(topic: str, level: str) -> Dict[str, str]:
    full = f"""
---

## عمق تخصصی Network Automation — «{topic}»

### ۱) هرم بلوغ
1. Runbook دستی + backup
2. اسکریپت Python (Netmiko/Scrapli) برای جمع‌آوری و backup
3. Ansible برای پیکربندی اعلامی چند دستگاه
4. CI: lint + check + diff قبل از apply
5. منبع حقیقت (Git) برای inventory و playbook

### ۲) قوانین ایمنی غیرقابل مذاکره
- **Backup قبل از change**
- **check / dry-run** وقتی ابزار دارد
- **محدود کردن host list** — هرگز all در production بدون فیلتر
- **پنجره Change** و rollback نوشته‌شده
- رمز و کلید در vault نه داخل Git

### ۳) الگوی عملی
```
# جمع‌آوری
python backup_all.py --inventory prod.ini

# آزمایش
ansible-playbook -i inv harden.yml --check --diff

# اعمال
ansible-playbook -i inv harden.yml --diff
```

### ۴) پیوند با «{topic}»
اتوماسیون خوب، همان دانش شبکه‌ات را تکرارپذیر می‌کند — جایگزین فهم OSPF/ACL نیست.
"""
    cmds = f"""# Automation — {topic}
```
ansible --version
ansible-playbook playbook.yml --check --diff
python -c "import netmiko; print(netmiko.__version__)"
```
"""
    lab = f"""# Lab Automation — {topic}
1. از یک روتر/سوییچ backup بگیر
2. یک change کوچک با اسکریپت یا ansible --check
3. diff را بخوان
4. apply و Verify
5. rollback از backup
"""
    notes = "بدون backup و check mode در production اجرا نکن."
    return {"extra_full": full, "extra_commands": cmds, "extra_lab": lab, "extra_notes": notes}


def _voip(topic: str, level: str) -> Dict[str, str]:
    full = f"""
---

## عمق تخصصی VoIP — «{topic}»

### SIP در برابر RTP
- **SIP:** سیگنالینگ (برقراری تماس) — معمولاً 5060
- **RTP:** صدای واقعی — پورت‌های دینامیک
علامت کلاسیک: زنگ می‌خورد ولی صدا نیست → SIP OK، RTP/NAT/فایروال مشکل دارد.

### چک‌لیست
| مورد | بررسی |
|------|--------|
| ثبت extension | register در PBX |
| NAT | external IP در PBX |
| فایروال | SIP + بازه RTP |
| QoS | EF برای RTP |
| Codec | دو طرف یکسان |

### پیوند با «{topic}»
همیشه بگو مشکل در signaling است یا media — بعد ابزار را انتخاب کن.
"""
    cmds = f"""# VoIP — {topic}
```
# Asterisk/Issabel
asterisk -rvvv
sip show peers
# شبکه
tcpdump -ni any port 5060
```
"""
    lab = f"""# Lab VoIP — {topic}
1. دو داخلی تماس
2. tcpdump SIP
3. یک rule فایروال RTP را ببند — صدا قطع می‌شود
4. برگردان و Verify
"""
    notes = "زنگ بدون صدا = RTP/NAT تا وقتی خلافش ثابت شود."
    return {"extra_full": full, "extra_commands": cmds, "extra_lab": lab, "extra_notes": notes}


def _windows_net(topic: str, level: str) -> Dict[str, str]:
    full = f"""
---

## عمق تخصصی Windows / AD Networking — «{topic}»

###DNS قلب دامنه است
کلاینت دامنه باید DNS سرور دامنه را داشته باشد. گذاشتن فقط 8.8.8.8 روی کلاینت دامنه = خرابی login، GPO، و «trust».

### ابزارهای سریع
```
Get-NetIPConfiguration
Test-NetConnection dc01 -Port 389
Resolve-DnsName _ldap._tcp.dc._msdcs.contoso.local -Type SRV
Test-ComputerSecureChannel -Verbose
```

### پیوند با «{topic}»
قبل از دستکاری GPO یا AD، از کلاینت تا DC مسیر DNS و پورت را Verify کن.
"""
    cmds = f"""# Windows Network — {topic}
```
Get-NetRoute
Get-DnsClientServerAddress
Test-NetConnection 8.8.8.8 -TraceRoute
Get-NetFirewallRule | Where-Object Enabled -eq $true | Select displayname
```
"""
    lab = f"""# Lab Windows — {topic}
1. IP/DNS فعلی را ثبت کن
2. DNS را عمداً غلط کن — علامت login/GPO را ببین
3. برگردان و Test-ComputerSecureChannel
"""
    notes = "بیشتر خرابی‌های AD در شبکه، DNS است."
    return {"extra_full": full, "extra_commands": cmds, "extra_lab": lab, "extra_notes": notes}
