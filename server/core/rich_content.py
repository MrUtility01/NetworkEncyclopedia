# -*- coding: utf-8 -*-
"""محتوای عمیق: teacher اختصاصی + deep_fallback."""
from __future__ import annotations
import re
from typing import Any, Dict
from core.rich_data import BANKS, COMMON

def level_tag(title: str) -> str:
    m = re.match(r"\[(L[0-4])\]", title or "")
    return m.group(1) if m else "L0"

def clean_topic(title: str) -> str:
    t = re.sub(r"^\[L[0-4]\]\s*", "", title or "").strip()
    t = re.sub(r"\s*[—\-]\s*(آشنایی|مقدماتی|ادمین|مهندس|خبره).*$", "", t, flags=re.I)
    return t.strip() or (title or "موضوع")

def _fmt_cmds(pairs):
    return "\n".join(f"```\n{cmd}\n```\n→ {desc}\n" for cmd, desc in pairs)

def build_rich_lesson(title_fa: str, title_en: str = "", level: str | None = None) -> Dict[str, Any]:
    try:
        from core.chapter17_teacher import build_chapter17_lesson
        if any(k in (title_fa or "") for k in ("VXLAN", "VNI", "VTEP", "Overlay", "EVPN", "Control Plane", "Route Type", "Leaf", "Spine", "Underlay", "Anycast", "RT-2", "RT-3", "RT-5")):
            c = build_chapter17_lesson(title_fa, title_en)
            if c: return _ensure_dense(title_fa, title_en, level, c)
    except Exception:
        pass
    try:
        from core.chapter16_teacher import build_chapter16_lesson
        if any(k in (title_fa or "") for k in ("Multicast", "PIM", "IGMP", "Dense", "Sparse", "IPTV", "چرا Multicast", "Rendezvous", "MLD", "SSM")):
            c = build_chapter16_lesson(title_fa, title_en)
            if c: return _ensure_dense(title_fa, title_en, level, c)
    except Exception:
        pass
    try:
        from core.chapter15_teacher import build_chapter15_lesson
        if any(k in (title_fa or "") for k in ("VRF", "MPLS", "Label", "L3VPN", "PE P CE", "LDP", "LSP", "Route Target", "Route Distinguisher", "VPNv4", "Label Switching", "PHP")):
            c = build_chapter15_lesson(title_fa, title_en)
            if c: return _ensure_dense(title_fa, title_en, level, c)
    except Exception:
        pass
    try:
        from core.chapter14_teacher import build_chapter14_lesson
        if any(k in (title_fa or "") for k in ("Static Route", "OSPF", "Link-State", "EIGRP", "Metric مرکب", "BGP", "AS Number", "Prefix-list", "route-map", "Redistribut", "Floating", "LSA", "eBGP", "iBGP", "Administrative Distance", "next-hop")):
            c = build_chapter14_lesson(title_fa, title_en)
            if c: return _ensure_dense(title_fa, title_en, level, c)
    except Exception:
        pass
    try:
        from core.chapter13_teacher import build_chapter13_lesson
        if any(k in (title_fa or "") for k in ("VLAN", "مفهوم VLAN", "Trunk", "STP", "RSTP", "Loop", "Root Bridge", "EtherChannel", "LACP", "Port Security", "DHCP Snooping", "BPDU", "802.1X", "PortFast", "Native VLAN", "SVI", "Storm Control", "DAI")):
            c = build_chapter13_lesson(title_fa, title_en)
            if c: return _ensure_dense(title_fa, title_en, level, c)
    except Exception:
        pass
    try:
        from core.chapter12_teacher import build_chapter12_lesson
        if any(k in (title_fa or "") for k in ("Cat5", "Cat6", "Cat6A", "OM3", "OM4", "فیبر", "Fiber", "رک", "Rack", "Wiremap", "PDU", "PoE", "T568", "RJ45", "OTDR")):
            c = build_chapter12_lesson(title_fa, title_en)
            if c: return _ensure_dense(title_fa, title_en, level, c)
    except Exception:
        pass
    try:
        from core.chapter11_teacher import build_chapter11_lesson
        if any(k in (title_fa or "") for k in ("DHCP", "DORA", "Discover", "Offer", "Relay", "helper", "IPAM", "Lease", "Scope", "Reservation", "APIPA", "Renew")):
            c = build_chapter11_lesson(title_fa, title_en)
            if c: return _ensure_dense(title_fa, title_en, level, c)
    except Exception:
        pass
    try:
        from core.chapter10_teacher import build_chapter10_lesson
        if any(k in (title_fa or "") for k in ("DNS", "Resolver", "AAAA", "CNAME", "MX", "TXT", "SOA", "PTR", "SRV", "Forwarder", "DNSSEC", "رکورد", "TTL", "nslookup")):
            c = build_chapter10_lesson(title_fa, title_en)
            if c: return _ensure_dense(title_fa, title_en, level, c)
    except Exception:
        pass
    try:
        from core.chapter09_teacher import build_chapter09_lesson
        if any(k in (title_fa or "") for k in ("ARP", "ICMP", "Echo", "Three-way", "Handshake", "TCP", "UDP", "Sequence", "Window", "SYN", "FIN", "RST", "traceroute", "ویژگی‌ها")):
            c = build_chapter09_lesson(title_fa, title_en)
            if c: return _ensure_dense(title_fa, title_en, level, c)
    except Exception:
        pass
    try:
        from core.chapter08_teacher import build_chapter08_lesson
        if any(k in (title_fa or "") for k in ("IPv4", "IPv6", "Subnet", "ساب‌نت", "ماسک", "CIDR", "VLSM", "SLAAC", "fe80", "NDP", "RFC1918", "DMZ")):
            c = build_chapter08_lesson(title_fa, title_en)
            if c: return _ensure_dense(title_fa, title_en, level, c)
    except Exception:
        pass
    try:
        from core.chapter07_teacher import build_chapter07_lesson
        if any(k in (title_fa or "") for k in ("فریم", "Frame", "اترنت", "Ethernet", "MAC Table", "Learning", "Store-and-Forward", "سوییچ", "Switch", "Duplex", "FCS", "CRC", "CAM", "MTU", "SFP")):
            c = build_chapter07_lesson(title_fa, title_en)
            if c: return _ensure_dense(title_fa, title_en, level, c)
    except Exception:
        pass
    try:
        from core.chapter06_teacher import build_chapter06_lesson
        if any(k in (title_fa or "") for k in ("LAN", "WAN", "WLAN", "OSI", "TCP/IP", "Packet", "Encapsulation", "توپولوژی", "Broadcast", "Unicast", "Gateway", "مبانی شبکه")):
            if not any(k in (title_fa or "") for k in ("IPv4", "IPv6", "Subnet", "ARP", "ICMP", "DNS", "DHCP", "VLAN", "STP", "OSPF", "BGP", "MPLS", "Multicast", "VXLAN", "EVPN")):
                c = build_chapter06_lesson(title_fa, title_en)
                if c: return _ensure_dense(title_fa, title_en, level, c)
    except Exception:
        pass
    try:
        from core.chapter03_teacher import build_chapter03_lesson
        if any(k in (title_fa or "") for k in ("BIOS", "UEFI", "بوت", "Boot", "Secure Boot", "TPM", "CMOS", "GRUB", "PXE")):
            c = build_chapter03_lesson(title_fa, title_en)
            if c: return _ensure_dense(title_fa, title_en, level, c)
    except Exception:
        pass
    try:
        from core.chapter05_teacher import build_chapter05_lesson
        if any(k in (title_fa or "") for k in ("FAT", "NTFS", "ext4", "XFS", "MBR", "GPT", "پارتیشن", "RAID", "fsck", "mount", "mdadm")):
            c = build_chapter05_lesson(title_fa, title_en)
            if c: return _ensure_dense(title_fa, title_en, level, c)
    except Exception:
        pass
    try:
        from core.chapter04_teacher import build_chapter04_lesson
        if any(k in (title_fa or "") for k in ("Kernel", "هسته", "Registry", "ویندوز", "Windows", "لینوکس", "Linux", "systemd", "Process", "PowerShell", "Task Manager")):
            c = build_chapter04_lesson(title_fa, title_en)
            if c: return _ensure_dense(title_fa, title_en, level, c)
    except Exception:
        pass
    try:
        from core.chapter02_teacher import build_chapter02_lesson
        if any(k in (title_fa or "") for k in ("ESD", "ایمنی", "اسمبل", "Beep", "ProLiant", "iLO", "سرور HP")):
            c = build_chapter02_lesson(title_fa, title_en)
            if c: return _ensure_dense(title_fa, title_en, level, c)
    except Exception:
        pass
    try:
        from core.chapter01_teacher import build_chapter01_lesson, _bucket, _topic
        topic0 = _topic(title_fa)
        if _bucket(topic0) in ("cpu", "ram", "storage", "mb", "psu") or any(k in (title_fa or "") for k in ("CPU", "ALU", "RAM", "DDR", "SSD", "HDD", "NVMe", "مادربرد", "Chipset", "PSU", "تغذیه")):
            if not any(k in (title_fa or "") for k in ("BIOS", "UEFI", "Boot", "CPU بالا", "RAID", "LAN", "IPv4", "TCP", "DNS", "DHCP", "VLAN", "OSPF", "MPLS", "Multicast", "VXLAN")):
                c = build_chapter01_lesson(title_fa, title_en)
                if c: return _ensure_dense(title_fa, title_en, level, c)
    except Exception:
        pass
    from core.deep_fallback import build_deep_fallback
    return build_deep_fallback(title_fa, title_en, level or level_tag(title_fa))


def _content_len(d: Dict[str, Any]) -> int:
    return sum(len(str(d.get(k) or "")) for k in ("summary", "full_content", "commands", "examples", "notes"))


def _ensure_dense(title_fa: str, title_en: str, level: str | None, candidate: Dict[str, Any] | None) -> Dict[str, Any]:
    """اگر teacher خیلی کوتاه بود، deep_fallback را پایه کن و فیلدهای مفید teacher را روی آن سوار کن."""
    from core.deep_fallback import build_deep_fallback
    dense = build_deep_fallback(title_fa, title_en, level or level_tag(title_fa))
    if not candidate:
        return dense
    if _content_len(candidate) >= 4000:
        return candidate
    out = dict(dense)
    for k in ("commands", "examples", "notes", "lab"):
        cv = str(candidate.get(k) or "")
        if len(cv) > len(str(out.get(k) or "")):
            out[k] = cv
    cs = str(candidate.get("summary") or "").strip()
    if cs and cs not in str(out.get("summary") or ""):
        out["summary"] = cs + " | " + str(out.get("summary") or "")
    cf = str(candidate.get("full_content") or "").strip()
    if cf and len(cf) > 80:
        out["full_content"] = str(out.get("full_content") or "") + "\n\n---\n## یادداشت تخصصی Teacher\n\n" + cf
    out["level"] = candidate.get("level") or out.get("level")
    out["topic"] = candidate.get("topic") or out.get("topic")
    out["category"] = candidate.get("category") or out.get("category")
    return out
