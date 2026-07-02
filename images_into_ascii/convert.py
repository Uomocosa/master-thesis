# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pillow",
# ]
# ///

"""
Convert images to colored ASCII art rendered as PNG (LaTeX-ready via includegraphics).

Usage:
    uv run convert.py images/photo.jpg
    uv run convert.py images/*.jpg --width 120 --output-dir ascii_output/
    uv run convert.py images/photo.jpg --font-size 16 --bg 15,15,25
"""

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont

ASCII_CHARS = " `.-':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@"

FONT_CANDIDATES = [
    "C:/Windows/Fonts/consola.ttf",   # Consolas — best for ASCII art
    "C:/Windows/Fonts/cour.ttf",      # Courier New
    "C:/Windows/Fonts/lucon.ttf",     # Lucida Console
]


def load_font(font_size: int) -> ImageFont.FreeTypeFont:
    for path in FONT_CANDIDATES:
        try:
            return ImageFont.truetype(path, font_size)
        except OSError:
            continue
    print("[warn] No system monospace font found, falling back to default", file=sys.stderr)
    return ImageFont.load_default()


def image_to_colored_png(
    path: Path,
    width: int,
    contrast: float,
    font_size: int,
    bg: tuple[int, int, int],
    out_dir: Path,
) -> Path:
    img = Image.open(path).convert("RGB")
    img = ImageEnhance.Contrast(img).enhance(contrast)
    img_gray = img.convert("L")

    # aspect-ratio correction for monospace font: char height / char width
    font = load_font(font_size)
    ascent, descent = font.getmetrics()
    line_h = ascent + descent
    char_w = max(1, int(font.getlength("M")))
    cell_ratio = line_h / char_w  # typically ~2.0 for monospace

    orig_w, orig_h = img.size
    height = max(1, int(orig_h / orig_w * width / cell_ratio))

    img_color = img.resize((width, height), Image.LANCZOS)
    img_gray_small = img_gray.resize((width, height), Image.LANCZOS)

    canvas = Image.new("RGB", (width * char_w, height * line_h), bg)
    draw = ImageDraw.Draw(canvas)

    pixels_gray = list(img_gray_small.getdata())
    pixels_color = list(img_color.getdata())
    n = len(ASCII_CHARS) - 1

    for idx, (pg, pc) in enumerate(zip(pixels_gray, pixels_color)):
        char = ASCII_CHARS[int(pg / 255 * n)]
        if char == " ":
            continue
        col = idx % width
        row = idx // width
        x = col * char_w
        y = row * line_h
        draw.text((x, y), char, font=font, fill=pc)

    out_path = out_dir / f"{path.stem}.png"
    canvas.save(out_path, "PNG", dpi=(300, 300))
    return out_path


def make_tex_snippet(png_path: Path, stem: str, out_dir: Path) -> Path:
    # path relative to main.tex at repo root (images_into_ascii/ascii_output/filename.png)
    rel_str = f"images_into_ascii/ascii_output/{png_path.name}"
    snippet = (
        f"% --- {stem} (colored ASCII art) ---\n"
        "% Paste inside your acknowledgements chapter\n"
        "\\begin{figure}[htbp]\n"
        "\\centering\n"
        f"\\includegraphics[width=0.85\\textwidth]{{{rel_str}}}\n"
        "\\end{figure}\n"
    )
    tex_path = out_dir / f"{stem}.tex"
    tex_path.write_text(snippet, encoding="utf-8")
    return tex_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Image → colored ASCII art PNG for LaTeX thesis")
    parser.add_argument("images", nargs="+", type=Path)
    parser.add_argument("--width", type=int, default=120,
                        help="Characters per row (default: 120)")
    parser.add_argument("--font-size", type=int, default=14,
                        help="Font size in pixels (default: 14 — increase for sharper print)")
    parser.add_argument("--contrast", type=float, default=1.4,
                        help="Contrast boost (default: 1.4)")
    parser.add_argument("--bg", type=str, default="10,10,10",
                        help="Background RGB e.g. '10,10,10' for near-black (default)")
    parser.add_argument("--output-dir", type=Path, default=Path("ascii_output"))
    args = parser.parse_args()

    bg = tuple(int(x) for x in args.bg.split(","))
    args.output_dir.mkdir(parents=True, exist_ok=True)

    for img_path in args.images:
        if not img_path.exists():
            print(f"[skip] {img_path} not found", file=sys.stderr)
            continue

        print(f"  converting {img_path.name} ...", end=" ", flush=True)
        png_path = image_to_colored_png(
            img_path, args.width, args.contrast, args.font_size, bg, args.output_dir
        )
        tex_path = make_tex_snippet(png_path, img_path.stem, args.output_dir)
        print("done")
        print(f"    PNG  -> {png_path}")
        print(f"    .tex -> {tex_path}")


if __name__ == "__main__":
    main()
