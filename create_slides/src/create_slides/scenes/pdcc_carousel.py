import csv
from pathlib import Path

from manim import (
    UP,
    FadeIn,
    Line,
    Scene,
    Text,
    VGroup,
    config,
)

config.background_color = "#FFFFFF"

CSV_PATH = Path(__file__).resolve().parents[3] / "assets" / "animations" / "pdcc.csv"
INK = "#1A1A2E"
ACCENT = "#B31939"

COLUMNS = [
    ("Polimero", "POLYMER_USED", -5.7),
    ("Molecola", "DRUG", -2.0),
    ("pH", "WATER_PH", 2.0),
    ("Conc.", "CONCENTRATION", 3.9),
    ("Capacità", "CAPACITY", 5.8),
]
ROW_STEP = 0.62
HEADER_Y = 2.7
FIRST_ROW_Y = HEADER_Y - 0.9
WINDOW = 8
BOTTOM_Y = FIRST_ROW_Y - (WINDOW - 1) * ROW_STEP
ROW_TIME = 0.3


def truncate(text: str, limit: int = 22) -> str:
    text = text or ""
    return text if len(text) <= limit else text[: limit - 1] + "…"


def format_capacity(value: str) -> str:
    try:
        return f"{float(value):.3g}"
    except (ValueError, TypeError):
        return value or ""


def make_row(row: dict[str, str], y: float, is_header: bool) -> VGroup:
    cells = []
    for header, key, x in COLUMNS:
        if is_header:
            content = header
        elif key == "CAPACITY":
            content = format_capacity(row[key])
        else:
            content = truncate(row[key])
        content = content or "—"
        cell = Text(
            content,
            font="Consolas",
            weight="BOLD" if is_header else "NORMAL",
            color=ACCENT if is_header else INK,
            font_size=22 if is_header else 20,
        )
        cell.move_to([x, y, 0])
        cells.append(cell)
    return VGroup(*cells)


class PDCCCarouselScene(Scene):
    def construct(self):
        with open(CSV_PATH, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))

        header = make_row({}, HEADER_Y, is_header=True)
        underline = Line(
            [-6.6, HEADER_Y - 0.35, 0], [6.6, HEADER_Y - 0.35, 0], color=ACCENT, stroke_width=3
        )
        self.play(FadeIn(header), FadeIn(underline), run_time=0.6)
        self.wait(0.4)

        visible: list[VGroup] = []
        for row in rows:
            if len(visible) < WINDOW:
                y = FIRST_ROW_Y - len(visible) * ROW_STEP
                new_row = make_row(row, y, is_header=False)
                self.play(FadeIn(new_row, shift=UP * 0.2), run_time=ROW_TIME)
                visible.append(new_row)
            else:
                new_row = make_row(row, BOTTOM_Y, is_header=False)
                oldest = visible.pop(0)
                self.play(
                    *[grp.animate.shift(UP * ROW_STEP) for grp in visible],
                    FadeIn(new_row, shift=UP * 0.2),
                    run_time=ROW_TIME,
                )
                self.remove(oldest)
                visible.append(new_row)
        self.wait(0.8)
