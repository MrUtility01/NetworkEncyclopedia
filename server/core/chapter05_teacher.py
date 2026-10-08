# -*- coding: utf-8 -*-
"""فصل ۰۵ — فایل‌سیستم و Storage: FAT/NTFS · ext4 · MBR/GPT · RAID"""
from __future__ import annotations
import re
from typing import Any, Dict, Tuple

def _level(title: str) -> str:
    m = re.match(r"\[(L[0-4])\]", title or "")
    return m.group(1) if m else "L0"

def _topic(title: str) -> str:
    t = re.sub(r"^\[L[0-4]\]\s*", "", title or "")
    t = re.sub(r"\s*[—\-]\s*(آشنایی|مقدماتی|ادمین|مهندس|خبره|Intro|Junior|Admin|Senior|Architect).*$", "", t, flags=re.I)
    return t.strip()

def _bucket(topic: str) -> str:
    t = (topic or "").lower()
    if any(k in t for k in ("raid", "mirror", "stripe", "parity", "rebuild", "hot spare")):
        return "raid"
    if any(k in t for k in ("mbr", "gpt", "پارتیشن", "partition", "volume", "esp")):
        return "partition"
    if any(k in t for k in ("ext4", "ext3", "xfs", "btrfs", "inode", "fsck", "mount", "fstab", "journal")):
        return "linux_fs"
    if any(k in t for k in ("fat", "exfat", "ntfs", "refs", "bitlocker", "allocation")):
        return "windows_fs"
    if "linux" in t or "لینوکس" in t:
        return "linux_fs"
    if "windows" in t or "ویندوز" in t:
        return "windows_fs"
    return "partition"

def _depth(level: str) -> str:
    return {"L0": "تصویر ذهنی", "L1": "مثال+Lab", "L2": "دستور ادمین", "L3": "طراحی", "L4": "سازمانی"}.get(level, "")

def _windows_fs(topic, level):
    summary = f"«{topic}»: FAT32/exFAT برای جابه‌جایی؛ NTFS برای سیستم و سهم‌ها."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## تشبیه
دیسک = کتابخانه | فایل‌سیستم = قفسه‌بندی

## FAT32 · exFAT · NTFS
| | FAT32 | exFAT | NTFS |
|--|-------|-------|------|
| فایل خیلی بزرگ | محدودیت ~4GB | مناسب | عالی |
| مجوز | ضعیف | ضعیف | ACL قوی |
| کاربرد | USB قدیمی | فلش/تبادل | سیستم و Share |

C: → NTFS | فلش چندسیستمی → exFAT

## فریم‌به‌فریم Write روی NTFS
WriteFile → Cache → متادیتای NTFS → کلاستر دیسک → ژورنال

## خلاصه
انتخاب FS = سازگاری + اندازه + امنیت + پایداری
"""
    commands = """```
Get-Volume | Format-Table DriveLetter, FileSystem, SizeRemaining, Size
```
```
fsutil fsinfo volumeinfo C:
```
```
chkdsk C: /scan
```
```
icacls C:\\Windows
```
"""
    lab = """# Lab ویندوز FS
Get-Volume را ببین. برای ویدیو ۸گیگ FAT32 مناسب است؟ چرا؟
"""
    return summary, full, commands, lab

def _linux_fs(topic, level):
    summary = f"«{topic}»: پارتیشن با mount زیر مسیر می‌آید؛ ext4 رایج است."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## mount
/dev/sda1 --mount--> /

## ext4
ژورنال + inode (متادیتای فایل). XFS برای داده بزرگ سرور رایج است.

## فریم‌به‌فریم نوشتن
write → page cache → flush دیسک → ژورنال/متادیتا

## fstab و fsck
fstab اشتباه = emergency mode. fsck روی FS mount‌شده معمولاً نه.
"""
    commands = """```
lsblk -f
```
```
df -hT
```
```
findmnt
```
```
sudo blkid
```
```
cat /etc/fstab
```
```
stat /etc/hostname
```
"""
    lab = """# Lab لینوکس FS
lsblk -f و df -hT | stat یک فایل | cat fstab فقط خواندن
"""
    return summary, full, commands, lab

def _partition(topic, level):
    summary = f"«{topic}»: MBR قدیمی؛ GPT مدرن با UEFI و ESP."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## MBR در برابر GPT
| | MBR | GPT |
|--|-----|-----|
| بوت | BIOS Legacy | UEFI |
| دیسک بزرگ | محدودیت | مناسب |
| بازیابی جدول | ضعیف | هدر پشتیبان |

ترکیب رایج: UEFI + GPT + ESP + root/NTFS

## فریم‌به‌فریم بوت GPT
UEFI جدول را می‌خواند → ESP → Bootloader → OS

## احتیاط
diskpart/fdisk می‌توانند همه را پاک کنند. دو بار lsblk بخوان.
"""
    commands = """```
Get-Disk | Format-Table Number, FriendlyName, PartitionStyle, Size
```
```
Get-Partition
```
```
lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINT
```
```
sudo fdisk -l
```
```
sudo blkid
```
"""
    lab = """# Lab پارتیشن
PartitionStyle را ببین (GPT/MBR). ESP را پیدا کن. دیسک ۲TB ویندوز جدید: GPT چرا؟
"""
    return summary, full, commands, lab

def _raid(topic, level):
    summary = f"«{topic}»: RAID سرعت یا افزونگی می‌دهد — پشتیبان‌گیری نیست."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## قانون
RAID ≠ Backup

## سطوح
| سطح | ایده | حداقل دیسک |
|------|------|------------|
| 0 | Stripe سرعت | 2 |
| 1 | Mirror | 2 |
| 5 | Stripe+parity | 3 |
| 6 | دو parity | 4 |
| 10 | Mirror+Stripe | 4 |

## فریم RAID1
write روی هر دو دیسک؛ fail یکی → ادامه از روی دیگر؛ دیسک جدید → rebuild

## مانیتورینگ
Optimal / Degraded / Rebuild + SMART + آلارم
"""
    commands = """```
cat /proc/mdstat
```
```
sudo mdadm --detail /dev/md0 2>/dev/null
```
```
Get-PhysicalDisk | Format-Table FriendlyName, HealthStatus, Size
```
```
Get-StoragePool
```
"""
    lab = """# Lab RAID
سناریو کاغذی: دو دیسک فقط سرعت؟ دو دیسک سیستم مهم؟ چهار دیسک DB؟
وضعیت mdstat یا PhysicalDisk را ببین.
"""
    return summary, full, commands, lab

_BUILDERS = {"windows_fs": _windows_fs, "linux_fs": _linux_fs, "partition": _partition, "raid": _raid}

def build_chapter05_lesson(title_fa: str, title_en: str = "") -> Dict[str, Any] | None:
    topic, level = _topic(title_fa), _level(title_fa)
    b = _bucket(topic)
    summary, full, commands, lab = _BUILDERS[b](topic, level)
    return {
        "summary": summary, "full_content": full, "commands": commands,
        "examples": lab, "notes": f"فصل۰۵ · {b} · {level} · RAID≠Backup", "lab": lab,
        "level": level, "topic": topic, "category": b, "chapter": 5,
    }
