#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit JSON source packs without modifying project data."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from collections import Counter

TEXT_KEYS = ("full_content", "content", "body", "lesson_body", "description")
ITEM_KEYS = ("lessons", "items", "records", "commands", "topics", "questions", "examples", "labs")

def records_from(data):
    if isinstance(data, list):
        return [x for x in data if isinstance(x, dict)]
    if not isinstance(data, dict):
        return []
    out = []
    for key in ITEM_KEYS:
        value = data.get(key)
        if isinstance(value, list):
            out.extend(x for x in value if isinstance(x, dict))
    curriculum = data.get("curriculum")
    if isinstance(curriculum, dict):
        for chapter in curriculum.get("chapters") or []:
            if not isinstance(chapter, dict): continue
            for collection in chapter.get("collections") or []:
                if not isinstance(collection, dict): continue
                for lesson in collection.get("lessons") or []:
                    if not isinstance(lesson, dict): continue
                    out.extend(x for x in (lesson.get("sub_lessons") or [lesson]) if isinstance(x, dict))
    return out

def text_length(row):
    for key in TEXT_KEYS:
        value = row.get(key)
        if isinstance(value, str) and value.strip(): return len(value.strip())
        if isinstance(value, (dict, list)) and value: return len(json.dumps(value, ensure_ascii=False))
    return 0

def audit(path):
    result = {"path": str(path), "valid_json": False, "records": 0, "uid_missing": 0,
              "uid_duplicates": 0, "content_missing": 0, "content_lt_800": 0,
              "content_lt_2000": 0, "assessment_records": 0, "answer_key_records": 0, "error": None}
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig")); result["valid_json"] = True
    except Exception as exc:
        result["error"] = str(exc); return result
    rows = records_from(data); result["records"] = len(rows); ids = []
    for row in rows:
        uid = row.get("uid") or row.get("id")
        if uid: ids.append(str(uid))
        else: result["uid_missing"] += 1
        n = text_length(row)
        if n == 0: result["content_missing"] += 1
        if n < 800: result["content_lt_800"] += 1
        if n < 2000: result["content_lt_2000"] += 1
        meta = row.get("meta") if isinstance(row.get("meta"), dict) else {}
        assessment = meta.get("assessment") if isinstance(meta, dict) else None
        if assessment or row.get("questions") or row.get("assessment"): result["assessment_records"] += 1
        if (isinstance(assessment, dict) and assessment.get("answer_key") is not None) or row.get("answer_key") is not None:
            result["answer_key_records"] += 1
    counts = Counter(ids); result["uid_duplicates"] = sum(n-1 for n in counts.values() if n > 1)
    return result

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--json", dest="json_path")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    files = sorted(p for p in (root / "tools").rglob("*.json") if p.is_file() and "node_modules" not in p.parts)
    results = [audit(p) for p in files]
    report = {"root": str(root), "files_checked": len(results),
              "invalid_json_files": sum(not x["valid_json"] for x in results), "files": results,
              "limitations": ["Source-pack validation does not prove SQLite import or app rendering.",
                              "Command catalogs may use schemas other than lesson records; record counts are structural."]}
    print(f"JSON files checked: {report['files_checked']} | invalid: {report['invalid_json_files']}")
    for x in results:
        if not x["valid_json"] or x["content_missing"] or x["uid_duplicates"]:
            print(f"REVIEW {x['path']}: valid={x['valid_json']} records={x['records']} missing_content={x['content_missing']} duplicate_uid={x['uid_duplicates']} error={x['error']}")
    if args.json_path:
        target = Path(args.json_path); target = target if target.is_absolute() else root / target
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print("Report written:", target)
    return 1 if report["invalid_json_files"] else 0

if __name__ == "__main__":
    raise SystemExit(main())
