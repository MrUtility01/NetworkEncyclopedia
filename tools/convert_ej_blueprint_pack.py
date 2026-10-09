#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""تبدیل JSON اسکمای blueprint (curriculum.chapters) به content pack استاندارد."""
from __future__ import annotations
import argparse, json
from pathlib import Path

def convert(path: Path, focus, default_ch: int, purpose: str):
    d = json.loads(path.read_text(encoding="utf-8"))
    lessons, li = [], 0
    for ch in (d.get("curriculum") or {}).get("chapters") or []:
        ch_title = ch.get("title_fa") or ""
        for ci, col in enumerate(ch.get("collections") or [], 1):
            for les in col.get("lessons") or []:
                for sub in les.get("sub_lessons") or []:
                    title = sub.get("title_fa") or les.get("title_fa") or "درس"
                    content = sub.get("content") or ""
                    status = sub.get("status") or ""
                    blob = (title + " " + content + " " + ch_title).upper()
                    if not any(k.upper() in blob for k in focus):
                        continue
                    if status == "seeded" and len(content) < 350:
                        continue
                    if len(content) < 350 and status not in ("reviewed_content", "developed"):
                        continue
                    li += 1
                    target = default_ch
                    if any(k in blob for k in ("OSPF", "BGP", "REDIS", "EIGRP", "ROUTE-MAP")):
                        target = 14
                    if any(k in blob for k in ("IPSEC", "IKE", "SSL VPN", "PHASE", "TUNNEL", "VPN")):
                        target = 57
                        if "MIKROTIK" in blob or "میکروتیک" in (title + ch_title):
                            target = 21
                    full = content
                    if sub.get("commands"):
                        full += "\n\n## دستورات\n\n" + str(sub.get("commands"))
                    if sub.get("examples"):
                        full += "\n\n## مثال‌ها\n\n" + str(sub.get("examples"))
                    lessons.append({
                        "uid": f"lesson:ch{target:02d}:pack:{li:04d}",
                        "chapter_order": target,
                        "subchapter_order": ci,
                        "lesson_order": li,
                        "level": "L2",
                        "title_fa": title if str(title).startswith("[L") else f"[L2] {title}",
                        "title_en": sub.get("title_en") or title,
                        "topic": title,
                        "summary": (sub.get("summary") or content[:180]).strip(),
                        "full_content": full,
                        "commands": sub.get("commands") or "",
                        "examples": sub.get("examples") or "",
                        "notes": f"source={path.name}; status={status}",
                        "learning_objectives": [f"درک {title}", "Lab کنترل‌شده", "RCA با شواهد"],
                        "meta": {"assessment": {"questions": [], "answer_key": []}},
                        "source_status": "review_required",
                    })
    return {
        "package_schema_version": 1,
        "project": "ENGINEER JOKAR / NetworkEncyclopedia",
        "purpose": purpose,
        "source_file": path.name,
        "lessons": lessons,
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("-o", "--output", required=True)
    ap.add_argument("--focus", nargs="+", required=True)
    ap.add_argument("--chapter", type=int, default=14)
    ap.add_argument("--purpose", default="converted")
    a = ap.parse_args()
    out = convert(Path(a.input), a.focus, a.chapter, a.purpose)
    Path(a.output).parent.mkdir(parents=True, exist_ok=True)
    Path(a.output).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print("wrote", a.output, "lessons", len(out["lessons"]))

if __name__ == "__main__":
    main()
