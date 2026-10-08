# -*- coding: utf-8 -*-
"""تولید محتوای آموزشی غنی برای هر درس — ویندوز و اندروید."""
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
    "L0": dict(paras=3, cmds=3, examples=2, trouble=2),
    "L1": dict(paras=4, cmds=4, examples=2, trouble=3),
    "L2": dict(paras=5, cmds=6, examples=3, trouble=4),
    "L3": dict(paras=6, cmds=8, examples=3, trouble=5),
    "L4": dict(paras=7, cmds=10, examples=4, trouble=6),
}

_LEVEL_FA = {
    "L0": "آشنایی / مقدماتی",
    "L1": "کاربر فنی / Junior",
    "L2": "Administrator",
    "L3": "Engineer / Senior",
    "L4": "Architect / Enterprise",
}


def build_rich_lesson(title_fa: str, title_en: str = "", level: str | None = None) -> Dict[str, Any]:
    level = level or level_tag(title_fa)
    topic = clean_topic(title_fa)
    d = _DEPTH.get(level, _DEPTH["L2"])
    level_name = _LEVEL_FA.get(level, level)
    first_word = (topic.split() or ["topic"])[0]

    summary = (
        f"{topic} در سطح {level} ({level_name}): "
        f"از درک مفهوم تا پیکربندی، Verify، عیب‌یابی و مستندسازی در محیط واقعی."
    )

    parts: list[str] = []
    parts.append(f"# {topic}\n")
    parts.append(f"**سطح آموزشی:** {level} — {level_name}\n")
    if title_en:
        parts.append(f"**عنوان انگلیسی:** {title_en}\n")

    parts.append("\n## ۱) این موضوع چیست؟\n\n")
    parts.append(
        f"«{topic}» یکی از اجزای مهم در مسیر مهندس شبکه، زیرساخت و امنیت است. "
        f"در سطح {level} انتظار می‌رود بتوانید آن را به‌زبان ساده توضیح دهید، "
        f"جایگاهش را در معماری سازمان مشخص کنید، و ارتباطش را با لایه‌های مجاور بفهمید.\n"
    )

    parts.append("\n## ۲) کاربرد عملی در سازمان\n\n")
    parts.append(
        f"- کاهش قطعی و افزایش پایداری سرویس‌های وابسته به «{topic}»\n"
        f"- استانداردسازی پیکربندی بین سایت‌ها و تیم‌ها\n"
        f"- آمادگی برای ممیزی امنیتی و مستندسازی Change\n"
        f"- پایه برای اتوماسیون، مانیتورینگ و Troubleshooting ساخت‌یافته\n"
    )

    parts.append("\n## ۳) پیش‌نیاز ذهنی\n\n")
    parts.append(
        "قبل از عمیق شدن: مدل OSI/TCP-IP، آدرس‌دهی IP، "
        "تفاوت Control Plane و Data Plane، و چرخه Change "
        "(Backup → Apply → Verify → Document).\n"
    )

    parts.append("\n## ۴) مفاهیم کلیدی\n\n")
    concept_hints = [
        f"تعریف دقیق «{topic}» و مرز مسئولیت آن",
        "اجزای تشکیل‌دهنده و وابستگی به سرویس‌های مجاور",
        "پارامترهای حیاتی که اشتباه تنظیم‌شدنشان باعث outage می‌شود",
        "تفاوت Lab با Production و نکات rollback",
        "معیارهای Verify و علائم سلامت سرویس",
        "تأثیر روی امنیت، لاگ و Compliance",
        "گزینه‌های طراحی High Availability و Failure Domain",
    ]
    for i in range(d["paras"]):
        hint = concept_hints[i % len(concept_hints)]
        parts.append(f"### {i + 1}) {hint}\n\n")
        parts.append(
            f"در عمل برای «{topic}»، این مفهوم را با یک مثال از محیط خودتان پیوند بزنید. "
            f"اگر این بخش از کار بیفتد، blast radius چقدر است؟\n\n"
        )

    parts.append("\n## ۵) مسیر استاندارد کار\n\n")
    parts.append(
        "```\nLearn → Design → Configure → Verify → Monitor → Break/Fix → Secure → Automate → Document\n```\n"
    )

    parts.append("\n## ۶) سناریوی سازمانی\n\n")
    parts.append(
        f"سازمانی با چند سایت می‌خواهد «{topic}» را استاندارد کند. "
        f"شما طرح می‌نویسید، در Lab اثبات می‌کنید، و Runbook تحویل می‌دهید.\n"
    )

    parts.append("\n## ۷) Verification\n\n")
    parts.append(
        "1. Backup قبل از تغییر\n2. اعمال در پنجره Change\n"
        "3. show/status/log\n4. تست end-to-end\n5. ثبت مستندات\n"
    )

    parts.append("\n## ۸) Troubleshooting\n\n")
    steps = [
        "علائم (Symptom) را دقیق بنویسید",
        "محدوده (Scope) را مشخص کنید",
        "شواهد: log، counter، capture",
        "فرضیه بسازید و تست کنید",
        "اصلاح و Verify",
        "علت ریشه‌ای را مستند کنید",
    ]
    for i in range(min(d["trouble"], len(steps))):
        parts.append(f"{i + 1}. {steps[i]}\n")

    if level in ("L2", "L3", "L4"):
        parts.append("\n## ۹) امنیت و Hardening\n\n")
        parts.append(
            f"- Least Privilege برای مدیریت «{topic}»\n"
            f"- لاگ تغییرات حساس\n"
            f"- جداسازی management در صورت امکان\n"
            f"- بررسی وصله‌های امنیتی\n"
        )

    if level in ("L3", "L4"):
        parts.append("\n## ۱۰) نگاه Architect\n\n")
        parts.append(
            "redundancy، RTO/RPO، ظرفیت، Identity، Firewall، Monitoring و NetBox "
            f"را برای «{topic}» ببینید. از SPOF پرهیز کنید.\n"
        )

    parts.append("\n## ۱۱) منابع\n\n")
    parts.append("مستندات رسمی Vendor + RFC. Community فقط راهنمای ثانویه.\n")

    full_content = "".join(parts)

    cmd_lines = [
        f"# دستورات — {topic} ({level})",
        "# backup قبل از تغییر",
        "# --- وضعیت ---",
    ]
    for i in range(max(1, d["cmds"] // 2)):
        cmd_lines.append(f"show running-config | include {first_word}")
    cmd_lines.append("# --- Lab config ---")
    for i in range(max(1, d["cmds"] - d["cmds"] // 2)):
        cmd_lines.append("configure terminal")
        cmd_lines.append(f"! step {i + 1}: {topic}")
        cmd_lines.append("end")
        cmd_lines.append("write memory")
    cmd_lines.append("show logging | last 50")
    commands = "\n".join(cmd_lines)

    ex = [
        f"مثال {i + 1}: در Lab «{topic}» را پیاده و با Baseline مقایسه کنید."
        for i in range(d["examples"])
    ]
    if level in ("L3", "L4"):
        ex.append(f"مثال HA: failover مرتبط با «{topic}» و اندازه‌گیری زمان بازیابی.")
    examples = "\n".join(ex)

    notes = f"سطح {level}: تمرکز عملی روی «{topic}». Production فقط با Change و Rollback."

    return {
        "summary": summary,
        "full_content": full_content,
        "commands": commands,
        "examples": examples,
        "notes": notes,
        "level": level,
        "topic": topic,
        "learning_objectives": [
            f"توضیح مفهومی {topic}",
            f"پیکربندی و Verify {topic}",
            f"عیب‌یابی {topic}",
            f"امنیت و مستندسازی {topic}",
        ],
    }
