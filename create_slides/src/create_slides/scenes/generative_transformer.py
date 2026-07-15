from pathlib import Path

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    FadeIn,
    FadeOut,
    Group,
    ImageMobject,
    RoundedRectangle,
    Scene,
    Text,
    VGroup,
    config,
)

config.background_color = "#FFFFFF"

ANIMATIONS_DIR = Path(__file__).resolve().parents[3] / "assets" / "animations"
POLYMERS_DIR = ANIMATIONS_DIR / "polymers"
INK = "#1A1A2E"
ACCENT = "#B31939"

# P-SMILES for polymer_01..06 (first rows of the aspirin valid_polymers table).
PSMILES = [
    "*CCCCCCCCCOC(=O)NCCOCCCCCCCNC(=O)OCCCCCOC(=O)O*",
    "*[Si](*)(Cl)CCCCCCOCCOc1ccc(/N=N/c2ccc(C)c([N+](=O)[O-])c2)cc1",
    "*/C=C/c1cc([N+](=O)[O-])c(C(C)(C)c2ccc(C(C)(C)c3ccc(C(*)=O)cc3)cc2)cc1-c1ccccc1",
    "*CCCCCOc1ccc(-c2ccc(OCCOCCOC(=O)c3ccc(C(=O)O*)cc3)cc2)cc1",
    "*C(=O)NNC(=O)c1ccccc1*",
    "*CCCCCCCCCCCCCCCCCCCCCOC(=O)CCNC(=O)c1ccc(C(=O)NCCCCCCNC(=O)c2ccc(*)cc2)cc1",
]
# Where each spawned candidate flies to (direction * distance).
TARGETS = [
    LEFT * 4.6 + UP * 2.0,
    RIGHT * 4.6 + UP * 2.1,
    LEFT * 5.0 + DOWN * 1.9,
    RIGHT * 5.0 + DOWN * 2.0,
    LEFT * 2.4 + UP * 2.6,
    RIGHT * 2.4 + DOWN * 2.7,
]


def truncate(text: str, limit: int = 26) -> str:
    return text if len(text) <= limit else text[: limit - 1] + "…"


def transformer() -> VGroup:
    blocks = VGroup(
        *[
            RoundedRectangle(
                corner_radius=0.08,
                width=1.9,
                height=0.42,
                stroke_color=INK,
                stroke_width=2,
                fill_color="#EDEDF2",
                fill_opacity=1,
            )
            for _ in range(4)
        ]
    ).arrange(DOWN, buff=0.16)
    shell = RoundedRectangle(
        corner_radius=0.18,
        width=2.7,
        height=blocks.height + 0.9,
        stroke_color=ACCENT,
        stroke_width=3,
    )
    label = Text("Transformer", font="Calibri", weight="BOLD", color=ACCENT, font_size=26)
    label.next_to(shell, UP, buff=0.18)
    sub = Text("(mingpt)", font="Calibri", color=INK, font_size=20)
    sub.next_to(shell, DOWN, buff=0.18)
    return VGroup(shell, blocks, label, sub)


def candidate(index: int) -> Group:
    image = ImageMobject(str(POLYMERS_DIR / f"polymer_0{index + 1}.png")).scale_to_fit_width(2.3)
    notation = Text(
        truncate(PSMILES[index]), font="Consolas", weight="BOLD", color=INK, font_size=16
    )
    notation.next_to(image, DOWN, buff=0.12)
    return Group(image, notation)


class GenerativeTransformerScene(Scene):
    def construct(self):
        model = transformer()
        model.move_to([0, 0, 0])
        self.play(FadeIn(model, scale=1.1), run_time=0.7)

        center = model.get_center()
        candidates = [candidate(i) for i in range(len(PSMILES))]
        for cycle, item in enumerate(candidates):
            # Inflate (working), then deflate and spawn a new candidate on the way down.
            self.play(model.animate.scale(1.15), run_time=0.35)
            item.move_to(TARGETS[cycle])
            self.play(
                model.animate.scale(1 / 1.15),
                FadeIn(item, shift=TARGETS[cycle] - center),
                run_time=0.55,
            )

        self.wait(1.2)
        # Candidates disappear one at a time.
        for item in candidates:
            self.play(FadeOut(item), run_time=0.3)
        self.play(FadeOut(model), run_time=0.4)
        self.wait(0.2)
