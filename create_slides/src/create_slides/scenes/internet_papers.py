import math

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Circle,
    Ellipse,
    FadeIn,
    FadeOut,
    Line,
    RoundedRectangle,
    Scene,
    Text,
    VGroup,
    config,
)

config.background_color = "#FFFFFF"

INK = "#1A1A2E"
ACCENT = "#B31939"
PAPER_COUNT = 14


def paper_icon(scale: float = 1.0) -> VGroup:
    body = RoundedRectangle(
        corner_radius=0.05,
        width=0.7,
        height=0.92,
        stroke_color=INK,
        stroke_width=2,
        fill_color="#FFFFFF",
        fill_opacity=1,
    )
    lines = VGroup(
        *[
            Line(
                body.get_left() + RIGHT * 0.12 + UP * (0.28 - 0.16 * i),
                body.get_right() + LEFT * 0.12 + UP * (0.28 - 0.16 * i),
                stroke_color="#9A9AA8",
                stroke_width=2,
            )
            for i in range(4)
        ]
    )
    return VGroup(body, lines).scale(scale)


def globe() -> VGroup:
    outline = Circle(radius=1.15, stroke_color=ACCENT, stroke_width=3, fill_color="#F6EDEF", fill_opacity=1)
    meridians = VGroup(
        Line(UP * 1.15, DOWN * 1.15, stroke_color=ACCENT, stroke_width=1.5),
        Ellipse(width=1.1, height=2.3, stroke_color=ACCENT, stroke_width=1.5),
        Ellipse(width=2.1, height=2.3, stroke_color=ACCENT, stroke_width=1.5),
    )
    parallels = VGroup(
        Line(LEFT * 1.15, RIGHT * 1.15, stroke_color=ACCENT, stroke_width=1.5),
        Line(LEFT * 0.95 + UP * 0.62, RIGHT * 0.95 + UP * 0.62, stroke_color=ACCENT, stroke_width=1.5),
        Line(LEFT * 0.95 + DOWN * 0.62, RIGHT * 0.95 + DOWN * 0.62, stroke_color=ACCENT, stroke_width=1.5),
    )
    return VGroup(outline, meridians, parallels)


class InternetPapersScene(Scene):
    def construct(self):
        source = globe()
        label = Text("OpenAlex", font="Calibri", weight="BOLD", color=ACCENT, font_size=28)
        label.next_to(source, DOWN, buff=0.25)
        internet = VGroup(source, label).move_to([0, 0, 0])
        self.play(FadeIn(internet, scale=1.1), run_time=0.7)
        self.wait(0.3)

        papers = []
        for i in range(PAPER_COUNT):
            angle = 2 * math.pi * i / PAPER_COUNT + 0.2
            radius = 3.9 if i % 2 == 0 else 3.0
            target = np.array([radius * math.cos(angle), radius * math.sin(angle) * 0.72, 0.0])
            paper = paper_icon(0.9).move_to(target)
            papers.append(paper)
            self.play(FadeIn(paper, shift=target * 0.4), run_time=0.18)

        self.wait(1.2)
        for paper in papers:
            self.play(FadeOut(paper), run_time=0.12)
        self.wait(0.3)
