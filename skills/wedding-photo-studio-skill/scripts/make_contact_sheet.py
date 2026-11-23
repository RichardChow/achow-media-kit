#!/usr/bin/env python3
"""Assemble individual generated wedding photos into a clean numbered contact sheet.

Supports 2x2 (4 shots), 4x2 / 2x4 (8 shots), and 3x3 (9 shots) layouts while
preserving portrait 3:4 framing by default so gowns, veils, and high-crown hair
are never awkwardly square-cropped.

Inspired by wenyachen/ai-wedding-photo-skill (MIT License) and extended for
wedding-photo-studio-skill's individual-first workflow.
"""

from __future__ import annotations

import argparse
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont, ImageOps
except ImportError as exc:
    raise SystemExit(
        "Pillow is required to build contact sheets. Install it with:\n"
        "  python -m pip install Pillow"
    ) from exc


SUPPORTED_EXTS = {".jpg", ".jpeg", ".png", ".webp"}

LAYOUT_GRIDS = {
    "2x2": (2, 2),
    "4x2": (4, 2),
    "2x4": (2, 4),
    "3x3": (3, 3),
}


def parse_ratio(ratio_str: str) -> tuple[int, int]:
    parts = ratio_str.split(":")
    if len(parts) != 2:
        raise SystemExit(f"Invalid --cell-ratio {ratio_str!r}; expected format W:H such as 3:4 or 1:1")
    w, h = int(parts[0]), int(parts[1])
    if w <= 0 or h <= 0:
        raise SystemExit("--cell-ratio values must be positive integers")
    return w, h


def resolve_grid(layout: str, image_count: int) -> tuple[int, int]:
    if layout != "auto":
        return LAYOUT_GRIDS[layout]
    if image_count <= 4:
        return (2, 2)
    if image_count <= 8:
        return (4, 2)
    return (3, 3)


def draw_index_badge(canvas: Image.Image, x: int, y: int, index: int, cell_w: int) -> None:
    draw = ImageDraw.Draw(canvas, "RGBA")
    badge_size = max(28, int(cell_w * 0.11))
    margin = max(10, int(cell_w * 0.035))
    bx0, by0 = x + margin, y + margin
    bx1, by1 = bx0 + badge_size, by0 + badge_size

    draw.rounded_rectangle(
        (bx0, by0, bx1, by1),
        radius=max(6, badge_size // 4),
        fill=(20, 20, 20, 185),
    )

    label = str(index)
    try:
        font = ImageFont.load_default(size=max(14, int(badge_size * 0.55)))
    except TypeError:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), label, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = bx0 + (badge_size - tw) / 2 - bbox[0]
    ty = by0 + (badge_size - th) / 2 - bbox[1]
    draw.text((tx, ty), label, fill=(255, 255, 255, 245), font=font)


def build_contact_sheet(
    input_dir: Path,
    output_path: Path,
    layout: str = "auto",
    cell_width: int = 600,
    cell_ratio: str = "3:4",
    gap: int = 16,
    outer_margin: int = 24,
    bg_color: str = "#FFFFFF",
    show_numbers: bool = True,
) -> Path:
    if not input_dir.is_dir():
        raise SystemExit(f"Input directory not found: {input_dir}")

    files = sorted(
        p for p in input_dir.iterdir()
        if p.is_file() and p.suffix.lower() in SUPPORTED_EXTS
    )
    if not files:
        raise SystemExit(f"No supported images ({', '.join(sorted(SUPPORTED_EXTS))}) found in {input_dir}")

    cols, rows = resolve_grid(layout, len(files))
    max_slots = cols * rows
    selected = files[:max_slots]

    rw, rh = parse_ratio(cell_ratio)
    cell_h = int(round(cell_width * rh / rw))

    canvas_w = outer_margin * 2 + cols * cell_width + (cols - 1) * gap
    canvas_h = outer_margin * 2 + rows * cell_h + (rows - 1) * gap
    sheet = Image.new("RGB", (canvas_w, canvas_h), bg_color)

    for idx, img_path in enumerate(selected):
        with Image.open(img_path) as img:
            tile = ImageOps.fit(
                img.convert("RGB"),
                (cell_width, cell_h),
                method=Image.Resampling.LANCZOS,
                centering=(0.5, 0.35),
            )
        row, col = divmod(idx, cols)
        x = outer_margin + col * (cell_width + gap)
        y = outer_margin + row * (cell_h + gap)
        sheet.paste(tile, (x, y))
        if show_numbers:
            draw_index_badge(sheet, x, y, idx + 1, cell_width)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output_path, quality=94, optimize=True)
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Stitch individual wedding photos into a clean numbered contact sheet."
    )
    parser.add_argument("input_dir", type=Path, help="Folder containing individual generated images.")
    parser.add_argument("output", type=Path, help="Output contact sheet path (e.g. outputs/preview_grid.jpg).")
    parser.add_argument(
        "--layout",
        choices=("auto", "2x2", "4x2", "2x4", "3x3"),
        default="auto",
        help="Grid layout: auto (<=4: 2x2, <=8: 4x2, 9+: 3x3), 2x2, 4x2, 2x4, or 3x3.",
    )
    parser.add_argument("--cell-width", type=int, default=600, help="Width in pixels per tile (default: 600).")
    parser.add_argument("--cell-ratio", default="3:4", help="Tile aspect ratio W:H (default: 3:4).")
    parser.add_argument("--gap", type=int, default=16, help="Inner spacing between tiles in pixels (default: 16).")
    parser.add_argument("--margin", type=int, default=24, help="Outer canvas border margin in pixels (default: 24).")
    parser.add_argument("--bg", default="#FFFFFF", help="Background color hex (default: #FFFFFF).")
    parser.add_argument("--no-numbers", action="store_true", help="Disable corner index badges.")
    args = parser.parse_args()

    out = build_contact_sheet(
        input_dir=args.input_dir,
        output_path=args.output,
        layout=args.layout,
        cell_width=args.cell_width,
        cell_ratio=args.cell_ratio,
        gap=args.gap,
        outer_margin=args.margin,
        bg_color=args.bg,
        show_numbers=not args.no_numbers,
    )
    print(f"[OK] Contact sheet saved to: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
