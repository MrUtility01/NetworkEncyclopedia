# -*- coding: utf-8 -*-
"""کتاب جامع برای هر درس — هر مطلب مثل یک فصل کامل کتاب آموزشی."""
from __future__ import annotations
import re
from typing import Any, Dict, List, Tuple

def level_tag(title: str) -> str:
    m = re.match(r"\[(L[0-4])\]", title or "")
    return m.group(1) if m else "L0"

def clean_topic(title: str) -> str:
    t = re.sub(r"^\[L[0-4]\]\s*", "", title or "").strip()
    t = re.sub(r"\s*[—\-]\s*(آشنایی|مقدماتی|ادمین|مهندس|خبره).*$", "", t, flags=re.I)
    return t.strip() or (title or "موضوع")

def _cat_for(topic: str) -> str:
    t = (topic or "").lower()
    rules: List[Tuple[Tuple[str, ...], str]] = [
        (("vlan", "trunk", "svi", "access port", "private vlan"), "vlan"),
        (("ospf", "lsa", "area 0", "neighbor ospf", "dr/bdr"), "ospf"),
        (("bgp", "as number", "prefix-list", "route-map", "as-path"), "bgp"),
        (("nat", "pat", "masquerade", "source nat", "destination nat"), "nat"),
        (("dhcp", "dora", "lease", "relay agent", "snooping"), "dhcp"),
        (("dns", "resolver", "zone", "record a", "doh", "dot"), "dns"),
        (("vpn", "ipsec", "tunnel", "phase1", "phase2", "wireguard", "openvpn", "gre"), "vpn"),
        (("firewall", "acl", "policy", "filter", "ids", "ips", "waf"), "firewall"),
        (("wireless", "wifi", "ssid", "wpa", "802.11", "wlc", "capwap"), "wireless"),
        (("tcp", "udp", "arp", "icmp", "mtu", "mss", "ecn"), "tcpip"),
        (("mikrotik", "routeros", "winbox"), "mikrotik"),
        (("stp", "rstp", "mstp", "bpdu", "root bridge", "loop guard"), "stp"),
        (("qos", "queue", "dscp", "policer", "shaper", "cbwfq"), "qos"),
        (("ha", "hsrp", "vrrp", "glbp", "failover", "cluster"), "ha"),
        (("monitor", "snmp", "syslog", "netflow", "prometheus", "grafana", "zabbix", "telemetry"), "monitor"),
        (("automat", "ansible", "terraform", "python net", "api rest", "netconf", "napalm"), "automation"),
        (("cloud", "aws", "azure", "gcp", "vpc", "s3", "tgw"), "cloud"),
        (("security", "aaa", "radius", "tacacs", "802.1x", "zero trust", "pki", "hardening"), "security"),
        (("storage", "san", "nas", "iscsi", "nfs", "smb"), "storage"),
        (("virtual", "vmware", "hyper-v", "kvm", "docker", "kubernet", "overlay"), "virtualization"),
        (("linux", "systemd", "iptables", "nftables", "sshd", "iproute"), "linux"),
        (("window", "active directory", "gpo", "powershell", "dns server", "batch"), "windows"),
        (("backup", "snapshot", "restore", "dr ", "rpo", "rto"), "backup"),
        (("sdn", "sd-wan", "overlay", "underlay", "controller", "vxlan"), "sdn"),
        (("fortigate", "fortinet", "fortios"), "fortigate"),
        (("pfsense", "opnsense", "issabel", "asterisk", "sip", "voip"), "edge_apps"),
        (("mpls", "label", "l3vpn", "l2vpn", "vrf"), "mpls"),
        (("ipv6", "slaac", "ndp", "ra ", "dad"), "ipv6"),
    ]
    for keys, cat in rules:
        if any(k in t for k in keys):
            return cat
    return "general"

def _level_depth(level: str) -> str:
    return {
        "L0": "آشنایی — مفهوم، واژگان، تصویر ذهنی",
        "L1": "مقدماتی — پیکربندی ساده، Verify، Lab اول",
        "L2": "ادمین — چند دستگاه، عیب‌یابی، سناریوی دفتر",
        "L3": "مهندس — مقیاس، Failure Domain، HA، RCA سازمانی",
        "L4": "خبره — معماری، Trade-off، مصاحبه، استاندارد عملیات",
    }.get(level, "عمومی")

def _vendor_cmds(topic: str, cat: str) -> str:
    blocks = []
    blocks.append(f"""### Cisco IOS / IOS-XE — «{topic}»
```
show running-config
show ip interface brief
show interfaces
show ip route
show logging | last 50
copy running-config startup-config
ping <gateway>
ping 8.8.8.8
traceroute 1.1.1.1
```""")
    blocks.append(f"""### MikroTik RouterOS — «{topic}»
```
/system resource print
/interface print
/ip address print
/ip route print detail
/ip firewall filter print stats without-paging
/ip firewall nat print
/ip firewall connection print
/export file=backup-before-change
/ping 8.8.8.8 count=5
/tool torch interface=ether1
/ip dhcp-server lease print
```""")
    blocks.append(f"""### FortiGate FortiOS — «{topic}»
```
get system status
get system interface physical
get router info routing-table all
show firewall policy
diagnose sys session list
diagnose debug flow filter saddr x.x.x.x
diagnose debug flow trace start 20
execute ping 8.8.8.8
execute log display
```""")
    blocks.append(f"""### Linux — «{topic}»
```
ip -br a
ip route
ss -tulpn
ping -c 4 8.8.8.8
traceroute -n 1.1.1.1
tcpdump -ni any icmp -c 20
nft list ruleset
```""")
    blocks.append(f"""### Windows PowerShell / Batch — «{topic}»
```
Get-NetIPConfiguration
Get-NetRoute -AddressFamily IPv4
Get-DnsClientServerAddress
Test-NetConnection 8.8.8.8 -InformationLevel Detailed
Resolve-DnsName example.com
ipconfig /all
ipconfig /flushdns
ping -n 4 8.8.8.8
tracert 1.1.1.1
route print
netsh interface ip show config
```""")
    if cat in ("mikrotik", "firewall", "nat", "vpn"):
        blocks.append(f"""### RouterOS عمیق — «{topic}»
```
/ip firewall filter print without-paging
/ip firewall mangle print without-paging
/ip firewall raw print without-paging
/ip firewall nat print without-paging
/queue tree print
/interface wireguard print
/ip ipsec active-peers print
```""")
    if cat in ("fortigate", "firewall", "vpn", "sdn"):
        blocks.append(f"""### FortiOS عمیق — «{topic}»
```
show firewall vip
show firewall ippool
diagnose firewall iprope lookup 10.10.10.50 8.8.8.8 1 443
diagnose sys sdwan health-check
get system sdwan
```""")
    if cat == "edge_apps" or "sip" in topic.lower() or "issabel" in topic.lower():
        blocks.append(f"""### Issabel / Asterisk — «{topic}»
```
asterisk -rvvv
sip show peers
sip show registry
pjsip show endpoints
core show channels
rtp set debug on
tcpdump -ni any port 5060
tcpdump -ni any udp portrange 10000-20000
```""")
    return "\n\n".join(blocks)

def _book_body(topic: str, cat: str, level: str) -> str:
    L = level or "L0"
    parts: List[str] = []
    parts.append(f"""# کتاب جامع: {topic}

**سطح:** {L} — {_level_depth(L)} | **دسته:** `{cat}`

> این متن مثل یک **فصل کامل کتاب** است: مفهوم، دستور چندسکو، Lab، RCA، امنیت، مقیاس، مصاحبه.

---
""")
    parts.append(f"""## فصل ۱ — چرا «{topic}» حیاتی است؟

وقتی «{topic}» خراب شود معمولاً:
1. قطع کامل سرویس (VLAN / شعبه / سازمان)
2. قطع جزئی سخت‌عیب‌یابی
3. کندی و نوسان
4. حفره امنیتی در صورت policy اشتباه

### سه سؤال اجباری قبل از تغییر
| سؤال | مثال پاسخ خوب |
|------|----------------|
| دامنه اثر؟ | فقط VLAN 40 یا کل سایت |
| معیار موفقیت؟ | DHCP + پینگ GW + HTTPS |
| Rollback؟ | export قبلی / copy start run |

### داستان واقعی
تکنسین بدون Baseline روی «{topic}» تغییر می‌دهد؛ بعدازظهر نیمی از کاربرها اینترنت ندارند. بدون لاگ و آخرین change، تیم بین DNS و فایروال سرگردان می‌شود.

---
""")
    parts.append(f"""## فصل ۲ — واژه‌نامه

| واژه | معنی عملی |
|------|----------|
| Interface / Port / SSID | نقطه ورود |
| Policy / ACL / Route | قانون تصمیم |
| State / Session / Neighbor | زنده‌بودن |
| Control Plane | تصمیم |
| Data Plane | ارسال پکت |
| Baseline | قبل از تغییر |
| Verify | اثبات با شواهد |
| Rollback | برگشت امن |
| Failure Domain | شعاع خرابی |
| Observability | Metric+Log+Trace |

---
""")
    parts.append(f"""## فصل ۳ — معماری مرجع

```
Client → Access (VLAN) → Distribution/L3 → Edge FW → WAN/Internet
```

«{topic}» ممکن است روی Access، Distribution یا Edge اثر بگذارد.
قانون: Failure Domain را کوچک نگه دار.

---
""")
    parts.append(f"""## فصل ۴ — مبانی نظری

«{topic}» یک **قرارداد** است: مجاز / ممنوع / پیش‌فرض / شواهد رعایت.

لایه‌ها: فیزیک → اترنت/VLAN → IP/Route → Transport → Policy/App
عیب‌یابی را از لایه درست شروع کن.

| موضوع | Lab | Production |
|-------|-----|------------|
| تغییر | آزاد | پنجره + اطلاع |
| Debug | مجاز | محدود |
| Rollback | سریع | مستند |
| لاگ | اختیاری | اجباری |

---
""")
    parts.append(f"""## فصل ۵ — پیکربندی گام‌به‌گام

**A آماده‌سازی:** توپولوژی، IP plan، Backup، معیار موفقیت
**B Config حداقلی:** یک موضوع، یک Verify
**C Verify دولایه:** دستگاه + کلاینت
**D پایدارسازی:** ذخیره، مانیتور ۱۰ دقیقه، مستند ۳ خط

| چک | انتظار |
|----|--------|
| سرویس/پروتکل | up / established |
| جدول تصمیم | ورودی دیده شود |
| کلاینت | پایدار |
| لاگ | بدون deny غیرمنتظره |

---
""")
    parts.append(f"""## فصل ۶ — مرجع دستورات چندسکو

{_vendor_cmds(topic, cat)}

---
""")
    parts.append(f"""## فصل ۷ — سه سناریوی واقعی

**دفتر کوچک:** یک Edge + Access + SSID — پیاده‌سازی ساده و Backup
**شرکت چندطبقه:** VLANهای User/Server/Voice/Guest + Policy
**چندسایت:** VPN/SD-WAN — Failover، MTU/MSS، مسیر برگشت

برای هر سناریو: علامت موفقیت و شکست را بنویس.

---
""")
    parts.append(f"""## فصل ۸ — آزمایشگاه‌ها

**Lab A:** پیاده‌سازی + Verify دستگاه/کلاینت
**Lab B:** خراب‌کاری عمدی + RCA + Rollback
**Lab C:** بار بیشتر + CPU/Session
**Lab D:** مستند یک‌صفحه‌ای (هدف، توپولوژی، مراحل، Verify)

---
""")
    parts.append(f"""## فصل ۹ — دانشنامه عیب‌یابی

| علامت | احتمال | اقدام اول |
|-------|--------|----------|
| هیچکس سرویس ندارد | لینک/power/change | از لبه کاربر بالا برو |
| بعضی گروهها | Trunk/ACL/DHCP | مقایسه سالم/ناسالم |
| IP دارد اینترنت نه | GW/NAT/DNS/Policy | پینگ GW→1.1.1.1→نام |
| قطعی متناوب | STP/duplex/WiFi/HA | log + errors |
| بعد از change خراب | آخرین تغییر | diff + Rollback |

### RCA پنج‌مرحله‌ای
1. علامت دقیق 2. آخرین تغییر 3. لایه به لایه 4. یک فرضیه/یک تست 5. مانیتور بعد از رفع

---
""")
    parts.append(f"""## فصل ۱۰ — امنیت و سخت‌سازی

Least Privilege | مدیریت فقط از شبکه مدیریت | لاگ حساس | حذف سرویس بلااستفاده | جدا کردن Guest

- [ ] دسترسی مدیریت محدود
- [ ] policy مبهم حذف شده
- [ ] لاگ قابل‌پیگیری
- [ ] Backup خارج از دستگاه

---
""")
    parts.append(f"""## فصل ۱۱ — مقیاس و Failure Domain

- اگر این جزء بمیرد چند کاربر/سایت می‌خوابند؟
- Failover خودکار یا دستی؟
- تغییر سایت A روی B اثر دارد؟

Active/Standby | Active/Active | Segmentation | Observability

---
""")
    parts.append(f"""## فصل ۱۲ — Trade-off و مصاحبه

| انتخاب | سود | هزینه |
|--------|-----|-------|
| سادگی | خطای کمتر | انعطاف کمتر |
| Policy ریز | کنترل | هزینه عملیات |
| تک‌وندور | یکپارچگی | lock-in |
| اتوماسیون | تکرارپذیری | مهارت اولیه |

سؤالات: طراحی دو DC | SLO/Metric | RCA واقعی | Shared Fate | مستند شیفت

---
""")
    parts.append(f"""## فصل ۱۳ — ۱۵ ضدالگو

1. نبود Baseline 2. Verify فقط دستگاه 3. NAT روی تونل 4. DNS عمومی روی AD
5. FastTrack دورزننده policy 6. ترتیب ACL اشتباه 7. MTU/MSS روی VPN
8. لاگ خاموش 9. مستند نکردن استثنا 10. debug در ساعت اوج
11. لینک واحد بدون مانیتور 12. مدیریت از اینترنت باز 13. تغییر همزمان Routing+FW
14. فرض «دیروز کار می‌کرد» 15. نبود Rollback تست‌شده

---
""")
    parts.append(f"""## فصل ۱۴ — آزمونک

1. اولین قدم؟ Baseline + معیار + Rollback
2. Verify خوب؟ دستگاه + کلاینت + لاگ
3. Failure Domain؟ شعاع خرابی
4. بعد از change خراب؟ آخرین change محور RCA
5. چرا یک پینگ کافی نیست؟ نوسان و مسیرهای خاص را نمی‌بیند

---
""")
    parts.append(f"""## فصل ۱۵ — چک‌لیست نهایی «{topic}»

**قبل:** توپولوژی | IP plan | Backup | معیار موفقیت | تست
**بعد:** Verify دستگاه | Verify کلاینت | لاگ | مانیتور | مستند ۳ خط

وقتی بلدی که: توضیح به تازه‌کار | Lab خراب/درست | Production با Rollback | دفاع Trade-off در مصاحبه.

**سطح این فصل:** {_level_depth(L)}
""")
    return "\n".join(parts)

def _commands_book(topic: str, cat: str, level: str) -> str:
    return f"# مرجع دستورات کتاب «{topic}»\n\n{_vendor_cmds(topic, cat)}\n"

def _lab_book(topic: str, cat: str, level: str) -> str:
    return f"""# آزمایشگاه‌های کتاب «{topic}»

## Lab ۱ پایه
توپولوژی حداقل → Config → Verify دستگاه/کلاینت → ذخیره خروجی

## Lab ۲ RCA
اشتباه عمدی → ماتریس عیب‌یابی → رفع + Rollback

## Lab ۳ پایداری
بار بیشتر → CPU/Session/Error → گزارش نیم‌صفحه

## Lab ۴ چندسکو
همان سناریو روی Cisco / MikroTik / FortiGate / Linux و مقایسه Verify
"""

def _notes_book(topic: str, cat: str, level: str) -> str:
    return f"""# یادداشت و RCA — «{topic}»

1. علامت دقیق 2. آخرین تغییر 3. لایه به لایه 4. یک فرضیه/یک تست 5. مانیتور

مرور: معیار موفقیت؟ دستور Verify اصلی؟ خطرناک‌ترین ضدالگو؟ کوچک کردن Failure Domain؟
"""

def build_deep_fallback(title_fa: str, title_en: str = "", level: str | None = None) -> Dict[str, Any]:
    level = level or level_tag(title_fa)
    topic = clean_topic(title_fa)
    cat = _cat_for(topic)
    spec = {"extra_full": "", "extra_commands": "", "extra_lab": "", "extra_notes": ""}
    try:
        from core.specialized_depth import specialized_block, detect_specialty
        if detect_specialty(title_fa, title_en):
            spec = specialized_block(title_fa, title_en, level) or spec
    except Exception:
        pass
    body = _book_body(topic, cat, level)
    if spec.get("extra_full"):
        body += "\n\n---\n## پیوست تخصصی Vendor/Domain\n" + spec["extra_full"]
    summary = (
        f"کتاب جامع «{topic}» | {level} — {_level_depth(level)}. "
        f"مفهوم، دستورات چندسکو، Lab، RCA، امنیت، مقیاس، مصاحبه."
    )
    commands = _commands_book(topic, cat, level)
    if spec.get("extra_commands"):
        commands += "\n\n" + spec["extra_commands"]
    examples = _lab_book(topic, cat, level)
    if spec.get("extra_lab"):
        examples += "\n\n" + spec["extra_lab"]
    notes = _notes_book(topic, cat, level)
    if spec.get("extra_notes"):
        notes += "\n\n" + spec["extra_notes"]
    return {
        "summary": summary,
        "full_content": body,
        "commands": commands,
        "examples": examples,
        "notes": notes,
        "level": level,
        "topic": topic,
        "category": cat,
    }
