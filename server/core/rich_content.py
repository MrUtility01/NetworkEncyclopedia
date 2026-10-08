# -*- coding: utf-8 -*-
"""تولید محتوای آموزشی غنی + خلاصه دیدگاه‌کلی برای هر درس."""
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

    # خلاصه غنی — دیدگاه کلی برای مرور سریع
    summary = (
        f"دیدگاه کلی درباره «{topic}» (سطح {level} — {level_name}): "
        f"این مبحث مشخص می‌کند موضوع چیست، در شبکه/زیرساخت سازمان کجا استفاده می‌شود، "
        f"چه پیش‌نیازی دارد، و مهندس در این سطح باید بتواند آن را توضیح دهد، "
        f"پیکربندی کند، Verify کند و در صورت خرابی عیب‌یابی نماید. "
        f"خروجی یادگیری: درک مفهوم + کاربرد عملی + مسیر استاندارد کار "
        f"(Backup → Configure → Verify → Document)."
    )

    parts: list[str] = []
    parts.append(f"# {topic}\n")
    parts.append(f"**سطح آموزشی:** {level} — {level_name}\n")
    if title_en:
        parts.append(f"**عنوان انگلیسی:** {title_en}\n")

    parts.append("\n## خلاصه اجرایی (یک نگاه)\n\n")
    parts.append(summary + "\n")

    parts.append("\n## ۱) این موضوع چیست؟\n\n")
    parts.append(
        f"«{topic}» یکی از اجزای مهم مسیر مهندس شبکه، زیرساخت و امنیت است. "
        f"در سطح {level} باید بتوانید آن را ساده توضیح دهید، جایش را در معماری ببینید، "
        f"و ارتباطش را با لایه‌های مجاور بفهمید.\n"
    )

    parts.append("\n## ۲) کاربرد عملی در سازمان\n\n")
    parts.append(
        f"- پایداری سرویس‌های وابسته به «{topic}»\n"
        f"- استانداردسازی بین سایت‌ها\n"
        f"- آمادگی ممیزی و Change Management\n"
        f"- پایه مانیتورینگ و Troubleshooting ساخت‌یافته\n"
    )

    parts.append("\n## ۳) پیش‌نیاز ذهنی\n\n")
    parts.append(
        "مدل OSI/TCP-IP، آدرس‌دهی IP، Control vs Data Plane، "
        "و چرخه Change (Backup → Apply → Verify → Document).\n"
    )

    parts.append("\n## ۴) مفاهیم کلیدی\n\n")
    concept_hints = [
        f"تعریف «{topic}» و مرز مسئولیت",
        "اجزای تشکیل‌دهنده و وابستگی‌ها",
        "پارامترهای حیاتی و ریسک outage",
        "Lab در برابر Production و rollback",
        "معیار Verify و سلامت سرویس",
        "امنیت، لاگ و Compliance",
        "HA و Failure Domain",
    ]
    for i in range(d["paras"]):
        hint = concept_hints[i % len(concept_hints)]
        parts.append(f"### {i + 1}) {hint}\n\n")
        parts.append(
            f"برای «{topic}» این مفهوم را به محیط خودتان وصل کنید. "
            f"اگر این بخش از کار بیفتد، blast radius چقدر است؟\n\n"
        )

    parts.append("\n## ۵) مسیر استاندارد\n\n")
    parts.append(
        "```\nLearn → Design → Configure → Verify → Monitor → Break/Fix → Secure → Automate → Document\n```\n"
    )

    parts.append("\n## ۶) سناریوی سازمانی\n\n")
    parts.append(
        f"سازمان چندسایته می‌خواهد «{topic}» را استاندارد کند. "
        f"شما طرح می‌نویسید، در Lab اثبات می‌کنید و Runbook می‌دهید.\n"
    )

    parts.append("\n## ۷) Verification\n\n")
    parts.append(
        "1. Backup\n2. اعمال در پنجره Change\n3. show/status/log\n"
        "4. تست end-to-end\n5. ثبت مستندات\n"
    )

    parts.append("\n## ۸) Troubleshooting\n\n")
    steps = [
        "علائم را دقیق بنویسید",
        "محدوده (Scope) را مشخص کنید",
        "شواهد: log / counter / capture",
        "فرضیه بسازید و تست کنید",
        "اصلاح و Verify",
        "علت ریشه‌ای را مستند کنید",
    ]
    for i in range(min(d["trouble"], len(steps))):
        parts.append(f"{i + 1}. {steps[i]}\n")

    if level in ("L2", "L3", "L4"):
        parts.append("\n## ۹) امنیت\n\n")
        parts.append(
            f"- Least Privilege برای «{topic}»\n"
            f"- لاگ تغییرات\n- جداسازی management\n- وصله‌های امنیتی\n"
        )

    if level in ("L3", "L4"):
        parts.append("\n## ۱۰) Architect\n\n")
        parts.append(
            "redundancy، RTO/RPO، Identity، Firewall، Monitoring و NetBox را ببینید؛ از SPOF پرهیز کنید.\n"
        )

    parts.append("\n## ۱۱) منابع\n\n")
    parts.append("مستندات رسمی Vendor + RFC.\n")

    full_content = "".join(parts)

    cmd_lines = [f"# دستورات — {topic} ({level})", "# backup قبل از تغییر", "# --- وضعیت ---"]
    for i in range(max(1, d["cmds"] // 2)):
        cmd_lines.append(f"show running-config | include {first_word}")
    cmd_lines.append("# --- Lab ---")
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
        ex.append(f"مثال HA: failover مرتبط با «{topic}».")
    examples = "\n".join(ex)

    notes = f"سطح {level}: روی «{topic}» تمرکز عملی داشته باشید."

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
