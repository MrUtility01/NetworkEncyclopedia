# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import Dict

def _depth_note(level: str) -> str:
    return {"L0": "تصویر ذهنی", "L1": "مثال+Lab", "L2": "دستور ادمین", "L3": "طراحی", "L4": "سازمانی"}.get(level, "")

def _cpu(topic: str, level: str) -> Dict[str, str]:
    summary = (
        f"«{topic}»: پردازنده مغز سیستم است؛ دستور می‌گیرد، محاسبه می‌کند، نتیجه را برمی‌گرداند. "
        "این درس قدم‌به‌قدم نشان می‌دهد داخل CPU چه اتفاقی می‌افتد — مثل دیدن یک «فریم‌به‌فریم»."
    )
    full = f"""# {topic}

**سطح:** {level} — {_depth_note(level)}

## داستان ساده (مثل کلاس حضوری)

فرض کن یک آشپزخانه داری:
- **دستور غذا** = Instruction
- **آشپز** = CPU
- **کانتر** = Register / Cache
- **یخچال** = RAM
- **زیرزمین** = دیسک

چرخه اجرا: **Fetch → Decode → Execute → Write-back**

### فریم‌به‌فریم
1. **Fetch:** دستور از حافظه/کش می‌آید
2. **Decode:** CU می‌فهمد چه دستوری است
3. **Execute:** ALU محاسبه می‌کند
4. **Write-back:** نتیجه نوشته می‌شود

**ALU** = ماشین‌حساب | **CU** = مدیر صحنه
**Core** = آشپز واقعی | **Thread** = نوبت کاری (SMT)
**Cache L1/L2/L3:** هرچه نزدیک‌تر به core، سریع‌تر؛ Cache Miss → رفتن سراغ RAM

## مثال
فرکانس ۳GHz یعنی ظرفیت خام خیلی بالا؛ در عمل انتظار حافظه و branch mispredict عدد واقعی را کم می‌کند.

## ارتباط شبکه
CPU بالا + softirq شبکه → ممکن است drop بسته ببینی. فرق user با kernel/softirq را بشناس.

## امنیت
میکروکد/فیرمور، غیرفعال ویژگی آزمایشی بایوس وقتی لازم نیست.

## خلاصه
CPU کار را فریم‌به‌فریم انجام می‌دهد؛ داده نزدیک‌تر = کار سریع‌تر.
"""
    commands = f"""# دستورات — {topic}

## ویندوز
```
wmic cpu get Name,NumberOfCores,NumberOfLogicalProcessors,MaxClockSpeed
```
```
Get-CimInstance Win32_Processor | Format-List Name,NumberOfCores,NumberOfLogicalProcessors,LoadPercentage
```
```
msinfo32
```

## لینوکس
```
lscpu
```
```
cat /proc/cpuinfo | head -40
```
```
mpstat -P ALL 1 5
```
```
perf stat -e cycles,instructions,cache-misses sleep 2
```
"""
    lab = f"""# آزمایشگاه — {topic}

## آزمایش ۱: بیکار و زیر فشار
1. Task Manager یا top را باز کن
2. بار بیکار را ببین
3. کار سنگین بزن (مثلاً stress)
4. کدام هسته‌ها پر شدند؟

```
stress -c 2 -t 20
```

## آزمایش ۲: Core در برابر Thread
با lscpu یا WMIC مقایسه کن.

## آزمایش ۳: گلوگاه واقعی
کپی فایل بزرگ + نگاه به CPU. اگر CPU پایین و دیسک بالا → گلوگاه IO است.

| لحظه | رخداد |
|------|--------|
| شروع برنامه | دستورات وارد CPU |
| حلقه محاسبه | ALU/Cache مشغول |
| انتظار IO | CPU ممکن است بیکار بماند |
"""
    return summary, full, commands, lab
