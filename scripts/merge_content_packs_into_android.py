#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ادغام بسته‌های tools؛ فصل ۶۴=Git؛ امنیت+وایرلس→۶۵؛ blueprint OSPF/BGP/VPN."""
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
        k = str(f.resolve())
        if k not in seen and f.stat().st_size > 500 and f.name != "README_FA.md":
            seen.add(k)
            uniq.append(f)
    return sorted(uniq)

def blueprint_to_lessons(d, focus_keywords, default_ch):
    """Convert curriculum.chapters blueprint schema to standard lessons list."""
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
                        if "MIKROTIK" in blob or "میکروتیک" in (title + ch_title):
                            target = 21
                    full = content
                    if sub.get("commands"):
                        full += "\n\n## دستورات\n\n" + str(sub.get("commands"))
                    if sub.get("examples"):
                        full += "\n\n## مثال‌ها\n\n" + str(sub.get("examples"))
                    out.append({
                        "uid": f"lesson:ch{target:02d}:bp:{li:04d}",
                        "chapter_order": target,
                        "subchapter_order": ci,
                        "lesson_order": li,
                        "level": "L2",
                        "title_fa": title if str(title).startswith("[L") else f"[L2] {title}",
                        "title_en": sub.get("title_en") or title,
                        "summary": (sub.get("summary") or content[:180]).strip(),
                        "full_content": full,
                        "commands": sub.get("commands") or "",
                        "examples": sub.get("examples") or "",
                        "notes": f"blueprint status={status}",
                    })
    return out

def normalize_pack(path: Path, data: dict):
    if data.get("lessons"):
        return data.get("lessons") or []
    name = path.name.upper()
    if "curriculum" in data and isinstance(data.get("curriculum"), dict):
        if "OSPF" in name or "BGP" in name or "REDIS" in name:
            return blueprint_to_lessons(data, ["OSPF","BGP","Redistribution","Redistrib","Adjacency","eBGP","iBGP","SPF","LSA","Seed Metric","prefix","Route-map"], 14)
        if "VPN" in name or "IPSEC" in name:
            return blueprint_to_lessons(data, ["IPsec","IKEv","SSL VPN","Phase","Tunnel","Site-to-Site","Dial-up","VPN","Proposal","Peer","Portal"], 57)
        # generic: all developed/reviewed
        return blueprint_to_lessons(data, [], 1)
    return []

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
        # also match without [L2] prefix
        bare = re.sub(r"^\[L[0-4]\]\s*", "", title)
        by[("t", title)] = src
        by[("t", bare)] = src
        by[("bare", bare)] = src
    n = 0
    for ch in data["chapters"]:
        for sub in ch.get("subchapters", []):
            for les in sub.get("lessons", []):
                t = les.get("title_fa") or ""
                bare = re.sub(r"^\[L[0-4]\]\s*", "", t)
                # strip trailing level words for fuzzy
                bare2 = re.sub(r"\s*[—\-]\s*(آشنایی|مقدماتی|ادمین|مهندس|خبره).*$", "", bare)
                src = (
                    by.get((ch.get("order"), t))
                    or by.get(("t", t))
                    or by.get(("t", bare))
                    or by.get(("bare", bare2))
                )
                if not src:
                    # substring match on topic keywords
                    for k, v in list(by.items()):
                        if k[0] != "bare":
                            continue
                        if k[1] and (k[1] in t or k[1] in bare):
                            src = v
                            break
                if src:
                    apply_fields(les, src)
                    n += 1
    return n

def append_unmatched_as_extra(data, lessons, order, title_fa, title_en):
    """Lessons that did not match existing titles become extra chapter content via notes marker."""
    # Always build supplemental chapter for deep packs
    if not lessons:
        return 0
    data["chapters"] = [c for c in data["chapters"] if c.get("order") != order]
    subs = defaultdict(list)
    for src in lessons:
        subs[src.get("subchapter_order") or 1].append(src)
    out_subs = []
    for si in sorted(subs):
        les_out = []
        for src in sorted(subs[si], key=lambda x: x.get("lesson_order") or 0):
            les_out.append({
                "uid": src.get("uid") or f"lesson:ch{order:02d}:x:{len(les_out):04d}",
                "title_fa": src.get("title_fa") or "",
                "title_en": src.get("title_en") or "",
                "level": src.get("level") or "L2",
                "summary": src.get("summary") or "",
                "full_content": src.get("full_content") or "",
                "commands": as_text(src.get("commands")),
                "examples": as_text(src.get("examples")),
                "notes": as_text(src.get("notes")),
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
    routing_extra, vpn_extra = [], []
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
        n = merge_by_title(data, lessons)
        print("   title-merge", n)
        if "ospf" in name or "bgp" in name or "redistribution" in name or "routing_deep" in name:
            routing_extra.extend(lessons)
        if "vpn" in name or "ipsec" in name:
            vpn_extra.extend(lessons)

    # supplemental deep chapters (do not overwrite Git 64)
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
    data["version"] = 7
    GZ.write_bytes(gzip.compress(json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8"), 9))
    print("FINAL chapters", len(data["chapters"]), "lessons", n)
    for c in data["chapters"][-5:]:
        print(" ", c["order"], c["title_fa"][:52], sum(len(s["lessons"]) for s in c["subchapters"]))

if __name__ == "__main__":
    main()
