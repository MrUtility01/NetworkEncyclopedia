#!/usr/bin/env python3
"""Install launcher icons — uses tools/launcher_photo.b64 (user portrait) if present."""
from __future__ import annotations
import base64, struct, zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def png_rgb(w, h, rgb=(14, 165, 233)):
    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
    rows = []
    cx, cy = w / 2, h / 2
    for y in range(h):
        row = b"\x00"
        for x in range(w):
            dx, dy = (x - cx) / max(cx, 1), (y - cy) / max(cy, 1)
            f = max(0.0, 1.0 - (dx * dx + dy * dy) ** 0.5)
            r = int(rgb[0] * (0.55 + 0.45 * f))
            g = int(rgb[1] * (0.55 + 0.45 * f))
            b = int(rgb[2] * (0.55 + 0.45 * f))
            row += bytes((r, g, b))
        rows.append(row)
    raw = b"".join(rows)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b"")

def main():
    photo_b64 = ROOT / "tools" / "launcher_photo.b64"
    photo_png = ROOT / "android" / "app" / "src" / "main" / "res" / "drawable" / "ic_launcher_photo.png"
    data = None
    if photo_b64.is_file():
        data = base64.b64decode(photo_b64.read_text().strip())
        print("using tools/launcher_photo.b64")
    elif photo_png.is_file():
        data = photo_png.read_bytes()
        print("using drawable photo png")
    for dens, size in (("mdpi", 48), ("hdpi", 72), ("xhdpi", 96), ("xxhdpi", 144), ("xxxhdpi", 192)):
        d = ROOT / f"android/app/src/main/res/mipmap-{dens}"
        d.mkdir(parents=True, exist_ok=True)
        blob = data if data is not None else png_rgb(size, size)
        (d / "ic_launcher.png").write_bytes(blob)
        (d / "ic_launcher_round.png").write_bytes(blob)
    print("launcher icons ready")

if __name__ == "__main__":
    main()
