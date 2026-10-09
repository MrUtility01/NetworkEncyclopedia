# -*- coding: utf-8 -*-
"""فصل ۱۳ — سوییچینگ سیسکو: VLAN · STP · EtherChannel · L2 Security · 802.1X
محتوای غنی، ملموس و سازمانی با داستان واقعی، Lab گام‌به‌گام و RCA.
"""
from __future__ import annotations
import re
from typing import Any, Dict

def _level(title: str) -> str:
    m = re.match(r"\[(L[0-4])\]", title or "")
    return m.group(1) if m else "L0"

def _topic(title: str) -> str:
    t = re.sub(r"^\[L[0-4]\]\s*", "", title or "")
    t = re.sub(r"\s*[—\-]\s*(آشنایی|مقدماتی|ادمین|مهندس|خبره|Intro|Junior|Admin|Senior|Architect).*$", "", t, flags=re.I)
    return t.strip()

def _bucket(topic: str) -> str:
    t = (topic or "").lower()
    if any(k in t for k in ("802.1x", "eap", "radius", "mab", "dot1x")):
        return "dot1x"
    if any(k in t for k in ("port security", "dhcp snooping", "dai", "storm control", "bpdu guard", "root guard", "امنیت")):
        return "l2sec"
    if any(k in t for k in ("etherchannel", "lacp", "pagp", "port-channel", "lag")):
        return "etherchannel"
    if any(k in t for k in ("stp", "rstp", "mst", "loop", "root bridge", "bpdu", "spanning", "مشکل loop")):
        return "stp"
    if any(k in t for k in ("vlan", "trunk", "access", "802.1q", "native", "svi", "مفهوم vlan")):
        return "vlan"
    return "vlan"

def _depth(level: str) -> str:
    return {"L0": "تصویر ذهنی", "L1": "فریم‌به‌فریم+Lab", "L2": "دستور IOS + Verify", "L3": "طراحی و RCA", "L4": "سازمانی + Change Control"}.get(level, "")

def _vlan(topic, level):
    summary = (
        f"«{topic}»: VLAN شبکه منطقی روی سوییچ است. بدون مسیریابی لایه ۳، "
        f"دو VLAN مثل دو جزیره جدا هستند. در سازمان برای Users/Servers/VoIP/Guest جدا می‌شوند."
    )
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

---

## داستان سازمانی
ساختمان ۴ طبقه. VLAN10 کاربران، VLAN20 سرورها، VLAN30 تلفن، VLAN40 مهمان.
بعد از جابجایی سوییچ طبقه ۳، کاربران به فایل‌سرور نمی‌رسند. ARP گاهی ناقص است.
شما باید بفهمید مشکل از access است، trunk، یا inter-VLAN routing.

## تشبیه
ساختمان چندطبقه: هر طبقه یک VLAN. آسانسور (SVI/روتر) برای رفتن بین طبقه‌ها لازم است.
راهرو بین دو ساختمان (trunk) باید اجازه عبور چند طبقه را بدهد (allowed VLAN).

## مفاهیم کلیدی
| مفهوم | معنی عملی |
|-------|-----------|
| Access Port | یک VLAN به کلاینت — بدون تگ |
| Trunk | چند VLAN با تگ 802.1Q |
| Native VLAN | روی trunk بدون تگ؛ دو طرف باید یکی باشند |
| SVI | interface VlanX = gateway لایه ۳ همان VLAN |
| Allowed VLAN | لیست VLANهایی که از trunk عبور می‌کنند |

## فریم‌به‌فریم روی Trunk
1. کلاینت VLAN10 فریم بدون تگ می‌فرستد
2. سوییچ access تگ 10 می‌زند و روی trunk می‌فرستد
3. سوییچ مقابل تگ را می‌خواند و به پورت access VLAN10 می‌دهد
4. اگر مقصد VLAN20 باشد و L3 در مسیر باشد، SVI/روتر مسیریابی می‌کند

## عیب‌یابی سریع
| علامت | علت محتمل | دستور |
|-------|-----------|-------|
| پینگ داخل VLAN نه | پورت در VLAN اشتباه / shutdown | show vlan brief |
| بین دو سوییچ نه | trunk نیست یا allowed کم | show interfaces trunk |
| Native mismatch در لاگ | native دو طرف فرق دارد | show interfaces trunk |
| بین VLAN نه | SVI down یا ip routing off یا ACL | show ip interface brief |

## امنیت
- Native VLAN را از VLAN کاربران جدا کن (مثلاً VLAN999)
- Trunk را به allowed مشخص محدود کن
- Port-security روی access
"""
    commands = """# دستورات عملی VLAN

## مشاهده
```
show vlan brief
```
```
show interfaces trunk
```
```
show interfaces switchport
```
```
show mac address-table vlan 10
```

## پیکربندی Access
```
interface Gi0/1
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
 spanning-tree bpduguard enable
 no shutdown
```

## پیکربندی Trunk
```
interface Gi0/24
 switchport mode trunk
 switchport trunk native vlan 999
 switchport trunk allowed vlan 10,20,30
```

## SVI (Gateway)
```
interface Vlan10
 ip address 10.10.10.1 255.255.255.0
 no shutdown
```
```
ip routing
```
"""
    lab = f"""# Lab عملی — {topic}

## توپولوژی
دو سوییچ، دو کلاینت. کلاینت A روی SW1، کلاینت B روی SW2.

## مراحل
1. VLAN 10 و 20 بساز
2. پورت کلاینت‌ها access VLAN10
3. لینک بین سوییچ‌ها trunk با allowed 10,20
4. پینگ بین دو کلاینت باید OK شود
5. یکی را به VLAN20 ببر — بدون L3 نباید به هم برسند
6. SVI بساز و inter-VLAN را تست کن
7. عمداً allowed را خراب کن و با show interfaces trunk پیدا کن

## جدول ثبت
| مرحله | نتیجه | دستور تأیید |
|-------|--------|-------------|
| پینگ هم‌VLAN | | |
| پینگ بین‌VLAN بدون SVI | باید fail | |
| بعد از SVI | | |
"""
    return summary, full, commands, lab

def _stp(topic, level):
    summary = (
        f"«{topic}»: بدون STP، یک کابل اضافه می‌تواند کل شبکه را با broadcast storm بکشد. "
        f"STP یک مسیر Forward نگه می‌دارد و بقیه را Block می‌کند."
    )
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

---

## داستان سازمانی
تیم کابل‌کشی یک uplink backup بین دو سوییچ access گذاشت. در کمتر از یک دقیقه
CPU سوییچ‌ها ۱۰۰٪ شد، تلفن‌ها و دوربین‌ها قطع شدند. لاگ پر از MACFLAP بود.

## تشبیه
خیابان یک‌طرفه با پل اضافی: اگر هر دو پل باز باشند و پلیس (STP) نباشد،
ماشین‌ها (broadcast) دور خود می‌چرخند تا بنزین تمام شود (شبکه می‌میرد).

## مفاهیم
| مفهوم | نقش |
|-------|-----|
| Root Bridge | مرجع توپولوژی (کم‌ترین Bridge ID) |
| Root Port | نزدیک‌ترین پورت هر سوییچ به Root |
| Designated Port | مسئول هر سگمنت |
| Blocking / Alternate | جلوی loop |
| BPDU | پیام کنترل STP |
| PortFast | رد شدن از listening/learning روی کلاینت |
| BPDU Guard | اگر روی access BPDU آمد → err-disable |

## RSTP در برابر STP کلاسیک
RSTP (802.1w) همگرایی خیلی سریع‌تر دارد. در سازمان امروزی rapid-pvst یا MST ترجیح داده می‌شود.

## عیب‌یابی
| علامت | علت | اقدام |
|-------|-----|-------|
| storm / CPU 100% | loop، STP off یا لینک جدید | کابل مشکوک را بکش |
| err-disabled روی access | BPDU Guard | دستگاه غیرمجاز را جدا کن |
| Root مدام عوض می‌شود | اولویت یکسان / flapping | Root را دستی primary کن |
"""
    commands = """# دستورات STP

```
show spanning-tree
```
```
show spanning-tree vlan 10 detail
```
```
spanning-tree mode rapid-pvst
```
```
spanning-tree vlan 10 root primary
```
```
interface Gi0/1
 spanning-tree portfast
 spanning-tree bpduguard enable
```
```
show spanning-tree inconsistentports
```
"""
    lab = f"""# Lab — {topic}

1. سه سوییچ حلقه بساز (بدون STP اول — فقط در Lab ایزوله!)
2. STP را روشن کن و ببین کدام پورت Block شد
3. Root را عوض کن و reconvergence را تماشا کن
4. PortFast + BPDU Guard روی پورت کلاینت
5. یک سوییچ کوچک به پورت access بزن و ببین err-disable می‌شود
"""
    return summary, full, commands, lab

def _etherchannel(topic, level):
    summary = (
        f"«{topic}»: چند لینک فیزیکی را یک Port-Channel منطقی می‌کند. "
        f"پهنای بیشتر + افزونگی؛ STP کل باندل را یک پورت می‌بیند."
    )
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

---

## داستان
بین distribution و access دو کابل ۱G دارید. می‌خواهید ۲G منطقی و redundancy بدون اینکه STP یکی را Block کند.

## شروط حیاتی
- سرعت و duplex دو طرف یکسان
- mode یکسان (LACP active/active توصیه می‌شود)
- trunk/access و allowed VLAN یکسان
- نباید یکی از اعضا PortFast داشته باشد

## عیب‌یابی
| علامت | علت |
|-------|-----|
| باندل تشکیل نمی‌شود | mode یا سرعت ناسازگار |
| یک عضو out-of-bundle | کابل همان عضو یا تنظیمات فرق |
"""
    commands = """```
show etherchannel summary
```
```
interface range Gi0/1-2
 channel-group 1 mode active
```
```
interface Port-channel1
 switchport mode trunk
 switchport trunk allowed vlan 10,20,30
```
"""
    lab = f"""# Lab — {topic}
1. دو لینک را LACP کن
2. show etherchannel summary → وضعیت P
3. یک کابل را بکش — ترافیک باید روی عضو دیگر بماند
4. عمداً duplex را خراب کن و ببین عضو خارج می‌شود
"""
    return summary, full, commands, lab

def _l2sec(topic, level):
    summary = (
        f"«{topic}»: لبه شبکه را قفل کن — Port-Security، DHCP Snooping، DAI، BPDU Guard. "
        f"هسته را ساده نگه دار."
    )
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

---

## داستان
کاربر کارت شبکه لپ‌تاپ را عوض کرد و پورت err-disabled شد (Port-Security maximum 1).
یا یک rogue DHCP روی لپ‌تاپ مهمان gateway اشتباه پخش کرد.

## ابزارها و نقش
| ابزار | کار |
|-------|-----|
| Port-Security | سقف تعداد MAC روی پورت |
| DHCP Snooping | فقط پورت trust حق دارد Offer بدهد |
| DAI | ARP را با binding جدول Snooping چک می‌کند |
| BPDU Guard | BPDU روی access → err-disable |
| Storm Control | سقف broadcast/multicast |

## عادت سازمانی
لبه (access) را سخت‌گیر کن؛ هسته و distribution را ساده و سریع.
"""
    commands = """```
switchport port-security
switchport port-security maximum 2
switchport port-security mac-address sticky
switchport port-security violation restrict
```
```
ip dhcp snooping
ip dhcp snooping vlan 10,20
interface Gi0/24
 ip dhcp snooping trust
```
```
ip arp inspection vlan 10
```
```
show port-security interface Gi0/1
```
"""
    lab = f"""# Lab — L2 Security
1. maximum 1 روی پورت Lab
2. دومین MAC را بفرست و violation را ببین
3. DHCP Snooping: یک پورت trust و بقیه untrusted
4. از پورت untrusted DHCP Offer بفرست — باید drop شود
"""
    return summary, full, commands, lab

def _dot1x(topic, level):
    summary = (
        f"«{topic}»: قبل از دسترسی کامل به LAN، کلاینت با EAP و RADIUS احراز هویت می‌شود. "
        f"MAB برای دستگاه‌های بدون 802.1X (با احتیاط)."
    )
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

---

## نقش‌ها
| نقش | کیست |
|-----|------|
| Supplicant | کلاینت (لپ‌تاپ) |
| Authenticator | سوییچ |
| Authentication Server | RADIUS (ISE و مشابه) |

## جریان ساده
پورت محدود → EAPOL → RADIUS → در صورت موفقیت: VLAN پویا / ACL / دیتای کامل

## MAB
اگر دستگاه 802.1X بلد نباشد (چاپگر، دوربین)، MAC Authentication Bypass.
ضعیف‌تر از 802.1X کامل — فقط با policy مشخص.
"""
    commands = """```
show dot1x all
```
```
show authentication sessions
```
```
show authentication sessions interface Gi0/1
```
"""
    lab = f"""# Lab — 802.1X
1. سه نقش را روی کاغذ برای دفتر خودت بکش
2. اگر Lab با ISE/FreeRADIUS داری: یک کلاینت موفق و یک ناموفق
3. show authentication sessions را تفسیر کن
"""
    return summary, full, commands, lab

_BUILDERS = {
    "vlan": _vlan,
    "stp": _stp,
    "etherchannel": _etherchannel,
    "l2sec": _l2sec,
    "dot1x": _dot1x,
}

def build_chapter13_lesson(title_fa: str, title_en: str = "") -> Dict[str, Any] | None:
    topic, level = _topic(title_fa), _level(title_fa)
    b = _bucket(topic)
    summary, full, commands, lab = _BUILDERS[b](topic, level)
    return {
        "summary": summary,
        "full_content": full,
        "commands": commands,
        "examples": lab,
        "notes": f"فصل۱۳ · {b} · {level} · محتوای غنی سازمانی",
        "lab": lab,
        "level": level,
        "topic": topic,
        "category": b,
        "chapter": 13,
    }
