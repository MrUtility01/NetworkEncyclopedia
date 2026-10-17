#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Smoke-test Android curriculum export after professional pack merge."""
from __future__ import annotations
import gzip
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSET = ROOT / "android/app/src/main/assets/curriculum_index.json.gz"
EXPECTED = {
    57: ("بسته حرفه‌ای فصل 57", 9, 5),
    60: ("بسته حرفه‌ای فصل 60", 48, 20),
}


def main() -> int:
    if not ASSET.is_file():
        print(f"ERROR missing Android asset: {ASSET}", file=sys.stderr)
        return 1
    try:
        data = json.loads(gzip.decompress(ASSET.read_bytes()).decode("utf-8"))
    except Exception as exc:
        print(f"ERROR cannot parse Android curriculum gzip: {exc}", file=sys.stderr)
        return 1

    chapters = data.get("chapters") or []
    orders = [int(ch.get("order") or 0) for ch in chapters]
    errors = []
    if len(chapters) != 68:
        errors.append(f"expected 68 chapters, found {len(chapters)}")
    if len(orders) != len(set(orders)):
        errors.append("duplicate chapter order found")
    if set(orders) != set(range(1, 69)):
        errors.append("chapter orders are not exactly 1..68")

    all_uids = []
    for chapter_order, (section_title, expected_lessons, expected_labs) in EXPECTED.items():
        chapter = next((c for c in chapters if int(c.get("order") or 0) == chapter_order), None)
        if chapter is None:
            errors.append(f"chapter {chapter_order} is missing")
            continue
        sections = chapter.get("subchapters") or []
        section = next((s for s in sections if s.get("title_fa") == section_title), None)
        if section is None:
            errors.append(f"chapter {chapter_order} has no {section_title!r} section")
            continue
        lessons = section.get("lessons") or []
        actual_labs = [x for x in lessons if str(x.get("uid", "")).startswith(f"lesson:ch{chapter_order:02d}:lab:")]
        if len(lessons) != expected_lessons + expected_labs + 1:
            errors.append(
                f"chapter {chapter_order} expected {expected_lessons + expected_labs + 1} merged records, found {len(lessons)}"
            )
        if len(actual_labs) != expected_labs:
            errors.append(f"chapter {chapter_order} expected {expected_labs} lab lessons, found {len(actual_labs)}")
        if not any("EJ_ASSESSMENT" in str(x.get("notes", "")) for x in lessons):
            errors.append(f"chapter {chapter_order} has no embedded assessment bank")
        if not any("لابراتوار" in str(x.get("title_fa", "")) for x in lessons):
            errors.append(f"chapter {chapter_order} has no visible lab lesson")
        original_sections = [s for s in sections if s.get("title_fa") != section_title]
        if not original_sections:
            errors.append(f"chapter {chapter_order} appears to have lost its original curriculum sections")
        print(
            f"chapter {chapter_order}: original_sections={len(original_sections)} "
            f"merged_lessons={expected_lessons} labs={len(actual_labs)} assessment=embedded"
        )

    for chapter in chapters:
        for sub in chapter.get("subchapters") or []:
            for lesson in sub.get("lessons") or []:
                uid = lesson.get("uid")
                if uid:
                    all_uids.append(uid)
    duplicates = sorted({uid for uid in all_uids if all_uids.count(uid) > 1})
    if duplicates:
        errors.append(f"duplicate lesson UIDs across Android index: {', '.join(duplicates[:8])}")

    declared_count = data.get("lesson_count")
    actual_count = sum(len(sub.get("lessons") or []) for ch in chapters for sub in ch.get("subchapters") or [])
    if declared_count != actual_count:
        errors.append(f"lesson_count metadata says {declared_count}, actual count is {actual_count}")

    if errors:
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        print(f"FAILED: {len(errors)} integration issue(s)")
        return 1
    print(f"PASS Android pack integration: chapters={len(chapters)} lessons={actual_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
