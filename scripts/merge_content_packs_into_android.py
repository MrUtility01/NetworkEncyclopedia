#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ادغام بسته‌های tools؛ فصل ۶۴=Git؛ امنیت→۶۵؛ OSPF/VPN→۶۶/۶۷؛ دستورات→۶۸."""
from __future__ import annotations
import gzip, json, sys, re
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
    files += list(ROOT.glob("tools/ENGINEER_JOKAR_*.json"))
    files += list(ROOT.glob("tools/packs/**/*.json"))
    uniq, seen = [], set()
    for f in files:
        if f.name.lower() in ("readme.md", "readme_fa.md"):
            continue
        k = str(f.resolve())
        if k not in seen and f.stat().st_size > 500:
            seen.add(k)
            uniq.append(f)
    return sorted(uniq)


def commands_to_lessons(data: dict) -> list:
    ch = int(data.get("chapter_order") or 68)
    out = []
    sub_map = {
        "basics": 1, "interface": 2, "vlan": 3, "trunk": 3, "stp": 4, "spanning-tree": 4,
        "etherchannel": 5, "port-security": 6, "mac": 7, "cdp": 8, "lldp": 8,
        "troubleshoot": 9, "switching": 2, "general": 10,
    }
    for i, c in enumerate(data.get("commands") or [], 1):
        if not isinstance(c, dict):
            continue
        cmd = c.get("command") or c.get("title_en") or ""
        level = c.get("level") or "L1"
        title_fa = c.get("title_fa") or cmd
        if not str(title_fa).startswith("[L"):
            title_fa = f"[{level}] {title_fa}"
        sub = (c.get("subcategory") or c.get("category") or "general").strip().lower()
        sub_order = sub_map.get(sub, 10)
        args = c.get("arguments") or []
        arg_lines = []
        for a in args:
            if isinstance(a, dict):
                arg_lines.append(
                    f"- `{a.get('name', '')}`: {a.get('meaning_fa', '')} — مثال: `{a.get('example', '')}`"
                )
            else:
                arg_lines.append(f"- {a}")
        steps = c.get("steps_fa") or []
        if isinstance(steps, list):
            steps_txt = "\n".join(f"{idx}. {s}" for idx, s in enumerate(steps, 1))
        else:
            steps_txt = str(steps)
        out_fields = c.get("output_fields_fa") or []
        of_txt = "\n".join(
            f"- **{x.get('field', '')}**: {x.get('meaning', '')}" if isinstance(x, dict) else f"- {x}"
            for x in out_fields
        )
        related = c.get("related_commands") or []
        rel_txt = ", ".join(f"`{x}`" for x in related) if isinstance(related, list) else str(related)
        mistakes = c.get("common_mistakes_fa") or []
        mist_txt = "\n".join(f"- {m}" for m in mistakes) if isinstance(mistakes, list) else str(mistakes)
        kw = c.get("search_keywords") or []
        kw_txt = ", ".join(kw) if isinstance(kw, list) else str(kw)
        aliases = c.get("aliases") or []
        alias_txt = ", ".join(aliases) if isinstance(aliases, list) else str(aliases)
        prereq = c.get("prerequisites_fa") or []
        prereq_txt = "\n".join(f"- {x}" for x in prereq) if isinstance(prereq, list) else str(prereq)

        full = (
            f"# {c.get('title_fa') or cmd}\n\n"
            f"## دستور\n```text\n{cmd}\n```\n"
            f"**Aliases:** {alias_txt}\n\n**Syntax:** `{c.get('syntax') or cmd}`\n\n"
            f"## چه زمانی\n{c.get('when_to_use_fa') or ''}\n\n"
            f"## پیش‌نیاز\n{prereq_txt or '- —'}\n\n"
            f"## آرگومان‌ها\n{chr(10).join(arg_lines) if arg_lines else '- —'}\n\n"
            f"## مراحل\n{steps_txt or '- —'}\n\n"
            f"## نمونه خروجی\n```text\n{c.get('sample_output') or ''}\n```\n\n"
            f"## فیلدهای خروجی\n{of_txt or '- —'}\n\n"
            f"## دستورات مرتبط\n{rel_txt or '—'}\n\n"
            f"## اشتباهات رایج\n{mist_txt or '- —'}\n\n"
            f"## Lab\n{c.get('lab_hint_fa') or ''}\n\n"
            f"## امنیت\n{c.get('security_notes_fa') or ''}\n\n"
            f"## کلیدواژه جستجو\n{kw_txt}\n"
        )
        notes = ""
        flash = c.get("flashcards")
        assess = c.get("assessment")
        meta = {}
        if assess:
            meta["assessment"] = assess
            notes += "\n\n<!-- EJ_ASSESSMENT\n" + json.dumps(assess, ensure_ascii=False) + "\n-->\n"
        if flash:
            meta["flashcards"] = flash
            notes += "\n\n<!-- EJ_FLASHCARDS\n" + json.dumps(flash, ensure_ascii=False) + "\n-->\n"

        lesson_uid = f"lesson:ch{ch:02d}:cmd:{i:04d}"
        out.append({
            "uid": lesson_uid,
            "chapter_order": ch,
            "subchapter_order": sub_order,
            "lesson_order": i,
            "level": level,
            "title_fa": title_fa,
            "title_en": c.get("title_en") or cmd,
            "summary": (c.get("when_to_use_fa") or title_fa)[:220],
            "full_content": full,
            "commands": cmd + (("\n" + alias_txt) if alias_txt else ""),
            "examples": c.get("sample_output") or "",
            "notes": notes.strip(),
            "meta": meta,
            "source_status": "review_required",
        })
    return out


def blueprint_to_lessons(d, focus_keywords, default_ch):
    out, li = [], 0
    for ch in (d.get("curriculum") or {}).get("chapters") or []:
        ch_title = ch.get("title_fa") or ""
        for ci, col in enumerate(ch.get("collections") or [], 1):
            for les in col.get("lessons") or []:
                for sub in les.get("sub_lessons") or []:
                    title = sub.get("title_fa") or les.get("title_fa") or "درس"
                    content = sub.get("content") or ""
                    status = sub.get("status") or ""
                    blob = (title + " " + content + " " + ch_title).upper()
                    if focus_keywords and not any(k.upper() in blob for k in focus_keywords):
                        continue
                    if status == "seeded" and len(content) < 350:
                        continue
                    if len(content) < 350 and status not in ("reviewed_content", "developed"):
                        continue
                    li += 1
                    target = default_ch
                    if any(k in blob for k in ("OSPF", "BGP", "REDIS", "EIGRP", "ROUTE-MAP")):
                        target = 14
                    if any(k in blob for k in ("IPSEC", "IKE", "SSL VPN", "PHASE", "TUNNEL", "VPN")):
                        target = 57
                    full = content
                    if sub.get("commands"):
                        full += "\n\n## دستورات\n\n" + str(sub.get("commands"))
                    out.append({
                        "uid": f"lesson:ch{target:02d}:bp:{li:04d}",
                        "title_fa": title if str(title).startswith("[L") else f"[L2] {title}",
                        "chapter_order": target,
                        "subchapter_order": ci,
                        "level": "L2",
                        "summary": (sub.get("summary") or content[:180]).strip(),
                        "full_content": full,
                        "commands": sub.get("commands") or "",
                        "examples": sub.get("examples") or "",
                        "notes": f"blueprint status={status}",
                    })
    return out


def normalize_pack(path: Path, data: dict):
    if data.get("commands"):
        return commands_to_lessons(data)
    if data.get("lessons"):
        return data.get("lessons") or []
    name = path.name.upper()
    if "curriculum" in data:
        if any(k in name for k in ("OSPF", "BGP", "REDIS")):
            return blueprint_to_lessons(data, ["OSPF", "BGP", "Redistribution", "Adjacency", "eBGP", "iBGP", "SPF"], 14)
        if "VPN" in name or "IPSEC" in name:
            return blueprint_to_lessons(data, ["IPsec", "IKEv", "SSL VPN", "Phase", "Tunnel", "VPN"], 57)
        return blueprint_to_lessons(data, [], 1)
    return []


def apply_fields(les, src):
    for k in ("summary", "full_content", "commands", "examples", "notes"):
        if src.get(k):
            les[k] = as_text(src.get(k)) if k != "full_content" else (src.get(k) or "")


def merge_by_title(data, lessons):
    by = {}
    for src in lessons:
        title = (src.get("title_fa") or "").strip()
        by[(src.get("chapter_order"), title)] = src
        bare = re.sub(r"^\[L[0-4]\]\s*", "", title)
        by[(src.get("chapter_order"), bare)] = src
    n = 0
    for ch in data["chapters"]:
        for sub in ch.get("subchapters", []):
            for les in sub.get("lessons", []):
                t = (les.get("title_fa") or "").strip()
                src = by.get((ch.get("order"), t))
                if not src:
                    bare = re.sub(r"^\[L[0-4]\]\s*", "", t)
                    src = by.get((ch.get("order"), bare))
                if src:
                    apply_fields(les, src)
                    n += 1
    return n


def append_unmatched_as_extra(data, lessons, order, title_fa, title_en):
    if not lessons:
        return 0
    data["chapters"] = [c for c in data["chapters"] if c.get("order") != order]
    subs = defaultdict(list)
    for src in lessons:
        subs[src.get("subchapter_order") or 1].append(src)
    out_subs = []
    for si in sorted(subs):
        les_out = []
        for src in sorted(subs[si], key=lambda x: (x.get("lesson_order") or 0)):
            notes = as_text(src.get("notes"))
            ass = (src.get("meta") or {}).get("assessment")
            if ass and "EJ_ASSESSMENT" not in notes:
                notes += "\n\n<!-- EJ_ASSESSMENT\n" + json.dumps(ass, ensure_ascii=False) + "\n-->\n"
            les_out.append({
                "uid": src.get("uid") or f"lesson:ch{order:02d}:s{int(si):03d}:l{len(les_out):04d}",
                "title_fa": src.get("title_fa") or "",
                "title_en": src.get("title_en") or "",
                "level": src.get("level") or "L0",
                "summary": src.get("summary") or "",
                "full_content": src.get("full_content") or "",
                "commands": as_text(src.get("commands")),
                "examples": as_text(src.get("examples")),
                "notes": notes,
            })
        out_subs.append({"title_fa": f"زیرفصل {si}", "lessons": les_out})
    data["chapters"].append({
        "order": order,
        "title_fa": title_fa,
        "title_en": title_en,
        "subchapters": out_subs,
    })
    return sum(len(s["lessons"]) for s in out_subs)


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
    routing_extra, vpn_extra, cmd_extra = [], [], []
    for p in packs:
        try:
            d = load_json(p)
        except Exception as e:
            print(" skip", p.name, e)
            continue
        name = str(p).replace("\\", "/").lower()
        lessons = normalize_pack(p, d)
        print(" ", p.name, "lessons", len(lessons))
        if not lessons:
            continue
        if "security_ethical" in name:
            sec.extend(lessons)
            continue
        if "wireless" in name and "vpn" not in name:
            wireless.extend(lessons)
            continue
        if d.get("commands") or "commands_encyclopedia" in name:
            cmd_extra.extend(lessons)
            continue
        n = merge_by_title(data, lessons)
        print("   title-merge", n)
        if "ospf" in name or "bgp" in name or "redistribution" in name or "routing_deep" in name:
            routing_extra.extend(lessons)
        if "vpn" in name or "ipsec" in name:
            vpn_extra.extend(lessons)

    if routing_extra:
        n = append_unmatched_as_extra(
            data, routing_extra, 66,
            "فصل ۶۶: مسیریابی عمیق OSPF/BGP/Redistribution",
            "Ch66 Routing Deep OSPF BGP",
        )
        print("ch66 routing", n)
    if vpn_extra:
        n = append_unmatched_as_extra(
            data, vpn_extra, 67,
            "فصل ۶۷: VPN سازمانی IPsec/SSL و عیب‌یابی",
            "Ch67 Enterprise VPN",
        )
        print("ch67 vpn", n)
    if cmd_extra:
        n = append_unmatched_as_extra(
            data, cmd_extra, 68,
            "فصل ۶۸: دانشنامه جامع دستورات",
            "Ch68 Commands Encyclopedia",
        )
        print("ch68 commands", n)

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
    data["version"] = int(data.get("version") or 7) + 1
    GZ.write_bytes(
        gzip.compress(json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8"), 9)
    )
    print("FINAL chapters", len(data["chapters"]), "lessons", n, "version", data["version"])
    for c in data["chapters"][-6:]:
        print(" ", c["order"], c["title_fa"][:52], sum(len(s["lessons"]) for s in c["subchapters"]))


if __name__ == "__main__":
    main()
