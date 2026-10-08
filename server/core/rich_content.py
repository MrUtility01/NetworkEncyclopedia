# -*- coding: utf-8 -*-
"""محتوای غنی + دستورات با توضیح آرگومان برای ویندوز و اندروید."""
from __future__ import annotations

import re
from typing import Any, Dict


def level_tag(title: str) -> str:
    m = re.match(r"\[(L[0-4])\]", title or "")
    return m.group(1) if m else "L0"


def clean_topic(title: str) -> str:
    t = re.sub(r"^\[L[0-4]\]\s*", "", title or "").strip()
    t = re.sub(
        r"\s*[—\-]\s*(آشنایی|مقدماتی|ادمین|مهندس|خبره|Intro|Junior|Admin|Senior|Architect)\s*$",
        "",
        t,
        flags=re.I,
    )
    return t.strip() or (title or "موضوع")


_DEPTH = {
    "L0": dict(paras=3, cmds=4, examples=2, trouble=2),
    "L1": dict(paras=4, cmds=5, examples=2, trouble=3),
    "L2": dict(paras=5, cmds=7, examples=3, trouble=4),
    "L3": dict(paras=6, cmds=9, examples=3, trouble=5),
    "L4": dict(paras=7, cmds=11, examples=4, trouble=6),
}

_LEVEL_FA = {
    "L0": "آشنایی / مقدماتی",
    "L1": "کاربر فنی / Junior",
    "L2": "Administrator",
    "L3": "Engineer / Senior",
    "L4": "Architect / Enterprise",
}


def _commands_block(topic: str, level: str, d: dict) -> str:
    """دستورات با توضیح فارسی برای هر خط."""
    fw = (topic.split() or ["topic"])[0]
    lines = [
        f"# =====================================================",
        f"# دستورات عملی — {topic} | سطح {level}",
        f"# هر خط: دستور + توضیح کاربرد و آرگومان",
        f"# =====================================================",
        "",
        "# --- ۰) ایمنی قبل از تغییر ---",
        "# هدف: نقطه بازگشت داشته باشید",
        "copy running-config tftp://10.0.0.50/backup.cfg",
        "# توضیح: از running-config نسخه پشتیبان روی TFTP می‌گیرد",
        "# آرگومان: آدرس سرور TFTP و نام فایل backup",
        "",
        "enable",
        "# توضیح: ورود به حالت Privileged EXEC برای دستورات مدیریتی",
        "",
        "show running-config",
        "# توضیح: نمایش پیکربندی فعال فعلی برای مقایسه قبل/بعد",
        "",
        "# --- ۱) شناسایی و وضعیت ---",
        f"show version",
        "# توضیح: نسخه IOS/firmware، uptime، مدل دستگاه",
        "",
        f"show ip interface brief",
        "# توضیح: وضعیت up/down و IP هر اینترفیس — سریع برای Scope",
        "",
        f"show interfaces status",
        "# توضیح: VLAN، duplex، speed، connect — لایه دسترسی",
        "",
        f"show logging | include {fw}",
        f"# توضیح: فیلتر لاگ بر اساس کلمه کلیدی «{fw}» برای یافتن خطا",
        f"# آرگومان include: الگوی متنی جستجو در بافر لاگ",
        "",
        "# --- ۲) پیکربندی نمونه (Lab) ---",
        "configure terminal",
        "# توضیح: ورود به حالت پیکربندی سراسری",
        "",
    ]
    steps = max(2, d["cmds"] // 2)
    for i in range(steps):
        lines += [
            f"! --- گام {i + 1} مرتبط با {topic} ---",
            f"# هدف گام {i + 1}: اعمال بخش {i + 1} از پیکربندی «{topic}»",
            f"# پس از هر گام: end → show ... → بررسی خروجی",
            "",
        ]
    lines += [
        "end",
        "# توضیح: خروج از configure terminal به Privileged EXEC",
        "",
        "write memory",
        "# توضیح: ذخیره running در startup تا بعد از ریبوت باقی بماند",
        "# معادل: copy running-config startup-config",
        "",
        "# --- ۳) Verify ---",
        "show running-config | include ",
        f"# توضیح: فقط خطوط مرتبط را ببینید؛ الگوی جستجو را با نام «{topic}» تنظیم کنید",
        "",
        "show logging | last 50",
        "# توضیح: ۵۰ خط آخر لاگ برای خطای فوری بعد از تغییر",
        "# آرگومان last: تعداد خطوط انتهایی",
        "",
        "ping 8.8.8.8",
        "# توضیح: تست اتصال لایه ۳ به مقصد شناخته‌شده",
        "# آرگومان: آدرس IP مقصد",
        "",
        "traceroute 8.8.8.8",
        "# توضیح: مسیر hop-by-hop برای یافتن نقطه شکست",
        "",
        "# --- ۴) Rollback سریع ---",
        "# configure terminal",
        "# (برگرداندن دستورات معکوس)",
        "# end",
        "# write memory",
        "# توضیح: همیشه دستور معکوس را از قبل در Runbook بنویسید",
    ]
    if level in ("L2", "L3", "L4"):
        lines += [
            "",
            "# --- ۵) سطح عملیات سازمانی ---",
            "show processes cpu sorted",
            "# توضیح: فرآیندهای پرمصرف CPU — برای incident عملکردی",
            "",
            "show ip route",
            "# توضیح: جدول مسیریابی؛ default و routeهای خاص را چک کنید",
            "",
            "show cdp neighbors detail",
            "# توضیح: همسایه‌های متصل (اگر CDP فعال باشد) برای توپولوژی",
        ]
    if level in ("L3", "L4"):
        lines += [
            "",
            "# --- ۶) Engineer/Architect ---",
            "# - تغییر را در Change ثبت کنید",
            "# - قبل/بعد را در مستندات CMDB/NetBox بگذارید",
            "# - blast radius را قبل از apply برآورد کنید",
            f"# - برای «{topic}» تست از دو کلاینت در دو VLAN/سایت",
        ]
    return "\n".join(lines)


def build_rich_lesson(title_fa: str, title_en: str = "", level: str | None = None) -> Dict[str, Any]:
    level = level or level_tag(title_fa)
    topic = clean_topic(title_fa)
    d = _DEPTH.get(level, _DEPTH["L2"])
    level_name = _LEVEL_FA.get(level, level)

    summary = (
        f"دیدگاه کلی «{topic}» (سطح {level} — {level_name}): "
        f"این مبحث تعریف می‌کند موضوع چیست، در معماری شبکه/زیرساخت سازمان کجا قرار می‌گیرد، "
        f"چه پیش‌نیازی دارد، چه ریسکی در صورت پیکربندی غلط ایجاد می‌کند، و مهندس در این سطح "
        f"باید بتواند آن را توضیح دهد، در Lab پیاده کند، Verify کند و با روش ساخت‌یافته عیب‌یابی نماید. "
        f"خروجی مورد انتظار: درک مفهوم + کاربرد عملی + دستورات با معنی + مسیر Backup→Configure→Verify→Document."
    )

    parts: list[str] = []
    parts.append(f"# {topic}\n")
    parts.append(f"**سطح:** {level} — {level_name}\n")
    if title_en:
        parts.append(f"**EN:** {title_en}\n")
    parts.append("\n## خلاصه اجرایی\n\n" + summary + "\n")
    parts.append("\n## ۱) چیستی\n\n")
    parts.append(
        f"«{topic}» بخشی از دانش عملی مهندس شبکه/زیرساخت/امنیت است. "
        f"در سطح {level} باید جایش در توپولوژی، وابستگی‌ها و اثر شکست آن را بدانید.\n"
    )
    parts.append("\n## ۲) کاربرد سازمانی\n\n")
    parts.append(
        "- پایداری و کاهش قطعی\n- استانداردسازی چندسایت\n"
        "- ممیزی و Change\n- مانیتورینگ و Troubleshooting\n"
    )
    parts.append("\n## ۳) پیش‌نیاز\n\n")
    parts.append("OSI/TCP-IP، IP addressing، تفاوت Control/Data Plane، چرخه Change.\n")
    parts.append("\n## ۴) مفاهیم کلیدی\n\n")
    hints = [
        f"تعریف و مرز «{topic}»",
        "اجزای وابسته",
        "پارامترهای حساس outage",
        "Lab در برابر Production",
        "Verify و سلامت",
        "امنیت و لاگ",
        "HA و Failure Domain",
    ]
    for i in range(d["paras"]):
        parts.append(f"### {i + 1}) {hints[i % len(hints)]}\n\n")
        parts.append(f"این مفهوم را به محیط واقعی خود وصل کنید؛ blast radius را برآورد کنید.\n\n")
    parts.append("\n## ۵) مسیر کار\n\n```\nLearn → Design → Configure → Verify → Monitor → Fix → Secure → Document\n```\n")
    parts.append("\n## ۶) سناریوی کوتاه\n\n")
    parts.append(f"سازمان می‌خواهد «{topic}» را استاندارد کند؛ شما طرح، Lab و Runbook می‌دهید.\n")
    parts.append("\n## ۷) Verification\n\n1. Backup\n2. Change window\n3. show/log\n4. تست کلاینت\n5. مستند\n")
    parts.append("\n## ۸) Troubleshooting\n\n")
    for i, s in enumerate(
        ["Symptom", "Scope", "Evidence", "Hypothesis", "Fix+Verify", "Root cause doc"][: d["trouble"]], 1
    ):
        parts.append(f"{i}. {s}\n")
    if level in ("L2", "L3", "L4"):
        parts.append("\n## ۹) امنیت\n\nLeast Privilege، لاگ تغییر، جداسازی MGMT، وصله.\n")
    if level in ("L3", "L4"):
        parts.append("\n## ۱۰) Architect\n\nRTO/RPO، redundancy، NetBox، بدون SPOF.\n")

    full_content = "".join(parts)
    commands = _commands_block(topic, level, d)

    ex = [
        f"مثال {i + 1}: در Lab «{topic}» را پیاده کنید؛ خروجی show قبل/بعد را ذخیره و مقایسه کنید."
        for i in range(d["examples"])
    ]
    if level in ("L3", "L4"):
        ex.append(f"مثال سازمانی: شکست کنترل‌شده و اندازه‌گیری بازیابی برای «{topic}».")
    examples = "\n".join(ex)
    notes = (
        f"سطح {level}: روی «{topic}» تمرکز عملی. "
        "هر دستور بالا توضیح دارد؛ قبل از Production در Lab تکرار کنید."
    )

    return {
        "summary": summary,
        "full_content": full_content,
        "commands": commands,
        "examples": examples,
        "notes": notes,
        "level": level,
        "topic": topic,
        "learning_objectives": [
            f"توضیح {topic}",
            f"پیکربندی و Verify {topic}",
            f"عیب‌یابی {topic}",
            f"اجرای ایمن دستورات با درک آرگومان",
        ],
    }
