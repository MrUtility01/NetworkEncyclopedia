# -*- coding: utf-8 -*-
"""فصل ۰۲ — اسمبل، POST، نگهداری، سرور HP"""
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
    t = topic.lower()
    if any(k in t for k in ("esd", "ایمنی", "اسمبل", "assembly", "کابل", "نصب")):
        return "assembly"
    if any(k in t for k in ("post", "beep", "بایوس", "bios", "uefi", "عیب", "خطا", "troubleshoot")):
        return "post"
    if any(k in t for k in ("تمیز", "نگهداری", "گرد", "thermal", "خمیر", "fan", "خنک")):
        return "maintain"
    if any(k in t for k in ("hp", "proliant", "ilo", "سرور", "server", "rack", "blade")):
        return "server"
    return "assembly"

def _assembly(topic, level):
    summary = f"«{topic}»: اسمبل درست = پایداری. ESD و ترتیب نصب را جدی بگیر."
    full = f"""# {topic}

**سطح:** {level}

## ایمنی اول
دستبند ESD، سطح مناسب، برق قطع.

## ترتیب اسمبل
1) CPU 2) خمیر 3) خنک‌کننده 4) RAM 5) مادربورد در کیس 6) PSU 7) دیسک 8) PCIe 9) پنل جلو

## فریم‌به‌فریم روشن شدن
پاور → ریل PSU → POST → تصویر/بوت

## ایمنی
فرش+جوراب خطرناک؛ PSU باز را دستکاری نکن.
"""
    commands = """```
msinfo32
```
```
lscpu && free -h && lsblk
```
"""
    lab = """# آزمایشگاه اسمبل
شناسنامه سخت‌افزار بنویس. Bench test قبل از بستن درب.
| اشتباه | نتیجه |
|--------|--------|
| استندآف جا افتاده | شورت |
| RAM نصفه | POST fail |
"""
    return summary, full, commands, lab

def _post(topic, level):
    summary = f"«{topic}»: POST خودآزمایی روشن‌شدن است؛ beep/LED راهنمای عیب‌اند."
    full = f"""# {topic}

**سطح:** {level}

POST: تغذیه → CPU → RAM → تصویر → بوت.
حداقل‌سازی: CPU+یک رم+PSU(+GPU).
Beep codes به سازنده بستگی دارد — دفترچه مادربورد مرجع است.
"""
    commands = """```
msinfo32
```
```
sudo dmidecode -t bios
```
"""
    lab = """# Lab POST
سناریو: روشن می‌شود تصویر نیست. فرضیه‌ها را یکی‌یکی با حداقل‌سازی رد کن.
"""
    return summary, full, commands, lab

def _maintain(topic, level):
    summary = f"«{topic}»: گرد و خمیر خشک = دمای بالا."
    full = f"""# {topic}

**سطح:** {level}

گردگیری دوره‌ای، جریان هوا، تجدید خمیر وقتی دما غیرعادی است.
فریم حرارتی: بار → دما بالا → throttle یا قطع.
"""
    commands = """```
sensors
```
"""
    lab = """# Lab دما
idle را یادداشت کن، ۵ دقیقه بار بده، پیک را مقایسه کن.
"""
    return summary, full, commands, lab

def _server(topic, level):
    summary = f"«{topic}»: سرور = ECC + PSU اضافه + iLO/IPMI + hot-plug."
    full = f"""# {topic}

**سطح:** {level}

iLO: کنسول و سنسور حتی بدون OS.
امنیت iLO: پسورد قوی، فقط شبکه مدیریت، فیرمور به‌روز.
"""
    commands = """```
sudo dmidecode -t system | head
```
```
ipmitool sensor 2>/dev/null | head
```
"""
    lab = """# Lab سرور
اگر iLO داری Sensors را ببین. وگرنه شناسنامه با dmidecode.
"""
    return summary, full, commands, lab

def build_chapter02_lesson(title_fa: str, title_en: str = "") -> Dict[str, Any] | None:
    topic, level = _topic(title_fa), _level(title_fa)
    b = _bucket(topic)
    fn = {"assembly": _assembly, "post": _post, "maintain": _maintain, "server": _server}[b]
    summary, full, commands, lab = fn(topic, level)
    return {
        "summary": summary, "full_content": full, "commands": commands,
        "examples": lab, "notes": f"فصل۰۲ · {b} · {level}", "lab": lab,
        "level": level, "topic": topic, "category": b, "chapter": 2,
    }
