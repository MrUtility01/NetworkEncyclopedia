#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""پس از export_android_index: بسته‌های JSON تخصصی را در curriculum_index.json.gz ادغام می‌کند."""
from __future__ import annotations
import gzip, json, sys
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
GZ = ROOT / "android" / "app" / "src" / "main" / "assets" / "curriculum_index.json.gz"

def as_text(v):
    if v is None:
        return ""
    if isinstance(v, list):
        return "\n".join(str(x) for x in v)
    return str(v)

def load_json(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))

def apply_lesson_fields(les, src):
    for k in ("summary", "full_content", "commands", "examples"):
        val = src.get(k)
        if val is not None:
            les[k] = as_text(val)
    notes = as_text(src.get("notes"))
    ass = (src.get("meta") or {}).get("assessment")
    if ass and "EJ_ASSESSMENT" not in notes:
        notes += "\n\n<!-- EJ_ASSESSMENT\n" + json.dumps(ass, ensure_ascii=False) + "\n-->\n"
    if notes:
        les["notes"] = notes
    if src.get("uid"):
        les["uid"] = src["uid"]

def merge_by_title(data, pack_lessons):
    by = {}
    for src in pack_lessons:
        by[(src.get("chapter_order"), src.get("title_fa"))] = src
        by[("t", src.get("title_fa"))] = src
    n = 0
    for ch in data["chapters"]:
        for sub in ch.get("subchapters", []):
            for les in sub.get("lessons", []):
                src = by.get((ch.get("order"), les.get("title_fa"))) or by.get(("t", les.get("title_fa")))
                if src:
                    apply_lesson_fields(les, src)
                    n += 1
    return n

def ensure_ch64(data, security_pack, wireless_pack):
    data["chapters"] = [c for c in data["chapters"] if c.get("order") != 64]
    scope_titles = {s["subchapter_order"]: s["title"] for s in (security_pack.get("scope") or [])}
    subs = defaultdict(list)
    for les in security_pack.get("lessons") or []:
        subs[les["subchapter_order"]].append(les)
    for les in (wireless_pack or {}).get("lessons") or []:
        subs[les.get("subchapter_order", 8)].append(les)
    ch_subs = []
    for si in sorted(subs.keys()):
        items = sorted(subs[si], key=lambda x: (x.get("lesson_order", 0), x.get("level", "")))
        seen = set()
        out = []
        for src in items:
            uid = src.get("uid") or ""
            if uid in seen:
                continue
            seen.add(uid)
            notes = as_text(src.get("notes"))
            ass = (src.get("meta") or {}).get("assessment")
            if ass and "EJ_ASSESSMENT" not in notes:
                notes += "\n\n<!-- EJ_ASSESSMENT\n" + json.dumps(ass, ensure_ascii=False) + "\n-->\n"
            out.append({
                "uid": uid or f"lesson:ch64:s{si:03d}:l{len(out):04d}",
                "title_fa": src.get("title_fa") or "",
                "title_en": src.get("title_en") or "",
                "level": src.get("level") or "L0",
                "summary": src.get("summary") or "",
                "full_content": src.get("full_content") or "",
                "commands": as_text(src.get("commands")),
                "examples": as_text(src.get("examples")),
                "notes": notes,
            })
        title = scope_titles.get(si, f"زیرفصل {si}")
        if si == 8 and wireless_pack:
            title = title + " + امنیت بی‌سیم"
        ch_subs.append({"title_fa": title, "lessons": out})
    data["chapters"].append({
        "order": 64,
        "title_fa": "فصل ۶۴: امنیت سایبری و هک اخلاقی (دفاعی)",
        "title_en": "Chapter 64: Cybersecurity & Ethical Hacking (Defensive)",
        "subchapters": ch_subs,
    })

def main():
    if not GZ.is_file():
        print("ERROR: missing", GZ)
        sys.exit(1)
    data = json.loads(gzip.open(GZ, "rt", encoding="utf-8").read())
    auto_p = ROOT / "tools/engineer_jokar_automation_python/automation_python_curriculum_pack.json"
    sec_p = ROOT / "tools/engineer_jokar_security_ethical_hacking/security_ethical_hacking_pack.json"
    wl_p = ROOT / "tools/engineer_jokar_wireless_security/wireless_security_pack.json"
    if auto_p.is_file():
        auto = load_json(auto_p)
        n = merge_by_title(data, auto.get("lessons") or [])
        print("auto merged", n)
    sec = load_json(sec_p) if sec_p.is_file() else None
    wl = load_json(wl_p) if wl_p.is_file() else None
    if sec:
        ensure_ch64(data, sec, wl)
        print("ch64 ensured security", len(sec.get("lessons") or []), "wireless", len((wl or {}).get("lessons") or []))
    n = sum(len(l) for c in data["chapters"] for s in c["subchapters"] for l in [s["lessons"]])
    data["lesson_count"] = n
    data["version"] = max(int(data.get("version") or 1), 5)
    raw = json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    GZ.write_bytes(gzip.compress(raw, 9))
    print("FINAL chapters", len(data["chapters"]), "lessons", n, "gz", GZ.stat().st_size)
    assert len(data["chapters"]) >= 64
    assert n >= 5200

if __name__ == "__main__":
    main()
