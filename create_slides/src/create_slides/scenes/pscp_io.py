from pathlib import Path

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    FadeIn,
    Group,
    ImageMobject,
    Line,
    RoundedRectangle,
    Scene,
    Text,
    VGroup,
    config,
)

config.background_color = "#FFFFFF"

ANIMATIONS_DIR = Path(__file__).resolve().parents[3] / "assets" / "animations"
INK = "#1A1A2E"
ACCENT = "#B31939"


def value_chip(label: str, value: str) -> VGroup:
    title = Text(label, font="Calibri", weight="BOLD", color=ACCENT, font_size=24)
    body = Text(value, font="Calibri", color=INK, font_size=22)
    body.next_to(title, DOWN, buff=0.12)
    text = VGroup(title, body)
    box = RoundedRectangle(
        corner_radius=0.14,
        width=max(text.width + 0.6, 3.0),
        height=text.height + 0.5,
        stroke_color=INK,
        stroke_width=2,
    )
    text.move_to(box.get_center())
    return VGroup(box, text)


def structure_chip(image_name: str, label: str, notation: str) -> Group:
    image = ImageMobject(str(ANIMATIONS_DIR / image_name)).scale_to_fit_width(1.9)
    name = Text(label, font="Calibri", weight="BOLD", color=ACCENT, font_size=22)
    name.next_to(image, DOWN, buff=0.1)
    smiles = Text(notation, font="Consolas", weight="BOLD", color=INK, font_size=15)
    smiles.next_to(name, DOWN, buff=0.06)
    return Group(image, name, smiles)


class PscpIoScene(Scene):
    def construct(self):
        molecule = structure_chip("molecule_aspirin.png", "SMILES", "CC(=O)OC1=CC=CC=C1C(=O)O")
        polymer = structure_chip("molecule_repeat_unit.png", "P-SMILES", "*CC(c1ccccc1)*")
        conc = value_chip("CONCENTRAZIONE", "12.5")
        ph = value_chip("pH", "8.2")

        structures = Group(molecule, polymer).arrange(DOWN, buff=0.5)
        chips = VGroup(conc, ph).arrange(DOWN, buff=0.5)
        inputs = Group(structures, chips).arrange(DOWN, buff=0.5).to_edge(LEFT, buff=0.7)

        pscp = RoundedRectangle(
            corner_radius=0.2, width=2.6, height=2.4, stroke_color=ACCENT, stroke_width=4
        )
        pscp_label = Text("PSCP", font="Calibri", weight="BOLD", color=ACCENT, font_size=40)
        pscp_label.move_to(pscp.get_center())
        model = VGroup(pscp, pscp_label).move_to([0.1, 0, 0])

        out_title = Text(
            "Capacità di\nadsorbimento",
            font="Calibri",
            weight="BOLD",
            color=ACCENT,
            font_size=26,
            line_spacing=0.6,
        )
        out_value = Text("≈ 25 mg/g", font="Calibri", weight="BOLD", color=INK, font_size=40)
        out_value.next_to(out_title, DOWN, buff=0.2)
        output = VGroup(out_title, out_value).to_edge(RIGHT, buff=0.9)

        # Leave a top/bottom margin so the movie doesn't crowd the bullets above.
        Group(inputs, model, output).scale(0.86).shift(DOWN * 0.2)

        for chip in (molecule, polymer, conc, ph):
            self.play(FadeIn(chip, shift=RIGHT * 0.4), run_time=0.35)
        self.play(FadeIn(model, scale=1.1), run_time=0.6)

        arrows = VGroup(
            *[
                Line(
                    chip.get_right() + RIGHT * 0.1,
                    pscp.get_left() + LEFT * 0.1,
                    stroke_color=ACCENT,
                    stroke_width=2.5,
                )
                for chip in (molecule, polymer, conc, ph)
            ]
        )
        self.play(FadeIn(arrows), run_time=0.6)

        out_arrow = Line(
            pscp.get_right() + RIGHT * 0.1,
            output.get_left() + LEFT * 0.1,
            stroke_color=ACCENT,
            stroke_width=3,
        )
        self.play(FadeIn(out_arrow), run_time=0.4)
        self.play(FadeIn(output, scale=1.3), run_time=0.6)
        self.wait(1.8)
