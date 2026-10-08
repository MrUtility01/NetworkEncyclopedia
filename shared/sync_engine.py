# -*- coding: utf-8 -*-
"""موتور همگام‌سازی مشترک — hash / LWW / manifest."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

SCHEMA_VERSION = 1


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def content_hash(payload: Dict[str, Any]) -> str:
    """هش پایدار از فیلدهای معنایی (نه device_id)."""
    keys = sorted(k for k in payload.keys() if k not in ("device_id", "last_updated", "content_hash"))
    blob = json.dumps({k: payload[k] for k in keys}, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def lesson_uid(chapter_order: int, level_order: int, lesson_order: int) -> str:
    return f"lesson:ch{chapter_order:02d}:lv{level_order:03d}:l{lesson_order:04d}"


def scenario_uid(code: str) -> str:
    return f"scenario:{code}"


def compare_lww(server: Dict[str, Any], client: Dict[str, Any]) -> str:
    """برمی‌گرداند: accept_client | keep_server | equal | conflict"""
    su = server.get("last_updated") or ""
    cu = client.get("last_updated") or ""
    sh = server.get("content_hash") or ""
    ch = client.get("content_hash") or content_hash(client)
    if cu > su:
        return "accept_client"
    if cu < su:
        return "keep_server"
    if sh == ch:
        return "equal"
    return "conflict"


def build_manifest(records: List[Dict[str, Any]], since: Optional[str] = None) -> Dict[str, Any]:
    items = []
    for r in records:
        if since and (r.get("last_updated") or "") <= since:
            continue
        items.append(
            {
                "uid": r["uid"],
                "entity": r.get("entity", "lesson"),
                "last_updated": r.get("last_updated"),
                "content_hash": r.get("content_hash"),
                "deleted": bool(r.get("deleted")),
            }
        )
    return {"schema_version": SCHEMA_VERSION, "generated_at": utc_now(), "items": items}


def merge_push(
    server_by_uid: Dict[str, Dict[str, Any]],
    client_records: List[Dict[str, Any]],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    """(applied, rejected_keep_server, conflicts)"""
    applied, rejected, conflicts = [], [], []
    for c in client_records:
        uid = c.get("uid")
        if not uid:
            continue
        if "content_hash" not in c or not c["content_hash"]:
            c["content_hash"] = content_hash(c)
        s = server_by_uid.get(uid)
        if s is None:
            applied.append(c)
            continue
        decision = compare_lww(s, c)
        if decision == "accept_client":
            applied.append(c)
        elif decision in ("keep_server", "equal"):
            rejected.append({"uid": uid, "reason": decision, "server": s})
        else:
            conflicts.append({"uid": uid, "server": s, "client": c})
    return applied, rejected, conflicts
