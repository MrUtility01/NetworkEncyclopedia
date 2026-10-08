# -*- coding: utf-8 -*-
"""Loader — expands packed curriculum once on first import."""
from __future__ import annotations
import gzip, base64, sys, importlib.util
from pathlib import Path

_PACK = Path(__file__).with_name("_curriculum_pack.b64")
_CACHE = Path(__file__).with_name("_curriculum_expanded.py")

def _ensure():
    if _CACHE.exists() and _CACHE.stat().st_size > 1000:
        return
    if not _PACK.exists():
        raise FileNotFoundError("Missing _curriculum_pack.b64 — run pack script or copy full curriculum")
    raw = base64.b64decode(_PACK.read_text(encoding="ascii"))
    _CACHE.write_bytes(gzip.decompress(raw))

_ensure()
spec = importlib.util.spec_from_file_location("core._curriculum_expanded", _CACHE)
mod = importlib.util.module_from_spec(spec)
sys.modules["core._curriculum_expanded"] = mod
spec.loader.exec_module(mod)
get_full_curriculum = mod.get_full_curriculum
seed_from_full_curriculum = getattr(mod, "seed_from_full_curriculum", None)
rebuild_curriculum_from_scratch = getattr(mod, "rebuild_curriculum_from_scratch", None)
get_meta_template = getattr(mod, "get_meta_template", None)
