# -*- coding: utf-8 -*-
"""فصل ۰۴ — سیستم‌عامل پایه: Kernel · ویندوز · لینوکس · عیب‌یابی منابع"""
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
    if any(k in t for k in ("kernel", "هسته", "process", "thread", "scheduler", "syscall", "user mode", "مفهوم", "virtual memory")):
        return "kernel"
    if any(k in t for k in ("registry", "ویندوز", "windows", "powershell", "event viewer", "task manager", "services", "ntfs")):
        return "windows"
    if any(k in t for k in ("لینوکس", "linux", "سلسله", "filesystem", "systemd", "chmod", "journalctl", "fhs", "ext4", "inode")):
        return "linux"
    if any(k in t for k in ("cpu بالا", "منابع", "resource", "swap", "گلوگاه", "iostat", "bottleneck", "load", "عیب")):
        return "resource"
    return "kernel"

def _depth(level: str) -> str:
    return {"L0": "تصویر ذهنی", "L1": "مثال+Lab", "L2": "دستور ادمین", "L3": "تحلیل گلوگاه", "L4": "استاندارد سازمانی"}.get(level, "")

def _kernel(topic, level):
    summary = f"«{topic}»: هسته (Kernel) واسط سخت‌افزار و برنامه‌هاست؛ برنامه مستقیم به دیسک/رم دست نمی‌زند."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## تشبیه
برنامه = مشتری رستوران | Kernel = آشپزخانه | سخت‌افزار = اجاق و مواد

## User Mode در برابر Kernel Mode
| | User | Kernel |
|--|------|--------|
| دسترسی | غیرمستقیم | مستقیم |
| خرابی | معمولاً همان برنامه | ممکن است کل سیستم |

## Process و Thread
Process = برنامه در حال اجرا با حافظه جدا | Thread = مسیر اجرا داخل همان process

## فریم‌به‌فریم read فایل
1) برنامه read می‌زند 2) Syscall وارد Kernel 3) مجوز و مسیر 4) Cache یا دیسک 5) بازگشت به User

## Scheduler و حافظه مجازی
نوبت CPU را Kernel می‌دهد. صفحه (page) به RAM یا swap نگاشت می‌شود. کمبود RAM → فشار swap → کندی.

## خلاصه
Kernel نگهبان منابع است.
"""
    commands = f"""# — {topic}
## ویندوز
```
tasklist
```
```
Get-Process | Sort-Object CPU -Descending | Select-Object -First 10
```
## لینوکس
```
ps aux --sort=-%cpu | head
```
```
top
```
```
free -h
```
```
uname -r
```
"""
    lab = f"""# آزمایشگاه — {topic}

## آزمایش ۱: دیدن processها
Task Manager یا `ps aux | head`

## آزمایش ۲: بار CPU
Idle را ببین → کار سنگین → کدام process بالا است؟

## آزمایش ۳: نسخه Kernel/OS
```
uname -a
```
یا winver

| رخداد | معنی |
|--------|------|
| Syscall | ورود به Kernel |
| Context switch | عوض شدن نوبت |
| Page fault | صفحه در RAM نبود |
"""
    return summary, full, commands, lab

def _windows(topic, level):
    summary = f"«{topic}»: ویندوز ادمین = Services + Event Log + Registry (با احتیاط) + PowerShell."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## Registry
HKLM = کل سیستم | HKCU = کاربر جاری
**قانون:** قبل از تغییر Export/بکاپ. روی Production بدون Change دست نزن.

## Services
برنامه پس‌زمینه با عمر طولانی. services.msc یا Get-Service

## Event Viewer
لاگ System/Application/Security برای RCA زمانی.

## فریم‌به‌فریم لاگین دامنه (مفهوم)
رمز → DC (Kerberos) → Profile/GPO → Desktop
ساعت کج → Kerberos می‌شکند.

## NTFS
Share + NTFS؛ سخت‌گیرانه‌تر برنده است. Inheritance را بفهم.

## امنیت
UAC را بی‌دلیل خاموش نکن؛ ادمین محلی فقط وقتی لازم است.
"""
    commands = f"""# — {topic}
```
winver
```
```
systeminfo
```
```
Get-Service | Where-Object Status -ne 'Running' | Select -First 20
```
```
Get-WinEvent -LogName System -MaxEvents 15
```
```
Get-Process | Sort CPU -Desc | Select -First 8
```
```
reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion /v ProgramFilesDir
```
"""
    lab = f"""# آزمایشگاه ویندوز — {topic}

1) winver + systeminfo — نسخه را یادداشت کن
2) services.msc — فقط مشاهده Startup Type
3) Event Viewer → System → خطاهای ۲۴ساعت — یک Event ID یادداشت کن
4) Task Manager → Sort by CPU/Memory

| ابزار | کاربرد |
|--------|--------|
| Task Manager | نمای سریع |
| Event Viewer | RCA |
| services.msc | سرویس‌ها |
| regedit | خطرناک |
"""
    return summary, full, commands, lab

def _linux(topic, level):
    summary = f"«{topic}»: لینوکس = همه‌چیز فایل + process + permission + systemd."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## FHS خلاصه
| مسیر | نقش |
|------|-----|
| / | ریشه |
| /etc | تنظیمات |
| /var | لاگ و داده متغیر |
| /home | کاربران |
| /proc | نمای Kernel |
| /boot | کرنل و بوت |

## مجوز rwx
User Group Other — chmod/chown با احتیاط روی Production

## systemd
systemctl status/start/stop | journalctl -u نام -n 50

## فریم‌به‌فریم اجرای دستور
Shell → PATH → fork+exec → ps → کد خروج $?

## خلاصه
اول مسیرها، بعد مجوز، بعد سرویس، بعد لاگ.
"""
    commands = f"""# — {topic}
```
uname -a
```
```
cat /etc/os-release
```
```
ls /
```
```
df -h
```
```
ps aux | head
```
```
systemctl list-units --failed
```
```
journalctl -p err -n 20 --no-pager
```
```
free -h && uptime
```
```
ip -br a
```
"""
    lab = f"""# آزمایشگاه لینوکس — {topic}

## ۱ گردش FHS
```
ls /etc | head; ls /var/log | head; ls /proc | head
```
/proc دیسک واقعی نیست.

## ۲ یک سرویس
```
systemctl status systemd-journald
```

## ۳ لاگ خطا
```
journalctl -p err -n 30 --no-pager
```

## ۴ مجوز
```
ls -l /etc/hostname
```
"""
    return summary, full, commands, lab

def _resource(topic, level):
    summary = f"«{topic}»: کندی همیشه CPU نیست؛ گلوگاه CPU / RAM / Disk / Network را جدا کن."
    full = f"""# {topic}

**سطح:** {level} — {_depth(level)}

## چهار گلوگاه
1) CPU 2) Memory/swap 3) Disk I/O 4) Network

## فریم‌به‌فریم «سیستم کند است»
1) همه جا یا یک اپ؟ 2) Load/Task Manager 3) CPU کدام process؟ 4) RAM/swap؟ 5) دیسک 100%؟ 6) DNS/شبکه؟

## نشانه‌ها
CPU 100% یک process = حلقه/تک‌نخی | Disk util بالا + CPU پایین = I/O | swap زیاد = کمبود RAM

## خلاصه
سوال: کدام منبع تمام شده؟
"""
    commands = f"""# — {topic}
## ویندوز
```
Get-Process | Sort CPU -Desc | Select -First 10
```
```
Get-Process | Sort WorkingSet64 -Desc | Select -First 10
```
## لینوکس
```
uptime
```
```
mpstat 1 5
```
```
free -h
```
```
vmstat 1 5
```
```
iostat -xz 1 5
```
```
ss -s
```
"""
    lab = f"""# آزمایشگاه منابع — {topic}

1) Baseline در حالت آرام
2) بار بده (فشرده‌سازی / کپی بزرگ / تب زیاد)
3) همزمان CPU و RAM و Disk را ببین
4) یک جمله RCA: «کندی از X بود چون Y دیدم»

| نشانه | گلوگاه |
|--------|--------|
| CPU 100% یک process | محاسبه |
| Disk 100% | I/O |
| RAM پر + swap | حافظه |
| DNS/ping کند | شبکه |
"""
    return summary, full, commands, lab

_BUILDERS = {"kernel": _kernel, "windows": _windows, "linux": _linux, "resource": _resource}

def build_chapter04_lesson(title_fa: str, title_en: str = "") -> Dict[str, Any] | None:
    topic, level = _topic(title_fa), _level(title_fa)
    b = _bucket(topic)
    summary, full, commands, lab = _BUILDERS[b](topic, level)
    return {
        "summary": summary, "full_content": full, "commands": commands,
        "examples": lab, "notes": f"فصل۰۴ · {b} · {level}", "lab": lab,
        "level": level, "topic": topic, "category": b, "chapter": 4,
    }
