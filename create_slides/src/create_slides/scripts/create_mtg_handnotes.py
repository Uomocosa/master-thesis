"""Entry point: build MTG-card-sized hand notes from the v4 deck + DISCUSSION.md.

For every visible slide of `master-thesis-slides/Slide_Samuele_Maggiori_v4.pptx`:
- `MTG_HANDNOTES/front_N.png` — the slide screenshot with each embedded video replaced
  by its FINAL frame (the state at the end of the animations), rotated to fill a
  63x88 mm MTG card at 300 DPI;
- `MTG_HANDNOTES/back_N.png` — the matching DISCUSSION.md speech inside a thin UniSi-red
  outline, same card size.

Also emits A4 print sheets (`sheet_K_fronts.png` / `sheet_K_backs.png`, 3x3 cards each,
with cut marks) to print, cut and sleeve.
"""

import re
from pathlib import Path

import av
from loguru import logger
from PIL import Image, ImageDraw, ImageFont

from create_slides.WebExport.web_export import extract_slides, hidden_slide_numbers

CREATE_SLIDES_DIR = Path(__file__).resolve().parents[3]
REPO_ROOT = CREATE_SLIDES_DIR.parent
SLIDES_REPO = REPO_ROOT.parent / "master-thesis-slides"
PPTX_PATH = SLIDES_REPO / "Slide_Samuele_Maggiori_v4.pptx"
DOCS_ASSETS = SLIDES_REPO / "docs" / "assets"
DISCUSSION = REPO_ROOT / "DISCUSSION.md"
OUT_DIR = REPO_ROOT / "MTG_HANDNOTES"

DPI = 300
CARD_W, CARD_H = 744, 1063  # 63 x 88 mm at 300 DPI (MTG card)
A4_W, A4_H = 2480, 3508  # 210 x 297 mm at 300 DPI
UNISI_RED = (0x99, 0x00, 0x00)
FONTS = Path(r"C:\Windows\Fonts")


def last_frame(video_path: Path) -> Image.Image:
    """Decode the final frame of the video (what the animation ends on)."""
    container = av.open(str(video_path))
    stream = container.streams.video[0]
    end_seconds = float(stream.duration * stream.time_base) - 0.5
    container.seek(int(max(end_seconds, 0) / stream.time_base), stream=stream)
    image = None
    for frame in container.decode(stream):
        image = frame.to_image()
    container.close()
    if image is None:
        raise ValueError(f"no frame decoded from {video_path}")
    return image


def contain(image: Image.Image, box_w: int, box_h: int) -> Image.Image:
    scale = min(box_w / image.width, box_h / image.height)
    return image.resize((round(image.width * scale), round(image.height * scale)))


def parse_discussion() -> dict[int, tuple[str, str]]:
    """DISCUSSION.md -> {slide number: (title, speech)}; %...% side notes stripped."""
    sections: dict[int, tuple[str, str]] = {}
    for match in re.finditer(
        r"^### (\d+)\. (.+?)\n(.*?)(?=^### |\Z)", DISCUSSION.read_text(encoding="utf-8"),
        flags=re.M | re.S,
    ):
        speech = re.sub(r"%[^%]*%", "", match.group(3)).strip()
        speech = re.sub(r"[ \t]+", " ", speech)
        sections[int(match.group(1))] = (match.group(2).strip(), speech)
    return sections


def build_front(slide_png: Path, videos, out_path: Path) -> None:
    """Slide screenshot + final video frames at their rects, rotated onto the card."""
    base = Image.open(slide_png).convert("RGB")
    for v in videos:
        rect_w = round(v.width * base.width)
        rect_h = round(v.height * base.height)
        frame = contain(last_frame(DOCS_ASSETS / Path(v.src).name), rect_w, rect_h)
        x = round(v.left * base.width) + (rect_w - frame.width) // 2
        y = round(v.top * base.height) + (rect_h - frame.height) // 2
        base.paste(frame, (x, y))
    # Portrait card: the rotated slide uses the card area far better than landscape.
    rotated = base.rotate(270, expand=True)
    card = Image.new("RGB", (CARD_W, CARD_H), "white")
    margin = 16
    fitted = contain(rotated, CARD_W - 2 * margin, CARD_H - 2 * margin)
    card.paste(fitted, ((CARD_W - fitted.width) // 2, (CARD_H - fitted.height) // 2))
    card.save(out_path, dpi=(DPI, DPI))


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font, max_w: int) -> list[str]:
    lines: list[str] = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            continue
        line = words[0]
        for word in words[1:]:
            if draw.textlength(f"{line} {word}", font=font) <= max_w:
                line = f"{line} {word}"
            else:
                lines.append(line)
                line = word
        lines.append(line)
    return lines


def build_back(number: int, title: str, speech: str, out_path: Path) -> None:
    # Draw on a landscape canvas, then rotate so the back reads in the same held
    # orientation as the (rotated) front slide.
    canvas_w, canvas_h = CARD_H, CARD_W
    card = Image.new("RGB", (canvas_w, canvas_h), "white")
    draw = ImageDraw.Draw(card)
    # Thin double outline, kept close to the edge so it stays discreet.
    draw.rounded_rectangle([14, 14, canvas_w - 15, canvas_h - 15], radius=24,
                           outline=UNISI_RED, width=3)
    draw.rounded_rectangle([24, 24, canvas_w - 25, canvas_h - 25], radius=18,
                           outline=UNISI_RED, width=1)

    pad = 46
    max_w = canvas_w - 2 * pad
    title_font = ImageFont.truetype(str(FONTS / "calibrib.ttf"), 34)
    title_lines = wrap_text(draw, f"{number}. {title}", title_font, max_w)
    title_h = 40 * len(title_lines) + 8
    divider_gap = 16

    # Auto-shrink the speech font until the whole block fits between the borders.
    for size in range(30, 13, -1):
        body_font = ImageFont.truetype(str(FONTS / "calibri.ttf"), size)
        line_h = round(size * 1.22)
        lines = wrap_text(draw, speech, body_font, max_w)
        total_h = title_h + divider_gap + line_h * len(lines)
        if total_h <= canvas_h - 2 * pad:
            break

    # Vertically center the whole block (title + divider + speech).
    y = max(pad, (canvas_h - total_h) // 2)
    for line in title_lines:
        draw.text((canvas_w / 2, y), line, font=title_font, fill=UNISI_RED, anchor="ma")
        y += 40
    y += 8
    draw.line([pad, y, canvas_w - pad, y], fill=UNISI_RED, width=2)
    y += divider_gap
    for line in lines:
        draw.text((pad, y), line, font=body_font, fill=(20, 20, 20))
        y += line_h

    card.rotate(270, expand=True).save(out_path, dpi=(DPI, DPI))


def build_sheets(cards: list[Path], stem: str) -> None:
    """3x3 grids of cards on A4 pages with light cut marks."""
    for page, start in enumerate(range(0, len(cards), 9), start=1):
        sheet = Image.new("RGB", (A4_W, A4_H), "white")
        draw = ImageDraw.Draw(sheet)
        grid_w, grid_h = CARD_W * 3, CARD_H * 3
        ox, oy = (A4_W - grid_w) // 2, (A4_H - grid_h) // 2
        for i, card_path in enumerate(cards[start : start + 9]):
            col, row = i % 3, i // 3
            sheet.paste(Image.open(card_path), (ox + col * CARD_W, oy + row * CARD_H))
        for c in range(4):  # cut lines across the full page
            x = ox + c * CARD_W
            draw.line([x, 0, x, A4_H], fill=(180, 180, 180), width=1)
        for r in range(4):
            y = oy + r * CARD_H
            draw.line([0, y, A4_W, y], fill=(180, 180, 180), width=1)
        out = OUT_DIR / f"sheet_{page}_{stem}.png"
        sheet.save(out, dpi=(DPI, DPI))
        logger.info(f"wrote {out}")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    hidden = hidden_slide_numbers(PPTX_PATH)
    image_names = {
        int(p.stem.removeprefix("slide")): p.name
        for p in DOCS_ASSETS.glob("slide[0-9][0-9].png")
    }
    (OUT_DIR / "_tmp").mkdir(exist_ok=True)
    slides = extract_slides(PPTX_PATH, OUT_DIR / "_tmp", image_names, hidden)
    for tmp in (OUT_DIR / "_tmp").glob("*"):
        tmp.unlink()  # extract_slides re-dumps the videos; we read them from docs/assets
    (OUT_DIR / "_tmp").rmdir()
    speeches = parse_discussion()

    fronts: list[Path] = []
    backs: list[Path] = []
    for slide in slides:
        front = OUT_DIR / f"front_{slide.index}.png"
        build_front(DOCS_ASSETS / Path(slide.image).name, slide.videos, front)
        title, speech = speeches[slide.index]
        back = OUT_DIR / f"back_{slide.index}.png"
        build_back(slide.index, title, speech, back)
        fronts.append(front)
        backs.append(back)
        logger.info(f"card {slide.index}: front + back")

    build_sheets(fronts, "fronts")
    build_sheets(backs, "backs")
    logger.info(f"{len(fronts)} cards in {OUT_DIR}")


if __name__ == "__main__":
    main()
