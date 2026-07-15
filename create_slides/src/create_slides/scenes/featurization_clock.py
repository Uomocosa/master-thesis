import math
from pathlib import Path

from manim import (
    DOWN,
    Arrow,
    FadeIn,
    FadeOut,
    Group,
    GrowArrow,
    ImageMobject,
    Scene,
    Text,
    config,
)

config.background_color = "#FFFFFF"

ANIMATIONS_DIR = Path(__file__).resolve().parents[3] / "assets" / "animations"
INK = "#1A1A2E"
ACCENT = "#B31939"

FEATURES = [
    "Peso Molecolare",
    "LogP",
    "TPSA",
    "Donatori H",
    "Accettori H",
    "Anelli Aromatici",
    "Legami Rotabili",
    "Frazione Csp3",
]
RING_X_RADIUS = 5.6
RING_Y_RADIUS = 3.4


def captioned_image(image_name: str, label: str, notation: str) -> Group:
    image = ImageMobject(str(ANIMATIONS_DIR / image_name)).scale_to_fit_width(3.4)
    name = Text(label, font="Calibri", weight="BOLD", color=ACCENT, font_size=24)
    name.next_to(image, DOWN, buff=0.18)
    smiles = Text(notation, font="Consolas", weight="BOLD", color=INK, font_size=22)
    smiles.next_to(name, DOWN, buff=0.08)
    return Group(image, name, smiles)


def clock_point(index: int, total: int) -> tuple[float, float]:
    angle = math.pi / 2 - 2 * math.pi * index / total
    return RING_X_RADIUS * math.cos(angle), RING_Y_RADIUS * math.sin(angle)


class FeaturizationClockScene(Scene):
    def construct(self):
        molecule = captioned_image(
            "molecule_aspirin.png", "SMILES", "CC(=O)OC1=CC=CC=C1C(=O)O"
        )
        polymer = captioned_image(
            "molecule_repeat_unit.png", "P-SMILES", "*CC(c1ccccc1)*"
        )
        center = Group(molecule, polymer).arrange(buff=0.8)
        center.move_to([0, 0, 0])
        self.play(FadeIn(center, scale=1.1), run_time=0.8)
        self.wait(0.4)

        for index, feature in enumerate(FEATURES):
            x, y = clock_point(index, len(FEATURES))
            start = [x * 0.42, y * 0.42, 0]
            end = [x * 0.82, y * 0.82, 0]
            arrow = Arrow(
                start,
                end,
                buff=0,
                stroke_color=ACCENT,
                stroke_width=4,
                max_tip_length_to_length_ratio=0.18,
            )
            label = Text(feature, font="Calibri", weight="BOLD", color=INK, font_size=30)
            label.move_to([x, y, 0])
            self.play(GrowArrow(arrow), run_time=0.45)
            self.play(FadeIn(label), FadeOut(arrow), run_time=0.5)

        self.wait(0.8)
        caption = Text(
            "→ vettore di feature numeriche",
            font="Calibri",
            weight="BOLD",
            color=ACCENT,
            font_size=30,
        )
        caption.next_to(center, DOWN, buff=0.55)
        self.play(FadeIn(caption, shift=DOWN * 0.2), run_time=0.6)
        self.wait(1.5)
