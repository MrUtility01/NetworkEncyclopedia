#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""واردسازی content pack استاندارد یا blueprint ENGINEER_JOKAR به SQLite."""
from __future__ import annotations
import argparse, json, shutil, sqlite3, sys, re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def blueprint_to_lessons(d, focus=None, default_ch=14):
    out, li = [], 0
    focus = focus or []
    for ch in (d.get("curriculum") or {}).get("chapters") or []:
        ch_title = ch.get("title_fa") or ""
        for ci, col in enumerate(ch.get("collections") or [], 1):
            for les in col.get("lessons") or []:
                for sub in les.get("sub_lessons") or []:
                    title = sub.get("title_fa") or les.get("title_fa") or "درس"
                    content = sub.get("content") or ""
                    status = sub.get("status") or ""
                    blob = (title + " " + content + " " + ch_title).upper()
                    if focus and not any(k.upper() in blob for k in focus):
                        continue
                    if status == "seeded" and len(content) < 350:
                        continue
                    if len(content) < 350 and status not in ("reviewed_content", "developed"):
                        continue
                    li += 1
                    target = default_ch
                    if any(k in blob for k in ("OSPF", "BGP", "REDIS")):
                        target = 14
                    if any(k in blob for k in ("IPSEC", "IKE", "VPN", "PHASE", "TUNNEL")):
                        target = 57
                    full = content
                    if sub.get("commands"):
                        full += "\n\n## دستورات\n\n" + str(sub.get("commands"))
                    out.append({
                        "title_fa": title if str(title).startswith("[L") else f"[L2] {title}",
                        "chapter_order": target,
                        "summary": (sub.get("summary") or content[:180]).strip(),
                        "full_content": full,
                        "commands": sub.get("commands") or "",
                        "examples": sub.get("examples") or "",
                        "notes": f"status={status}",
                        "learning_objectives": [f"درک {title}"],
                        "meta": {},
                        "source_status": "review_required",
                        "uid": f"lesson:ch{target:02d}:bp:{li:04d}",
                    })
    return out

def load_lessons(path: Path):
    d = json.loads(path.read_text(encoding="utf-8"))
    if d.get("lessons"):
        return d["lessons"]
    name = path.name.upper()
    if "curriculum" in d:
        if any(k in name for k in ("OSPF", "BGP", "REDIS")):
            return blueprint_to_lessons(d, ["OSPF","BGP","Redistribution","Adjacency","eBGP","iBGP","SPF"], 14)
        if "VPN" in name or "IPSEC" in name:
            return blueprint_to_lessons(d, ["IPsec","IKE","VPN","Phase","Tunnel","Site-to-Site","SSL"], 57)
        return blueprint_to_lessons(d, [], 1)
    return []

def find_packs(all_flag, pack):
    if pack:
        p = Path(pack)
        if not p.is_file():
            p = ROOT / pack
        if not p.is_file():
            raise SystemExit(f"pack not found: {pack}")
        return [p]
    if all_flag:
        found = list(ROOT.glob("tools/**/*_pack.json"))
        found += list(ROOT.glob("tools/**/*curriculum*.json"))
        found += list(ROOT.glob("tools/ENGINEER_JOKAR_*.json"))
        uniq, seen = [], set()
        for f in found:
            k = str(f.resolve())
            if k not in seen and f.stat().st_size > 500:
                seen.add(k)
                uniq.append(f)
        return sorted(uniq)
    raise SystemExit("use --pack PATH or --all")

def match_lesson(conn, les):
    title = (les.get("title_fa") or "").strip()
    bare = re.sub(r"^\[L[0-4]\]\s*", "", title)
    bare2 = re.sub(r"\s*[—\-]\s*(آشنایی|مقدماتی|ادمین|مهندس|خبره).*$", "", bare)
    ch_order = les.get("chapter_order")
    if bare2:
        row = conn.execute(
            "SELECT id FROM lessons WHERE title_fa LIKE ? ORDER BY id LIMIT 1",
            (f"%{bare2}%",),
        ).fetchone()
        if row:
            return int(row[0])
    if title:
        row = conn.execute("SELECT id FROM lessons WHERE title_fa = ? LIMIT 1", (title,)).fetchone()
        if row:
            return int(row[0])
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", required=True)
    ap.add_argument("--pack")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--overwrite", action="store_true", default=True)
    args = ap.parse_args()
    db = Path(args.db)
    if not db.is_file():
        alt = ROOT / args.db
        if alt.is_file():
            db = alt
        else:
            print("ERROR db not found", args.db)
            return 1
    packs = find_packs(args.all, args.pack)
    print("packs", len(packs))
    conn = sqlite3.connect(str(db))
    if args.apply:
        bak = db.with_suffix(db.suffix + f".bak_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        shutil.copy2(db, bak)
        print("backup", bak)
    now = datetime.now(timezone.utc).isoformat()
    total_m = total_x = 0
    for p in packs:
        lessons = load_lessons(p)
        m = x = 0
        for les in lessons:
            lid = match_lesson(conn, les)
            if lid is None:
                x += 1
                continue
            m += 1
            if not args.apply:
                continue
            conn.execute(
                """UPDATE lessons SET summary=?, full_content=?, commands=?, examples=?, notes=?,
                   learning_objectives=?, last_updated=? WHERE id=?""",
                (
                    les.get("summary") or "",
                    les.get("full_content") or "",
                    as_text(les.get("commands")),
                    as_text(les.get("examples")),
                    as_text(les.get("notes")),
                    "\n".join(les.get("learning_objectives") or []),
                    now,
                    lid,
                ),
            )
        print(f"  {p.name}: matched={m} missing={x}")
        total_m += m
        total_x += x
    if args.apply:
        conn.commit()
    print(f"TOTAL matched={total_m} missing={total_x} mode={'APPLY' if args.apply else 'DRY-RUN'}")
    return 0

def as_text(v):
    if v is None:
        return ""
    if isinstance(v, list):
        return "\n".join(str(x) for x in v)
    return str(v)

if __name__ == "__main__":
    sys.exit(main())
