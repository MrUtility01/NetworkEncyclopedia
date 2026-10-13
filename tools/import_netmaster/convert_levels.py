# -*- coding: utf-8 -*-
"""تبدیل سطح‌های NetMasterLearning → پک NetworkEncyclopedia"""
from __future__ import annotations
import json
import sys
from pathlib import Path

NM = Path.home() / "NetMasterLearning" / "app" / "src" / "main" / "assets" / "curriculum.json"
OUT_DIR = Path(__file__).resolve().parents[1] / "packs" / "ordered_fill"

# نگاشت تقریبی سطح NetMaster → chapter_order در NE (قابل تنظیم)
LEVEL_TO_CHAPTER = {
    1: 1,   # مبانی IT
    2: 2,   # مبانی شبکه
    3: 3,   # Ethernet
    4: 4,   # IP
    5: 5,   # ARP/ICMP
    6: 6,   # Switching
    7: 7,   # VLAN
    8: 8,   # STP
    9: 9,   # Routing
    10: 10, # TCP/UDP
    11: 11, # DHCP
    12: 12, # DNS
}

def as_list(v):
    if v is None:
        return []
    if isinstance(v, list):
        return [str(x) for x in v]
    return [str(v)]

def build_full(L: dict) -> str:
    parts = []
    title = L.get("title") or ""
    parts.append(f"# {title}\n")
    if L.get("why_it_matters"):
        parts.append("## چرا مهم است\n" + L["why_it_matters"].strip() + "\n")
    if L.get("goal"):
        parts.append("## هدف یادگیری\n" + L["goal"].strip() + "\n")
    if L.get("simple"):
        parts.append("## از صفر\n" + L["simple"].strip() + "\n")
    if L.get("technical") or L.get("internals"):
        parts.append("## عمق فنی\n")
        if L.get("technical"):
            parts.append(L["technical"].strip() + "\n")
        if L.get("internals"):
            parts.append(L["internals"].strip() + "\n")
    if L.get("mental_model") or L.get("diagram") or L.get("state_machine"):
        parts.append("## مدل و معماری\n")
        for k in ("mental_model", "diagram", "state_machine"):
            if L.get(k):
                parts.append(L[k].strip() + "\n")
    if L.get("packet_state_walkthrough") or L.get("packetWalkthrough") or L.get("traffic"):
        parts.append("## مسیر پکت / State\n")
        for k in ("packet_state_walkthrough", "packetWalkthrough", "traffic"):
            if L.get(k):
                parts.append(L[k].strip() + "\n")
    if L.get("example") or L.get("realScenario") or L.get("expert_scenario"):
        parts.append("## مثال عملی\n")
        for k in ("example", "realScenario", "expert_scenario"):
            if L.get(k):
                parts.append(L[k].strip() + "\n")
    cmds = (L.get("commands") or "").strip()
    pcmd = (L.get("platformCommands") or "").strip()
    if cmds or pcmd:
        parts.append("## دستورات\n```\n")
        if cmds:
            parts.append(cmds + "\n")
        if pcmd:
            parts.append(pcmd + "\n")
        parts.append("```\n")
    if L.get("configurationPlaybook") or L.get("configuration_playbook"):
        parts.append("## پیکربندی\n")
        for k in ("configurationPlaybook", "configuration_playbook"):
            if L.get(k):
                parts.append(L[k].strip() + "\n")
    if L.get("verification"):
        parts.append("## Verification\n" + L["verification"].strip() + "\n")
    if L.get("troubleshooting") or L.get("failure_analysis"):
        parts.append("## عیب‌یابی\n")
        for k in ("troubleshooting", "failure_analysis"):
            if L.get(k):
                parts.append(L[k].strip() + "\n")
        fm = L.get("failureMatrix") or []
        if fm:
            parts.append("### ماتریس خطا\n")
            for row in fm:
                parts.append(f"- {row}\n")
    if L.get("lab") or L.get("labSteps"):
        parts.append("## لابراتوار\n")
        if L.get("lab"):
            parts.append(L["lab"].strip() + "\n")
        for i, step in enumerate(as_list(L.get("labSteps")), 1):
            parts.append(f"{i}. {step}\n")
    if L.get("evidenceChecklist"):
        parts.append("## Evidence\n")
        for e in as_list(L["evidenceChecklist"]):
            parts.append(f"- {e}\n")
    if L.get("keyPoints"):
        parts.append("## نکات کلیدی\n")
        for p in as_list(L["keyPoints"]):
            parts.append(f"- {p}\n")
    if L.get("commonMistakes"):
        parts.append("## اشتباهات رایج\n")
        for m in as_list(L["commonMistakes"]):
            parts.append(f"- {m}\n")
    if L.get("mastery"):
        parts.append("## تسلط\n" + L["mastery"].strip() + "\n")
    text = "\n".join(parts).strip() + "\n"
    return text

def convert_levels(level_ids: list[int]) -> dict:
    data = json.loads(NM.read_text(encoding="utf-8"))
    by_id = {int(lv["id"]): lv for lv in data["levels"]}
    lessons_out = []
    for lid in level_ids:
        lv = by_id.get(lid)
        if not lv:
            print("missing level", lid)
            continue
        ch = LEVEL_TO_CHAPTER.get(lid, lid)
        for L in lv.get("lessons") or []:
            full = build_full(L)
            if len(full) < 200:
                print("skip short", L.get("id"), len(full))
                continue
            objs = as_list(L.get("keyPoints"))[:6]
            if L.get("goal"):
                objs.insert(0, L["goal"][:200])
            lessons_out.append({
                "title_fa": L.get("title") or "",
                "title_en": L.get("id") or "",
                "chapter_order": ch,
                "summary": (L.get("simple") or L.get("goal") or full[:180])[:300],
                "full_content": full,
                "commands": (L.get("commands") or "") + (
                    ("\n" + L["platformCommands"]) if L.get("platformCommands") else ""
                ),
                "examples": "\n\n".join(
                    x for x in [L.get("example"), L.get("lab"), L.get("realScenario")] if x
                ),
                "notes": "\n\n".join(
                    x for x in [L.get("troubleshooting"), L.get("failure_analysis"), L.get("commonMistakes") and "\n".join(as_list(L["commonMistakes"]))] if x
                ),
                "learning_objectives": objs,
            })
            print(f"  OK {L.get('id')} | {L.get('title')[:50]} | {len(full)} chars")
    return {
        "package_schema_version": 1,
        "project": "ENGINEER JOKAR",
        "purpose": f"NetMaster import levels {level_ids}",
        "source": "NetMasterLearning curriculum.json",
        "lessons": lessons_out,
    }

def main():
    # پیش‌فرض: سطح 2 تا 5 (شبکه واقعی)
    ids = [int(x) for x in sys.argv[1:]] or [2, 3, 4, 5]
    if not NM.is_file():
        print("NOT FOUND:", NM)
        sys.exit(1)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    pack = convert_levels(ids)
    out = OUT_DIR / f"netmaster_levels_{'_'.join(map(str, ids))}.json"
    out.write_text(json.dumps(pack, ensure_ascii=False, indent=2), encoding="utf-8")
    print("wrote", out, "lessons", len(pack["lessons"]))
    sizes = [len(x["full_content"]) for x in pack["lessons"]]
    if sizes:
        print("chars min/avg/max", min(sizes), int(sum(sizes)/len(sizes)), max(sizes))

if __name__ == "__main__":
    main()
