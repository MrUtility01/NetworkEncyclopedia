#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
import gzip, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "server"))
from core.full_curriculum import get_full_curriculum
from core.rich_content import build_rich_lesson

def main() -> None:
    chapters = []
    lesson_count = 0
    for ch in get_full_curriculum():
        order, tfa, ten, subs = ch[0], ch[1], ch[2], ch[3]
        sub_out = []
        for si, sub in enumerate(subs):
            sname, lessons = sub[0], sub[1]
            les_out = []
            for li, les in enumerate(lessons):
                if isinstance(les, (list, tuple)) and len(les) >= 2:
                    lfa, len_ = les[0], les[1]
                else:
                    lfa, len_ = str(les), str(les)
                tag = lfa[1:3] if lfa.startswith("[L") else "L0"
                rich = build_rich_lesson(lfa, len_, level=tag)
                lesson_count += 1
                uid = f"lesson:ch{int(order):02d}:s{si:03d}:l{li:04d}"
                les_out.append({
                    "uid": uid, "title_fa": lfa, "title_en": len_, "level": tag,
                    "summary": rich["summary"], "full_content": rich["full_content"],
                    "commands": rich["commands"], "examples": rich["examples"], "notes": rich["notes"],
                })
            sub_out.append({"title_fa": sname, "lessons": les_out})
        chapters.append({"order": int(order), "title_fa": tfa, "title_en": ten, "subchapters": sub_out})
    payload = {"version": 2, "chapters": chapters, "lesson_count": lesson_count}
    raw = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    out_dir = ROOT / "android" / "app" / "src" / "main" / "assets"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "curriculum_index.json.gz"
    out.write_bytes(gzip.compress(raw, 9))
    print(f"wrote {out} lessons={lesson_count} raw={len(raw)} gz={out.stat().st_size}")

if __name__ == "__main__":
    main()
