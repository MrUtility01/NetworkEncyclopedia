# -*- coding: utf-8 -*-
"""پرامپت‌های بسیار عمیق برای اکسپورت JSON و کمک AI."""
from __future__ import annotations
from typing import Any, Dict, List

PROVIDERS = [
    {"id": "openai", "label": "OpenAI", "base": "https://api.openai.com/v1"},
    {"id": "grok", "label": "xAI Grok", "base": "https://api.x.ai/v1"},
    {"id": "openai_compat", "label": "OpenAI-compatible (Ollama/LM Studio)", "base": "http://127.0.0.1:11434/v1"},
]

SECTIONS = [
    "concept", "architecture", "protocol_headers", "commands_multi_vendor",
    "lab_scenario", "troubleshooting_matrix", "common_errors",
    "security_hardening", "automation_hooks", "verify_rollback", "sources",
]

def deep_lesson_prompt(title: str, level: str, category: str, existing: Dict[str, Any] | None = None) -> str:
    ctx = ""
    if existing:
        ctx = f"\nزمینه موجود:\n{(existing.get('summary') or '')[:500]}\n"
    return f"""
شما مهندس شبکه ارشد هستید.
عنوان: {title} | سطح: {level} | دسته: {category}
{ctx}
خروجی STRICT JSON:
{{
  "summary": "...",
  "concept": "...",
  "architecture": "ASCII + control/data",
  "protocol_headers": "headers + Wireshark filters",
  "commands_multi_vendor": [{{"vendor": "cisco|mikrotik|fortigate|linux|windows|ansible|python", "cmd": "...", "why": "..."}}],
  "lab_scenario": {{"topology": "...", "steps": [], "failure_inject": [], "verify": []}},
  "troubleshooting_matrix": [{{"symptom": "...", "likely_cause": "...", "evidence_cmd": "...", "fix": "..."}}],
  "common_errors": [],
  "security_hardening": [],
  "automation_hooks": {{"ansible": "...", "python_netmiko": "...", "terraform_note": "..."}},
  "verify_rollback": [],
  "sources": [{{"title": "...", "url": "..."}}],
  "quiz": [{{"q": "...", "options": ["a","b","c","d"], "answer_index": 0, "explain": "..."}}],
  "depth_score": 1
}}
حداقل ۱۵ دستور واقعی. حداقل ۵ ردیف troubleshooting. depth_score از ۱ تا ۱۰۰.
""".strip()

def chapter_expansion_prompt(chapter_title: str, lesson_titles: List[str]) -> str:
    joined = "\n".join(f"- {t}" for t in lesson_titles[:80])
    return f"فصل: {chapter_title}\nدروس:\n{joined}\nبرای هر درس سطحی JSON عمیق بساز. تمرکز اتوماسیون/پایتون/اسکرپ/DB."

def export_bundle_prompt(lessons: List[Dict[str, Any]]) -> str:
    return f"بسته دروس را به عمق ۱۰۰/۱۰۰ ارتقا بده. نمونه: {lessons[:2]!r}\nSchema کامل deep_lesson را رعایت کن."
