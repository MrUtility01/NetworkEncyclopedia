# -*- coding: utf-8 -*-
"""اعمال محتوای NetMaster روی درس‌های فصل هم‌موضوع — بر اساس id مرتب، نه match عنوان."""
from __future__ import annotations
import json
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DB = ROOT / "server" / "data" / "encyclopedia.db"
PACK = ROOT / "tools" / "packs" / "ordered_fill" / "netmaster_levels_2_3_4_5.json"

# NetMaster level id در پک از title_en مثل L02-01 → level 2
# chapter_order در پک فعلی اشتباه بود؛ اینجا صریح نگاشت می‌کنیم
NM_LEVEL_TO_NE_CHAPTER = {
    2: 6,  # مبانی شبکه
    3: 7,  # اترنت
    4: 8,  # IP
    5: 9,  # ARP ICMP
}

def nm_level(title_en: str) -> int:
    m = re.match(r"L0*(\d+)", title_en or "")
    return int(m.group(1)) if m else 0

def base_title(t: str) -> str:
    t = re.sub(r"^\[L[0-4]\]\s*", "", t or "")
    t = re.sub(r"\s*[—\-]\s*(آشنایی|مقدماتی|ادمین|مهندس|خبره).*$", "", t)
    return re.sub(r"\s+", " ", t).strip()

def main():
    if not DB.is_file():
        raise SystemExit(f"DB not found: {DB}")
    pack = json.loads(PACK.read_text(encoding="utf-8"))
    by_nm_level: dict[int, list] = {}
    for les in pack["lessons"]:
        lv = nm_level(les.get("title_en") or "")
        by_nm_level.setdefault(lv, []).append(les)

    conn = sqlite3.connect(str(DB))
    conn.row_factory = sqlite3.Row
    now = datetime.now(timezone.utc).isoformat()
    total = 0

    for nm_lv, ne_ch in NM_LEVEL_TO_NE_CHAPTER.items():
        src = by_nm_level.get(nm_lv) or []
        if not src:
            print(f"skip NM L{nm_lv}: no source")
            continue

        rows = conn.execute(
            """
            SELECT l.id, l.title_fa
            FROM lessons l
            JOIN levels lv ON l.level_id = lv.id
            JOIN chapters c ON lv.chapter_id = c.id
            WHERE c.order_index = ?
            ORDER BY l.id
            """,
            (ne_ch,),
        ).fetchall()

        # گروه بر اساس عنوان پایه (L0..L4 یک موضوع)
        groups: dict[str, list] = {}
        order = []
        for r in rows:
            b = base_title(r["title_fa"])
            if b not in groups:
                groups[b] = []
                order.append(b)
            groups[b].append(int(r["id"]))

        # به هر گروه موضوعی یک درس NetMaster (چرخشی اگر کمتر/بیشتر)
        n = 0
        for i, b in enumerate(order):
            src_les = src[i % len(src)]
            full = src_les["full_content"]
            summary = (src_les.get("summary") or "")[:300]
            commands = src_les.get("commands") or ""
            examples = src_les.get("examples") or ""
            notes = src_les.get("notes") or ""
            lo = src_les.get("learning_objectives") or ""
            if isinstance(lo, list):
                lo = "\n".join(str(x) for x in lo)
            for lid in groups[b]:
                conn.execute(
                    """
                    UPDATE lessons SET
                      summary=?, full_content=?, commands=?, examples=?, notes=?,
                      learning_objectives=?, last_updated=?
                    WHERE id=?
                    """,
                    (summary, full, commands, examples, notes, lo, now, lid),
                )
                n += 1
        conn.commit()
        total += n
        print(f"NE ch{ne_ch} <- NM L{nm_lv}: topics={len(order)} lessons_updated={n} src={len(src)}")

    conn.close()
    print("TOTAL updated", total)

if __name__ == "__main__":
    main()
