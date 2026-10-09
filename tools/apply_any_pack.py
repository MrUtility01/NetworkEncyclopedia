#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""واردسازی هر content pack JSON به SQLite برنامه (ویندوز/سرور)."""
from __future__ import annotations

import argparse
import json
import shutil
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def find_packs(all_flag: bool, pack: str | None) -> list[Path]:
    if pack:
        p = Path(pack)
        if not p.is_file():
            p = ROOT / pack
        if not p.is_file():
            raise SystemExit(f"pack not found: {pack}")
        return [p]
    if all_flag:
        found = []
        for pattern in (
            "tools/**/*_pack.json",
            "tools/**/*curriculum*.json",
            "tools/**/automation_python_curriculum_pack.json",
            "tools/**/security_ethical_hacking_pack.json",
            "tools/**/wireless_security_pack.json",
        ):
            found.extend(ROOT.glob(pattern))
        # unique
        uniq = []
        seen = set()
        for f in found:
            k = str(f.resolve())
            if k not in seen and f.stat().st_size > 1000:
                seen.add(k)
                uniq.append(f)
        return sorted(uniq)
    raise SystemExit("use --pack PATH or --all")


def connect(db: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db))
    conn.row_factory = sqlite3.Row
    return conn


def match_lesson(conn: sqlite3.Connection, les: dict) -> int | None:
    title = (les.get("title_fa") or les.get("match", {}).get("title_fa") or "").strip()
    ch_order = les.get("chapter_order") or (les.get("match") or {}).get("chapter_order")
    if not title:
        return None
    if ch_order is not None:
        row = conn.execute(
            """
            SELECT l.id FROM lessons l
            JOIN levels lv ON lv.id = l.level_id
            JOIN chapters c ON c.id = lv.chapter_id
            WHERE l.title_fa = ? AND (c.order_index = ? OR c.id = ?)
            ORDER BY l.id LIMIT 1
            """,
            (title, int(ch_order), int(ch_order)),
        ).fetchone()
        if row:
            return int(row["id"])
    row = conn.execute(
        "SELECT id FROM lessons WHERE title_fa = ? ORDER BY id LIMIT 1", (title,)
    ).fetchone()
    return int(row["id"]) if row else None


def apply_pack(conn: sqlite3.Connection, path: Path, do_write: bool, overwrite: bool) -> tuple[int, int]:
    data = json.loads(path.read_text(encoding="utf-8"))
    lessons = data.get("lessons") or []
    matched = 0
    missing = 0
    now = datetime.now(timezone.utc).isoformat()
    for les in lessons:
        lid = match_lesson(conn, les)
        if lid is None:
            missing += 1
            continue
        matched += 1
        if not do_write:
            continue
        if not overwrite:
            continue
        summary = les.get("summary") or ""
        full_content = les.get("full_content") or ""
        commands = les.get("commands") or ""
        if isinstance(commands, list):
            commands = "\n".join(str(x) for x in commands)
        examples = les.get("examples") or ""
        if isinstance(examples, list):
            examples = "\n".join(str(x) for x in examples)
        notes = les.get("notes") or ""
        lo = les.get("learning_objectives") or []
        if isinstance(lo, list):
            lo_text = "\n".join(str(x) for x in lo)
        else:
            lo_text = str(lo)
        meta = les.get("meta") or {}
        meta_json = json.dumps(meta, ensure_ascii=False)
        conn.execute(
            """
            UPDATE lessons SET
              summary=?, full_content=?, commands=?, examples=?, notes=?,
              learning_objectives=?, meta_json=?, source_status=?, last_updated=?
            WHERE id=?
            """,
            (
                summary,
                full_content,
                commands,
                examples,
                notes,
                lo_text,
                meta_json,
                les.get("source_status") or "review_required",
                now,
                lid,
            ),
        )
        try:
            uid = les.get("uid") or ""
            if uid:
                conn.execute("UPDATE lessons SET uid=? WHERE id=?", (uid, lid))
        except sqlite3.OperationalError:
            pass
    if do_write:
        conn.commit()
    return matched, missing


def main() -> int:
    ap = argparse.ArgumentParser(description="Apply any ENGINEER JOKAR content pack JSON")
    ap.add_argument("--db", required=True, help="Path to encyclopedia.db")
    ap.add_argument("--pack", help="Single JSON pack path")
    ap.add_argument("--all", action="store_true", help="All packs under tools/")
    ap.add_argument("--apply", action="store_true", help="Write changes (default dry-run)")
    ap.add_argument("--overwrite", action="store_true", default=True)
    args = ap.parse_args()

    db = Path(args.db)
    if not db.is_file():
        # try relative to repo
        alt = ROOT / args.db
        if alt.is_file():
            db = alt
        else:
            print(f"ERROR: db not found: {args.db}")
            print("Hint: run server once: cd server && python app.py")
            return 1

    packs = find_packs(args.all, args.pack)
    print(f"packs: {len(packs)}")
    conn = connect(db)

    if args.apply:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        bak = db.with_suffix(db.suffix + f".bak_{ts}")
        shutil.copy2(db, bak)
        print(f"backup: {bak}")

    total_m = total_x = 0
    for p in packs:
        m, x = apply_pack(conn, p, args.apply, args.overwrite)
        print(f"  {p.relative_to(ROOT) if p.is_relative_to(ROOT) else p}: matched={m} missing={x}")
        total_m += m
        total_x += x
    print(f"TOTAL matched={total_m} missing={total_x} mode={'APPLY' if args.apply else 'DRY-RUN'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
