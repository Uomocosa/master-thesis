from dataclasses import dataclass
from pathlib import Path

import numpy as np
from manim import (
    UL,
    DR,
    Dot,
    FadeIn,
    Group,
    ImageMobject,
    Scene,
    config,
)

config.background_color = "#FFFFFF"
# Wide, short frame matching the two figures side by side (minimal margin) so they
# render big; add_slide_movies places the movie at this real aspect ratio.
config.pixel_width = 1920
config.pixel_height = 700
config.frame_height = 8.0
config.frame_width = 8.0 * config.pixel_width / config.pixel_height

PAPERS_DIR = Path(__file__).resolve().parents[3] / "assets" / "papers"

# Curve trend-line colors, matched to each figure.
ORANGE = "#E8A33D"
NAVY = "#3B3B7A"
GRAY = "#B9B9C6"
LILAC = "#C9A9E0"
BLUE = "#2A2A8C"
CYAN = "#69C7E8"


@dataclass
class AxisCalib:
    """Maps data coordinates to fractions (0..1) of an image's bounding box."""

    x_min: float
    x_max: float
    y_min: float
    y_max: float
    left_frac: float  # image-width fraction where x == x_min
    right_frac: float  # image-width fraction where x == x_max
    bottom_frac: float  # image-height fraction (from top) where y == y_min
    top_frac: float  # image-height fraction (from top) where y == y_max


def data_to_scene(img: ImageMobject, calib: AxisCalib, x: float, y: float) -> np.ndarray:
    top_left = img.get_corner(UL)
    bottom_right = img.get_corner(DR)
    width = bottom_right[0] - top_left[0]
    height = top_left[1] - bottom_right[1]
    fx = calib.left_frac + (x - calib.x_min) / (calib.x_max - calib.x_min) * (
        calib.right_frac - calib.left_frac
    )
    fy = calib.bottom_frac + (y - calib.y_min) / (calib.y_max - calib.y_min) * (
        calib.top_frac - calib.bottom_frac
    )
    return np.array(
        [top_left[0] + fx * width, top_left[1] - fy * height, 0.0]
    )


def lele_interpolation(
    scene: Scene,
    to_scene,
    points: list[tuple[float, float]],
    origin: tuple[float, float],
    color: str,
) -> list[Dot]:
    """Add an interpolated point between each consecutive pair, then one at the origin."""
    dots: list[Dot] = []
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        mid = ((x0 + x1) / 2, (y0 + y1) / 2)
        dot = Dot(to_scene(*mid), radius=0.075, color=color, stroke_color="#1A1A2E", stroke_width=1)
        scene.play(FadeIn(dot, scale=1.6), run_time=0.28)
        dots.append(dot)
    origin_dot = Dot(
        to_scene(*origin), radius=0.075, color=color, stroke_color="#1A1A2E", stroke_width=1
    )
    scene.play(FadeIn(origin_dot, scale=1.6), run_time=0.28)
    dots.append(origin_dot)
    return dots


# Image 1: interpolated points must land ON each dashed trend line. The lines are
# straight through ~origin, so we sample points on y = slope*x; every midpoint then
# also lies on the line. Slopes read from each line's right endpoint at x=200.
_X1 = [10, 25, 50, 100, 200]
IMAGE1_CURVES = [
    ([(x, 0.276 * x) for x in _X1], ORANGE),  # Oestradiol, to (200, 55)
    ([(x, 0.185 * x) for x in _X1], NAVY),  # middle trend, to (200, 37)
    ([(x, 0.095 * x) for x in _X1], GRAY),  # Indomethacin, to (200, 19)
]

# Image 2: ignore the kinetic curves. Build a vertical interpolation at the last time
# point (~240 min) between the three plateau capacities (25/50/100 ppm), plus a point
# on the x-axis at y=0. One call → 2 midpoints + the (240, 0) point.
_T2 = 250
IMAGE2_PLATEAUS = [(_T2, 24), (_T2, 47), (_T2, 94)]
IMAGE2_ORIGIN = (_T2, 0)
IMAGE2_COLOR = "#B31939"

# Fractions measured from the source PNGs (axis lines + tick marks).
# img1 805x550: x=0 col131, x=250 col771, y=0 row470, y=70 row106
CALIB1 = AxisCalib(0, 250, 0, 70, 131 / 805, 771 / 805, 470 / 550, 106 / 550)
# img2 693x518: x=0 col116, x=250 col591, y=0 row449, y=100 row66
CALIB2 = AxisCalib(0, 250, 0, 100, 116 / 693, 591 / 693, 449 / 518, 66 / 518)


class InterpolationCurvesScene(Scene):
    def construct(self):
        img1 = ImageMobject(
            str(PAPERS_DIR / "oxazoline_capacity_indomethacin_oestradiol_ibuprofen.png")
        ).scale_to_fit_height(7.2)
        img2 = ImageMobject(
            str(PAPERS_DIR / "cryogel_cmegl_kinetics_piroxicam.png")
        ).scale_to_fit_height(img1.height)
        panels = Group(img1, img2).arrange(buff=0.8).move_to([0, 0, 0])

        self.play(FadeIn(panels), run_time=0.8)
        self.wait(0.4)

        for points, color in IMAGE1_CURVES:
            lele_interpolation(
                self, lambda x, y: data_to_scene(img1, CALIB1, x, y), points, (0, 0), color
            )
        lele_interpolation(
            self,
            lambda x, y: data_to_scene(img2, CALIB2, x, y),
            IMAGE2_PLATEAUS,
            IMAGE2_ORIGIN,
            IMAGE2_COLOR,
        )

        self.wait(1.6)
