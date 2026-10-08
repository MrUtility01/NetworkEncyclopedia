# -*- coding: utf-8 -*-
"""محتوای عمیق درس‌ها + هوک فصل ۱ استادمحور."""
from __future__ import annotations
import re
from typing import Any, Dict, List, Tuple
from core.rich_data import BANKS, ERRORS, COMMON

def level_tag(title: str) -> str:
    m = re.match(r"\[(L[0-4])\]", title or "")
    return m.group(1) if m else "L0"

def clean_topic(title: str) -> str:
    t = re.sub(r"^\[L[0-4]\]\s*", "", title or "").strip()
    t = re.sub(r"\s*[—\-]\s*(آشنایی|مقدماتی|ادمین|مهندس|خبره|Intro|Junior|Admin|Senior|Architect)\s*$", "", t, flags=re.I)
    return t.strip() or (title or "موضوع")

_LEVEL_FA = {"L0": "آشنایی / مقدماتی", "L1": "Junior", "L2": "Administrator", "L3": "Engineer / Senior", "L4": "Architect"}
_CATS = [
    ("vlan", ["vlan", "trunk", "access", "802.1q", "dot1q", "سگمنت", "tag", "native"]),
    ("stp", ["stp", "spanning", "rstp", "mst", "bpdu", "loop", "portfast"]),
    ("ospf", ["ospf", "area", "lsa", "dr", "bdr", "nssa"]),
    ("bgp", ["bgp", "as path", "prefix-list", "route-map", "ebgp", "ibgp"]),
    ("acl", ["acl", "access-list", "extended", "standard", "filter"]),
    ("nat", ["nat", "pat", "overload", "snat", "dnat", "masquerade"]),
    ("vpn", ["vpn", "ipsec", "ike", "tunnel", "gre", "ssl vpn", "dmvpn"]),
    ("dhcp", ["dhcp", "scope", "lease", "relay", "helper"]),
    ("dns", ["dns", "resolver", "zone", "forwarder"]),
    ("wireless", ["wifi", "wireless", "ssid", "wlc", "802.11", "wpa"]),
    ("firewall", ["firewall", "fortigate", "asa", "policy", "utm", "ngfw"]),
    ("ha", ["hsrp", "vrrp", "glbp", "ha", "failover"]),
    ("qos", ["qos", "dscp", "policing", "shaping", "priority"]),
    ("linux", ["linux", "iptables", "nftables", "systemd", "bash", "sshd"]),
    ("windows", ["windows", "powershell", "gpo", "active directory", "kerberos", "nps"]),
    ("ansible", ["ansible", "playbook", "inventory", "jinja", "awx"]),
    ("terraform", ["terraform", "iac", "provider", "tfstate"]),
    ("python", ["python", "paramiko", "netmiko", "nornir", "scrapli", "fastapi"]),
    ("sql", ["sql", "postgres", "mysql", "mongodb", "redis", "sqlite", "دیتابیس", "database"]),
    ("scrape", ["scrap", "beautifulsoup", "selenium", "playwright", "scrapy", "crawl"]),
    ("cpu", ["cpu", "processor", "core", "thread", "alu"]),
    ("memory", ["ram", "ddr", "ecc", "memory"]),
]

def _cat(topic: str) -> str:
    t = topic.lower()
    for c, keys in _CATS:
        if any(k in t for k in keys):
            return c
    return "general"

def _vendors(topic: str) -> List[str]:
    return ["cisco", "linux", "windows"]

def _fmt_cmds(pairs):
    lines = []
    for cmd, desc in pairs:
        lines.append(f"```\n{cmd}\n```\n→ {desc}\n")
    return "\n".join(lines)

def _commands_block(cat, topic, vendors, level):
    lines = [f"# دستورات — {topic} | {level} | {cat}", "", "## پایه", _fmt_cmds(COMMON),
             f"## تخصصی {cat}", _fmt_cmds(BANKS.get(cat, BANKS.get("linux", [])[:15]))]
    return "\n".join(lines)

def _errors_md(cat, topic):
    rows = ERRORS.get(cat, [(f"سرویس {topic} قطع", "ایزوله L1→L7", "ping / show interface")])
    lines = [f"\n## عیب‌یابی — {topic}\n", "| علامت | علت | اقدام |", "|---|---|---|"]
    for a,b,c in rows:
        lines.append(f"| {a} | {b} | `{c}` |")
    return "\n".join(lines)

def build_rich_lesson(title_fa: str, title_en: str = "", level: str | None = None) -> Dict[str, Any]:
    # فصل ۱ استادمحور + Lab فریم‌به‌فریم
    try:
        from core.chapter01_teacher import build_chapter01_lesson, _bucket, _topic
        topic0 = _topic(title_fa)
        if _bucket(topic0) in ("cpu", "ram", "storage", "mb", "psu") or any(
            k in (title_fa or "") for k in ("CPU", "ALU", "RAM", "DDR", "SSD", "HDD", "NVMe", "مادربرد", "Chipset", "PSU", "تغذیه", "BIOS", "UEFI", "حافظه", "ذخیره")
        ):
            c1 = build_chapter01_lesson(title_fa, title_en)
            if c1:
                return c1
    except Exception:
        pass

    level = level or level_tag(title_fa)
    topic = clean_topic(title_fa)
    cat = _cat(topic)
    vendors = _vendors(topic)
    level_name = _LEVEL_FA.get(level, level)
    summary = f"«{topic}» ({level} — {level_name}): معماری، دستورات، عیب‌یابی، Lab."
    full = f"# {topic}\n\n**سطح:** {level} — {level_name}\n\n## خلاصه\n{summary}\n\n" + _errors_md(cat, topic)
    commands = _commands_block(cat, topic, vendors, level)
    lab = f"## Lab — {topic}\n1. Backup\n2. تغییر کوچک\n3. Verify\n4. Rollback\n"
    return {
        "summary": summary,
        "full_content": full,
        "commands": commands,
        "examples": lab,
        "notes": f"دسته={cat} | سطح={level}",
        "level": level,
        "topic": topic,
        "category": cat,
    }
