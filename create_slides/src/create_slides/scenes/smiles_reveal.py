from pathlib import Path

from manim import (
    DOWN,
    UP,
    FadeIn,
    FadeTransform,
    ImageMobject,
    Scene,
    Text,
    config,
)

config.background_color = "#FFFFFF"

ANIMATIONS_DIR = Path(__file__).resolve().parents[3] / "assets" / "animations"
INK = "#1A1A2E"
ACCENT = "#B31939"


def reveal(scene: Scene, image_name: str, label: str, notation: str) -> None:
    title = Text(label, font="Calibri", weight="BOLD", color=ACCENT, font_size=52)
    title.to_edge(UP, buff=0.8)
    scene.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

    molecule = ImageMobject(str(ANIMATIONS_DIR / image_name)).scale_to_fit_width(9)
    molecule.move_to([0, -0.3, 0])
    scene.play(FadeIn(molecule, scale=1.1), run_time=0.8)
    scene.wait(1.2)

    notation_text = Text(notation, font="Consolas", weight="BOLD", color=INK, font_size=34)
    notation_text.scale_to_fit_width(min(11.5, len(notation) * 0.32))
    notation_text.move_to([0, -0.3, 0])
    scene.play(FadeTransform(molecule, notation_text), run_time=1.2)
    # Hold the final frame: the video must end on the notation, not fade to blank.
    scene.wait(1.4)


class SmilesRevealScene(Scene):
    def construct(self):
        reveal(
            self,
            "molecule_aspirin.png",
            "SMILES",
            "CC(=O)OC1=CC=CC=C1C(=O)O",
        )


class PsmilesRevealScene(Scene):
    def construct(self):
        reveal(
            self,
            "molecule_repeat_unit.png",
            "P-SMILES",
            "*CC(c1ccccc1)*",
        )
