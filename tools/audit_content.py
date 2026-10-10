#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ممیزی ساختار و عمق محتوا — فهرست / بانک / آزمون / سناریو / Lab.

Usage:
  python tools/audit_content.py --db server/data/encyclopedia.db
  python tools/audit_content.py --db server/data/encyclopedia.db --json report.json
  python tools/audit_content.py --curriculum-only
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIN_FULL = 800
MIN_COMMANDS = 20
LAB_MARKERS = ("لاب", "lab", "آزمایشگاه", "مراحل اجرا", "verify")
ASSESS_MARKERS = ("assessment", "questions", "answer_key")


def load_curriculum_skeleton():
    sys.path.insert(0, str(ROOT / "server"))
    from core.full_curriculum import get_full_curriculum
    C = get_full_curriculum()
    out = []
    for order, title_fa, title_en, levels in C:
        n_les = sum(len(lessons) for _, lessons in levels)
        out.append({"order": order, "title_fa": title_fa, "levels": len(levels), "lessons": n_les})
    return out


def audit_db(db_path: Path) -> dict:
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    chapters = cur.execute(
        "SELECT id, order_index, title_fa FROM chapters ORDER BY order_index"
    ).fetchall()
    stats = {
        "chapters": len(chapters),
        "levels": cur.execute("SELECT COUNT(*) c FROM levels").fetchone()["c"],
        "lessons": cur.execute("SELECT COUNT(*) c FROM lessons").fetchone()["c"],
        "scenarios": cur.execute("SELECT COUNT(*) c FROM scenarios").fetchone()["c"],
    }

    by_ch = []
    shallow = []
    no_lab_hint = 0
    no_assess = 0

    for ch in chapters:
        rows = cur.execute(
            """
            SELECT l.title_fa, l.summary, l.full_content, l.commands, l.notes, l.meta_json
            FROM lessons l
            JOIN levels lv ON lv.id = l.level_id
            WHERE lv.chapter_id = ?
            ORDER BY lv.order_index, l.order_index
            """,
            (ch["id"],),
        ).fetchall()
        deep = mid = thin = 0
        for r in rows:
            fc = r["full_content"] or ""
            cmd = r["commands"] or ""
            meta = r["meta_json"] or ""
            blob = (fc + "\n" + (r["notes"] or "") + "\n" + meta).lower()
            n = len(fc)
            if n >= 2000:
                deep += 1
            elif n >= MIN_FULL:
                mid += 1
            else:
                thin += 1
                if n < 400:
                    shallow.append({"chapter": ch["order_index"], "title": (r["title_fa"] or "")[:80], "full_len": n})
            if not any(m in blob for m in LAB_MARKERS):
                no_lab_hint += 1
            if not any(m in blob for m in ASSESS_MARKERS) and "questions" not in meta:
                no_assess += 1

        by_ch.append({
            "order": ch["order_index"],
            "title_fa": ch["title_fa"],
            "lessons": len(rows),
            "deep_ge_2000": deep,
            "mid_ge_800": mid,
            "thin_lt_800": thin,
            "depth_score": round(100.0 * (deep + mid * 0.5) / max(len(rows), 1), 1),
        })

    sc_rows = cur.execute(
        "SELECT code, title_fa, length(COALESCE(tasks,'')) t, length(COALESCE(solution,'')) s, length(COALESCE(verification,'')) v FROM scenarios"
    ).fetchall()
    sc_thin = [dict(r) for r in sc_rows if (r["t"] or 0) < 80 or (r["s"] or 0) < 40]

    by_ch_sorted = sorted(by_ch, key=lambda x: x["depth_score"])
    report = {
        "db": str(db_path),
        "stats": stats,
        "chapter_depth": by_ch,
        "weakest_chapters": by_ch_sorted[:15],
        "strongest_chapters": list(reversed(by_ch_sorted[-10:])),
        "shallow_lessons_sample": shallow[:40],
        "shallow_count": len(shallow),
        "lessons_missing_lab_hint_approx": no_lab_hint,
        "lessons_missing_assessment_approx": no_assess,
        "scenarios_total": len(sc_rows),
        "scenarios_thin": sc_thin[:20],
        "definition": {
            "deep": "full_content >= 2000 chars",
            "mid": "800-1999",
            "thin": "< 800",
            "note": "آزمون اندروید از بانک درس می‌سازد مگر assessment در meta باشد",
        },
    }
    conn.close()
    return report


def print_report(r: dict) -> None:
    print("=== CONTENT AUDIT ===")
    if "stats" in r:
        print("DB stats:", json.dumps(r["stats"], ensure_ascii=False))
        print("shallow lessons:", r.get("shallow_count"))
        print("scenarios:", r.get("scenarios_total"), "thin:", len(r.get("scenarios_thin") or []))
        print("\n--- weakest chapters ---")
        for c in r.get("weakest_chapters") or []:
            print(f"  ch{c['order']:02d} score={c['depth_score']:5.1f}  lessons={c['lessons']:4d}  thin={c['thin_lt_800']:4d}  {c['title_fa'][:50]}")
        print("\n--- strongest ---")
        for c in r.get("strongest_chapters") or []:
            print(f"  ch{c['order']:02d} score={c['depth_score']:5.1f}  deep={c['deep_ge_2000']} mid={c['mid_ge_800']}  {c['title_fa'][:50]}")
    if "curriculum" in r:
        print("Curriculum chapters:", len(r["curriculum"]))
        print("Total lesson slots:", sum(c["lessons"] for c in r["curriculum"]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", help="path to encyclopedia.db")
    ap.add_argument("--json", help="write full report JSON")
    ap.add_argument("--curriculum-only", action="store_true")
    args = ap.parse_args()

    report = {}
    if args.curriculum_only or not args.db:
        try:
            report["curriculum"] = load_curriculum_skeleton()
        except Exception as e:
            report["curriculum_error"] = str(e)

    if args.db:
        p = Path(args.db)
        if not p.is_file():
            p = ROOT / args.db
        if not p.is_file():
            print("DB not found:", args.db)
            return 1
        report.update(audit_db(p))

    print_report(report)
    if args.json:
        Path(args.json).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print("wrote", args.json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
