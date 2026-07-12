from pathlib import Path

from manim import (
    DOWN,
    UP,
    AnimationGroup,
    FadeIn,
    FadeOut,
    ImageMobject,
    Scene,
    config,
)

config.background_color = "#FFFFFF"

POLYMERS_DIR = Path(__file__).resolve().parents[3] / "assets" / "animations" / "polymers"
SHIFT = DOWN * 9
HOLD_SECONDS = 0.9
SLIDE_SECONDS = 0.8


class PolymerCarouselScene(Scene):
    def construct(self):
        images = [
            ImageMobject(str(path)).scale_to_fit_width(12)
            for path in sorted(POLYMERS_DIR.glob("polymer_*.png"))
        ]
        current = images[0]
        self.play(FadeIn(current, shift=SHIFT), run_time=SLIDE_SECONDS)
        self.wait(HOLD_SECONDS)
        for incoming in images[1:]:
            incoming.shift(-SHIFT)
            self.play(
                AnimationGroup(
                    current.animate.shift(SHIFT),
                    incoming.animate.shift(SHIFT),
                ),
                run_time=SLIDE_SECONDS,
            )
            self.remove(current)
            current = incoming
            self.wait(HOLD_SECONDS)
        self.play(FadeOut(current), run_time=0.5)
        self.wait(0.3)
