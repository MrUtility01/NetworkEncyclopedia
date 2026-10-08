# -*- coding: utf-8 -*-
"""فصل ۰۳ — BIOS/UEFI و فرآیند بوت — استادمحور + Lab"""
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
    if any(k in t for k in ("bios", "uefi", "firmware", "فریمور", "cmos", "setup", "secure boot", "tpm", "boot order", "legacy")):
        return "firmware"
    if any(k in t for k in ("boot", "بوت", "post", "mbr", "gpt", "grub", "bootloader", "bootmgr", "initrd", "kernel", "زنجیره", "efi", "esp")):
        return "boot"
    return "firmware"

def _depth(level: str) -> str:
    return {"L0": "تصویر ذهنی", "L1": "مثال+Lab", "L2": "دستور ادمین", "L3": "طراحی/عیب‌یابی", "L4": "استاندارد سازمانی"}.get(level, "")

def _firmware(topic: str, level: str):
    summary = f"«{topic}»: فیرمور اولین نرم‌افزار بعد از روشن شدن است؛ سخت‌افزار را زنده می‌کند و کنترل را به Bootloader می‌دهد."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## تشبیه
نگهبان ساختمان = BIOS/UEFI | کلید اتاق‌ها = تنظیمات CMOS/NVRAM | مدیر = Bootloader | ساکنین = OS

## BIOS در برابر UEFI
| | BIOS | UEFI |
|--|------|------|
| سن | قدیمی | استاندارد مدرن |
| دیسک | MBR کلاسیک | GPT + دیسک بزرگ |
| امنیت | محدود | Secure Boot |
| سرعت | کندتر | معمولاً سریع‌تر |

سازمان: ترجیح **UEFI + GPT**.

## CMOS/NVRAM
ترتیب بوت، ساعت، VT-x، Secure Boot. باتری ضعیف → ریست تنظیمات/ساعت.

## فریم‌به‌فریم Setup
1) روشن 2) Del/F2/F10 3) منو 4) تغییر 5) Save & Exit

## Secure Boot
فقط Bootloader امضاشده. Production: روشن. Lab: گاهی موقت خاموش.

## امنیت ادمین
پسورد Setup، محدود کردن USB boot، آپدیت فیرمور فقط رسمی، ثبت نسخه در دارایی.

## خلاصه
فیرمور پل «برق آمد» تا «OS بالا آمد» است؛ UEFI نسخه مدرن این پل است.
"""
    commands = f"""# — {topic}
## ویندوز
```
msinfo32
```
```
Get-ComputerInfo | Select BiosFirmwareType, BiosVersion
```
## لینوکس
```
sudo dmidecode -t bios
```
```
[ -d /sys/firmware/efi ] && echo UEFI || echo Legacy
```
```
efibootmgr -v
```
"""
    lab = f"""# آزمایشگاه — {topic}

## آزمایش ۱: UEFI یا Legacy؟
ویندوز: msinfo32 → BIOS Mode
لینوکس:
```
[ -d /sys/firmware/efi ] && echo UEFI || echo BIOS
```

## آزمایش ۲: نسخه فیرمور
```
sudo dmidecode -t bios | head -20
```

## آزمایش ۳: فقط نگاه به Setup
Restart → کلید Setup → Boot Order و Secure Boot را پیدا کن → Exit بدون Save

| لحظه | رخداد |
|------|--------|
| Power | فیرمور اجرا |
| POST | چک سخت‌افزار |
| Setup | اگر کلید زدی |
| Boot | تحویل به Bootloader |
"""
    return summary, full, commands, lab

def _boot(topic: str, level: str):
    summary = f"«{topic}»: بوت زنجیره است: Power → Firmware → Bootloader → Kernel → سرویس‌ها."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## زنجیره
```
Power → POST/Firmware → وسیله بوت → Bootloader (BOOTMGR/GRUB)
     → Kernel → init/systemd → Login
```

## MBR در برابر GPT
مدرن: UEFI + GPT. ESP = پارتیشن FAT مخصوص فایل‌های بوت UEFI.

## فریم‌به‌فریم ویندوز
UEFI → BOOTMGR → BCD → کرنل → Login

## فریم‌به‌فریم لینوکس
UEFI → GRUB → kernel+initrd → systemd → ورود

## PXE
بوت شبکه برای نصب جمعی (DHCP + TFTP/HTTP).

## عیب‌یابی حلقه
| علامت | حلقه مشکوک |
|--------|------------|
| بدون تصویر | POST/سخت‌افزار |
| No bootable device | ترتیب بوت/دیسک/ESP |
| GRUB/لوگو می‌ماند | Bootloader |
| Login می‌آید سرویس down | لایه OS |

## امنیت
Secure Boot، پسورد Setup، قفل USB boot، محافظت ESP.

## خلاصه
بوت مسابقه امدادی است؛ چوب را درست به نفر بعدی بده.
"""
    commands = f"""# — {topic}
## ویندوز
```
msinfo32
```
```
bcdedit /enum firmware
```
## لینوکس
```
lsblk -o NAME,SIZE,TYPE,MOUNTPOINT,FSTYPE
```
```
efibootmgr -v
```
```
cat /proc/cmdline
```
```
systemctl list-units --failed
```
"""
    lab = f"""# آزمایشگاه — {topic}

## آزمایش ۱: مشاهده زنجیره
Restart کن: لوگو مادربورد؟ GRUB؟ مستقیم OS؟ زمان تا Login؟

## آزمایش ۲: پیدا کردن ESP
```
lsblk -f
```
پارتیشن vfat کوچک اغلب EFI است.

## آزمایش ۳ کاغذی
«No bootable device» — سه فرضیه و سه اقدام بدون پاک کردن دیسک بنویس.

| مرحله | نشانه | اگر بشکند |
|--------|--------|----------|
| POST | لوگوی برد | بی‌تصویر |
| Bootloader | GRUB/لوگو OS | خطا/منو |
| Kernel | سیاهی کوتاه | پنیک/BSOD |
| Userspace | سرویس‌ها | Login با سرویس down |
"""
    return summary, full, commands, lab

def build_chapter03_lesson(title_fa: str, title_en: str = "") -> Dict[str, Any] | None:
    topic, level = _topic(title_fa), _level(title_fa)
    b = _bucket(topic)
    summary, full, commands, lab = (_firmware if b == "firmware" else _boot)(topic, level)
    return {
        "summary": summary, "full_content": full, "commands": commands,
        "examples": lab, "notes": f"فصل۰۳ · {b} · {level}", "lab": lab,
        "level": level, "topic": topic, "category": b, "chapter": 3,
    }
