#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ادغام بسته‌های tools؛ فصل ۶۴=Git حفظ می‌شود؛ امنیت+وایرلس → فصل ۶۵."""
from __future__ import annotations
import gzip, json, sys
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
GZ = ROOT / "android/app/src/main/assets/curriculum_index.json.gz"

def as_text(v):
    if v is None:
        return ""
    if isinstance(v, list):
        return "\n".join(str(x) for x in v)
    return str(v)

def load_json(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))

def find_pack_files():
    files = list(ROOT.glob("tools/**/*_pack.json")) + list(ROOT.glob("tools/**/*curriculum*.json"))
    uniq, seen = [], set()
    for f in files:
        k = str(f.resolve())
        if k not in seen and f.stat().st_size > 500:
            seen.add(k)
            uniq.append(f)
    return sorted(uniq)

def apply_fields(les, src):
    for k in ("summary", "full_content", "commands", "examples", "notes"):
        if src.get(k) is not None:
            les[k] = as_text(src.get(k))
    notes = les.get("notes") or ""
    ass = (src.get("meta") or {}).get("assessment")
    if ass and "EJ_ASSESSMENT" not in notes:
        notes += "\n\n<!-- EJ_ASSESSMENT\n" + json.dumps(ass, ensure_ascii=False) + "\n-->\n"
        les["notes"] = notes
    if src.get("uid"):
        les["uid"] = src["uid"]

def merge_by_title(data, lessons):
    by = {}
    for src in lessons:
        title = src.get("title_fa") or ""
        by[(src.get("chapter_order"), title)] = src
        by[("t", title)] = src
    n = 0
    for ch in data["chapters"]:
        for sub in ch.get("subchapters", []):
            for les in sub.get("lessons", []):
                src = by.get((ch.get("order"), les.get("title_fa"))) or by.get(("t", les.get("title_fa")))
                if src:
                    apply_fields(les, src)
                    n += 1
    return n

def build_ch65(lessons):
    subs = defaultdict(list)
    for les in lessons:
        subs[les.get("subchapter_order") or 1].append(les)
    out = []
    for si in sorted(subs):
        items = sorted(subs[si], key=lambda x: (x.get("lesson_order") or 0, x.get("level") or ""))
        seen, les_out = set(), []
        for src in items:
            uid = src.get("uid") or f"lesson:ch65:s{int(si):03d}:l{len(les_out):04d}"
            if uid in seen:
                continue
            seen.add(uid)
            notes = as_text(src.get("notes"))
            ass = (src.get("meta") or {}).get("assessment")
            if ass and "EJ_ASSESSMENT" not in notes:
                notes += "\n\n<!-- EJ_ASSESSMENT\n" + json.dumps(ass, ensure_ascii=False) + "\n-->\n"
            les_out.append({
                "uid": uid,
                "title_fa": src.get("title_fa") or "",
                "title_en": src.get("title_en") or "",
                "level": src.get("level") or "L0",
                "summary": src.get("summary") or "",
                "full_content": src.get("full_content") or "",
                "commands": as_text(src.get("commands")),
                "examples": as_text(src.get("examples")),
                "notes": notes,
            })
        out.append({"title_fa": f"زیرفصل {si}", "lessons": les_out})
    return {
        "order": 65,
        "title_fa": "فصل ۶۵: امنیت سایبری و هک اخلاقی (دفاعی) + بی‌سیم",
        "title_en": "Ch65 Security Ethical Hacking Wireless",
        "subchapters": out,
    }

def main():
    if not GZ.is_file():
        print("ERROR missing", GZ)
        sys.exit(1)
    data = json.loads(gzip.open(GZ, "rt", encoding="utf-8").read())
    packs = find_pack_files()
    print("packs", len(packs))
    sec, wireless = [], []
    for p in packs:
        d = load_json(p)
        lessons = d.get("lessons") or []
        name = str(p).replace("\\", "/").lower()
        print(" ", p.name, len(lessons))
        if "security_ethical" in name:
            sec.extend(lessons)
            continue
        if "wireless" in name:
            wireless.extend(lessons)
            continue
        print("   merge", merge_by_title(data, lessons))
    # keep chapter 64 Git; put security on 65
    data["chapters"] = [c for c in data["chapters"] if c.get("order") != 65]
    extra = list(sec)
    for w in wireless:
        w = dict(w)
        w["subchapter_order"] = 100 + int(w.get("subchapter_order") or 8)
        extra.append(w)
    if extra:
        data["chapters"].append(build_ch65(extra))
        print("ch65", sum(len(s["lessons"]) for s in data["chapters"][-1]["subchapters"]))
    data["chapters"].sort(key=lambda c: int(c.get("order") or 0))
    n = sum(len(s.get("lessons", [])) for c in data["chapters"] for s in c.get("subchapters", []))
    data["lesson_count"] = n
    data["version"] = 6
    GZ.write_bytes(gzip.compress(json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8"), 9))
    print("FINAL chapters", len(data["chapters"]), "lessons", n)
    for c in data["chapters"][-3:]:
        print(" ", c["order"], c["title_fa"][:48], sum(len(s["lessons"]) for s in c["subchapters"]))

if __name__ == "__main__":
    main()
