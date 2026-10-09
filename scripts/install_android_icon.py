#!/usr/bin/env python3
"""Generate mipmap launcher icons (portrait-style teal tile if no photo asset)."""
from __future__ import annotations
import struct, zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def png_rgb(w: int, h: int, rgb=(14, 165, 233)):
    def chunk(tag: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
    # simple radial-ish: center lighter
    rows = []
    cx, cy = w / 2, h / 2
    for y in range(h):
        row = b"\x00"
        for x in range(w):
            dx, dy = (x - cx) / cx, (y - cy) / cy
            f = max(0.0, 1.0 - (dx * dx + dy * dy) ** 0.5)
            r = int(rgb[0] * (0.55 + 0.45 * f))
            g = int(rgb[1] * (0.55 + 0.45 * f))
            b = int(rgb[2] * (0.55 + 0.45 * f))
            row += bytes((r, g, b))
        rows.append(row)
    raw = b"".join(rows)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b"")

def main():
    # Prefer pre-supplied PNG if present (user photo export)
    photo = ROOT / "android/app/src/main/res/drawable/ic_launcher_photo.png"
    for dens, size in (("mdpi", 48), ("hdpi", 72), ("xhdpi", 96), ("xxhdpi", 144), ("xxxhdpi", 192)):
        d = ROOT / f"android/app/src/main/res/mipmap-{dens}"
        d.mkdir(parents=True, exist_ok=True)
        if photo.is_file():
            data = photo.read_bytes()
        else:
            data = png_rgb(size, size)
        (d / "ic_launcher.png").write_bytes(data)
        (d / "ic_launcher_round.png").write_bytes(data)
    print("launcher icons ready")

if __name__ == "__main__":
    main()
