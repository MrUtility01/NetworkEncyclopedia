#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Export the canonical server SVG infographic catalog for offline Android use."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "android" / "app" / "src" / "main" / "assets" / "infographics.json"

# Reuse the exact SVG catalog used by the Windows/web version.
sys.path.insert(0, str(ROOT / "server"))
from core.infographics import all_infographics  # noqa: E402


def main() -> int:
    entries = all_infographics()
    items = [
        {"id": index + 1, "title": title, "svg": svg}
        for index, (title, svg) in enumerate(entries)
        if title.strip() and "<svg" in svg.lower() and "</svg>" in svg.lower()
    ]
    if len(items) < 90:
        raise SystemExit(f"Expected at least 90 valid infographic entries, got {len(items)}")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": 1,
        "source": "server/core/infographics.py",
        "count": len(items),
        "items": items,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    print(f"Exported {len(items)} offline SVG diagrams to {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
