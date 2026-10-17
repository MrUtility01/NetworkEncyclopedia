#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validate NetworkEncyclopedia content-pack JSON structure and assessment references."""
from __future__ import annotations

import json
import sys
from pathlib import Path


REQUIRED_ROOT = {"schema_version", "pack_id", "title_fa", "chapter_order", "language", "lessons", "labs", "assessment"}
REQUIRED_LESSON = {"uid", "chapter_order", "title_fa", "summary", "full_content", "commands", "examples", "assessment"}
REQUIRED_LAB = {"id", "title", "objective", "topology", "steps", "success_criteria", "rollback"}


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        pack = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"{path}: cannot parse JSON: {exc}"]

    missing = REQUIRED_ROOT - set(pack)
    if missing:
        errors.append(f"{path}: missing root keys: {', '.join(sorted(missing))}")
        return errors

    if not isinstance(pack["chapter_order"], int) or not 1 <= pack["chapter_order"] <= 68:
        errors.append(f"{path}: chapter_order must be an integer in 1..68")
    if not isinstance(pack["lessons"], list) or not pack["lessons"]:
        errors.append(f"{path}: lessons must be a non-empty list")
    if not isinstance(pack["labs"], list) or not pack["labs"]:
        errors.append(f"{path}: labs must be a non-empty list")

    def unique_ids(items, label):
        ids = [item.get("id") for item in items if isinstance(item, dict)]
        duplicates = sorted({value for value in ids if value and ids.count(value) > 1})
        if duplicates:
            errors.append(f"{path}: duplicate {label} IDs: {', '.join(duplicates[:10])}")
        if any(not value for value in ids):
            errors.append(f"{path}: one or more {label} records have no ID")
        return set(ids)

    lesson_uids = [x.get("uid") for x in pack.get("lessons", []) if isinstance(x, dict)]
    if len(lesson_uids) != len(set(lesson_uids)):
        errors.append(f"{path}: duplicate lesson uid")
    for i, lesson in enumerate(pack.get("lessons", []), 1):
        if not isinstance(lesson, dict):
            errors.append(f"{path}: lesson #{i} is not an object")
            continue
        absent = REQUIRED_LESSON - set(lesson)
        if absent:
            errors.append(f"{path}: lesson #{i} missing keys: {', '.join(sorted(absent))}")
        if lesson.get("chapter_order") != pack.get("chapter_order"):
            errors.append(f"{path}: lesson #{i} chapter_order does not match pack")
        assessment = lesson.get("assessment") or {}
        questions = assessment.get("questions") or []
        answer_key = assessment.get("answer_key") or []
        qids = [q.get("id") for q in questions if isinstance(q, dict)]
        aids = [a.get("id") for a in answer_key if isinstance(a, dict)]
        if len(qids) != len(set(qids)):
            errors.append(f"{path}: lesson #{i} has duplicate question IDs")
        if len(aids) != len(set(aids)):
            errors.append(f"{path}: lesson #{i} has duplicate answer_key IDs")
        if set(qids) != set(aids):
            errors.append(f"{path}: lesson #{i} question IDs and answer_key IDs differ")
        for q in questions:
            if not isinstance(q, dict) or not q.get("question"):
                errors.append(f"{path}: lesson #{i} has a question without question text")
                break

    lab_ids = unique_ids(pack.get("labs", []), "lab")
    lab_steps = []
    for i, lab in enumerate(pack.get("labs", []), 1):
        if not isinstance(lab, dict):
            errors.append(f"{path}: lab #{i} is not an object")
            continue
        absent = REQUIRED_LAB - set(lab)
        if absent:
            errors.append(f"{path}: lab #{i} missing keys: {', '.join(sorted(absent))}")
        steps = lab.get("steps")
        if not isinstance(steps, list) or len(steps) < 3:
            errors.append(f"{path}: lab #{i} must have at least 3 steps")
        if len(lab.get("success_criteria") or []) < 2:
            errors.append(f"{path}: lab #{i} must have at least 2 success criteria")
        lab_steps.append(json.dumps(steps, ensure_ascii=False, sort_keys=True))
    duplicates = sorted({s for s in lab_steps if s and lab_steps.count(s) > 1})
    if duplicates:
        errors.append(f"{path}: duplicate lab step sequences ({len(duplicates)} repeated sequence(s))")

    top = pack.get("assessment") or {}
    top_qs = top.get("questions") or []
    top_as = top.get("answer_key") or []
    qids = [q.get("id") for q in top_qs if isinstance(q, dict)]
    aids = [a.get("id") for a in top_as if isinstance(a, dict)]
    if len(qids) != len(set(qids)):
        errors.append(f"{path}: duplicate final assessment question IDs")
    if len(aids) != len(set(aids)):
        errors.append(f"{path}: duplicate final answer_key IDs")
    if set(qids) != set(aids):
        errors.append(f"{path}: final assessment question IDs and answer_key IDs differ")
    answer_ids = set(aids)
    for q in top_qs:
        if isinstance(q, dict) and q.get("answer_ref") and q["answer_ref"] not in answer_ids:
            errors.append(f"{path}: answer_ref {q['answer_ref']} has no matching answer_key entry")

    if errors:
        return errors
    print(
        f"PASS {path}: chapter={pack['chapter_order']} lessons={len(pack['lessons'])} "
        f"labs={len(pack['labs'])} final_questions={len(top_qs)}"
    )
    return []


def main(argv: list[str]) -> int:
    paths = [Path(arg) for arg in argv]
    if not paths:
        paths = sorted(Path("tools/packs").glob("ch*_professional.json"))
    if not paths:
        print("No content packs selected.")
        return 2
    errors: list[str] = []
    for path in paths:
        errors.extend(validate(path))
    for error in errors:
        print(f"ERROR {error}", file=sys.stderr)
    if errors:
        print(f"FAILED: {len(errors)} validation issue(s)")
        return 1
    print(f"All {len(paths)} content pack(s) passed structural validation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
