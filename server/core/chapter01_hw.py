# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import Dict

def _depth_note(level: str) -> str:
    return {"L0": "تصویر ذهنی", "L1": "مثال+Lab", "L2": "دستور ادمین", "L3": "طراحی", "L4": "سازمانی"}.get(level, "")

def _ram(topic: str, level: str) -> Dict[str, str]:
    summary = f"«{topic}»: RAM میز کار سیستم است. میز بزرگ‌تر = کمتر رفتن سراغ دیسک."
    full = f"""# {topic}

**سطح:** {level} — {_depth_note(level)}

RAM مثل میز تحریر است. کمبود RAM → paging/swap → کندی و دیسک شلوغ.

### فریم‌به‌فریم دسترسی حافظه
1. CPU آدرس می‌خواهد
2. Cache hit؟ برگرد
3. وگرنه کنترلر حافظه + ماژول DDR
4. داده برمی‌گردد

DDR4/DDR5 باید با CPU/مادربرد سازگار باشد. ECC بیشتر برای سرور.

## امنیت
ECC و سلامت ماژول در لاگ مدیریت سرور؛ cold-boot در سطح پیشرفته.
"""
    commands = """# ویندوز
```
wmic memorychip get Capacity,Speed,Manufacturer
```
```
Get-CimInstance Win32_OperatingSystem | Select TotalVisibleMemorySize,FreePhysicalMemory
```
# لینوکس
```
free -h
```
```
sudo dmidecode -t memory | less
```
```
vmstat 1 5
```
"""
    lab = """# Lab حافظه
1. free -h یا Task Manager را ببین
2. برنامه‌های سنگین باز کن
3. Available کم شد؟
4. vmstat: si/so بالا = فشار RAM
| رویداد | نشانه |
|--------|--------|
| Cache hit | سریع |
| RAM کم | hard fault / swap |
"""
    return summary, full, commands, lab

def _storage(topic: str, level: str) -> Dict[str, str]:
    summary = f"«{topic}»: ذخیره‌سازی ماندگار. مهم IOPS و تأخیر است نه فقط GB."
    full = f"""# {topic}

**سطح:** {level} — {_depth_note(level)}

HDD = دسترسی تصادفی ضعیف | SSD SATA = تأخیر کم | NVMe = صف‌های زیاد و مسیر PCIe

### فریم‌به‌فریم read
1. برنامه read می‌زند
2. page cache یا دیسک
3. فرمان SATA/NVMe
4. داده در بافر

در شبکه: لاگ و DB روی دیسک اشباع → سرویس «کند شبکه» به نظر می‌رسد.

## امنیت
BitLocker/LUKS، پاک‌سازی قبل اسقاط، جدا کردن دیسک لاگ.
"""
    commands = """# ویندوز
```
Get-PhysicalDisk | Format-Table FriendlyName,MediaType,BusType,HealthStatus,Size
```
# لینوکس
```
lsblk -o NAME,SIZE,TYPE,MOUNTPOINT,ROTA,MODEL
```
```
sudo smartctl -a /dev/sda
```
```
iostat -xz 1 5
```
"""
    lab = """# Lab دیسک
Task Manager یا iostat را ببین. util~100% = گلوگاه دیسک.
کپی چند گیگ و زمان را حس کن (SSD در برابر HDD).
"""
    return summary, full, commands, lab

def _mb(topic: str, level: str) -> Dict[str, str]:
    summary = f"«{topic}»: مادربورد میدان اتصال CPU/RAM/PCIe/دیسک/شبکه است."
    full = f"""# {topic}

**سطح:** {level} — {_depth_note(level)}

نقش‌ها: سوکت CPU، Chipset، اسلات RAM، PCIe، BIOS/UEFI.

### بوت فریم‌به‌فریم
1. PSU پایدار
2. UEFI مقداردهی
3. وسیله بوت
4. Bootloader
5. کرنل OS

## امنیت UEFI
پسورد بایوس، Secure Boot، بوت USB محدود، آپدیت کنترل‌شده فیرمور.
"""
    commands = """```
wmic baseboard get Product,Manufacturer,Version
```
```
sudo dmidecode -t baseboard
```
```
lspci | head
```
"""
    lab = """# Lab مادربورد
lspci یا Device Manager را ببین. قبل خرید: QVL پردازنده و رم را چک کن.
"""
    return summary, full, commands, lab

def _psu(topic: str, level: str) -> Dict[str, str]:
    summary = f"«{topic}»: تغذیه = پایداری. توان واقعی + حاشیه + 80Plus."
    full = f"""# {topic}

**سطح:** {level} — {_depth_note(level)}

کمبود توان → ریست زیر بار. محاسبه: جمع اجزا + ۲۰–۳۰٪ حاشیه.
در رک: PSU اضافه (redundant) و آلارم fail.

## ایمنی
کابل درست، دستکاری نکردن PSU باز، زمین رک.
"""
    commands = """# سرور مدیریت‌دار: iLO/iDRAC/IPMI سنسور توان
```
sensors
```
"""
    lab = """# Lab تغذیه
برچسب توان PSU را بخوان و با تخمین مصرف قطعات مقایسه کن.
روی سرور: وضعیت redundant PSU را در پنل ببین.
"""
    return summary, full, commands, lab

def _general(topic: str, level: str) -> Dict[str, str]:
    summary = f"«{topic}»: لایه سخت‌افزار تا جایی که OS می‌نشیند."
    full = f"""# {topic}

**سطح:** {level} — {_depth_note(level)}

لایه‌ها: برق → CPU/RAM → باس/دیسک → OS → شبکه/سرویس.
گلوگاه را با مشاهده پیدا کن نه حدس.
"""
    commands = """```
systeminfo
```
```
lscpu && free -h && lsblk
```
"""
    lab = """# Lab شناسنامه
CPU / RAM / Disk / بوت (BIOS|UEFI) را برای همین ماشین بنویس.
"""
    return summary, full, commands, lab
