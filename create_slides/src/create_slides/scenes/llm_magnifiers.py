from manim import (
    DOWN,
    RIGHT,
    UP,
    Circle,
    FadeIn,
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
LLMS = ["Gemma", "DeepSeek", "Kimi", "Claude Opus"]


def paper_row(width: float = 3.4) -> VGroup:
    body = RoundedRectangle(
        corner_radius=0.06,
        width=width,
        height=0.66,
        stroke_color=INK,
        stroke_width=2,
        fill_color="#FFFFFF",
        fill_opacity=1,
    )
    lines = VGroup(
        *[
            Line(
                body.get_left() + RIGHT * 0.2 + UP * (0.16 - 0.16 * i),
                body.get_right() + RIGHT * (-0.2 - 0.5 * i) + UP * (0.16 - 0.16 * i),
                stroke_color="#9A9AA8",
                stroke_width=2,
            )
            for i in range(3)
        ]
    )
    return VGroup(body, lines)


def magnifier(label: str) -> VGroup:
    lens = Circle(radius=0.34, stroke_color=ACCENT, stroke_width=5, fill_color="#F6EDEF", fill_opacity=0.55)
    handle = Line(
        lens.get_center() + [0.24, -0.24, 0],
        lens.get_center() + [0.55, -0.55, 0],
        stroke_color=ACCENT,
        stroke_width=6,
    )
    name = Text(label, font="Calibri", weight="BOLD", color=INK, font_size=18)
    name.next_to(lens, UP, buff=0.12)
    return VGroup(lens, handle, name)


class LlmMagnifiersScene(Scene):
    def construct(self):
        papers = VGroup(*[paper_row() for _ in range(6)]).arrange(DOWN, buff=0.26)
        papers.scale(0.82).move_to([2.1, -0.7, 0])
        self.play(FadeIn(papers, shift=UP * 0.3), run_time=0.7)

        glasses = [magnifier(name) for name in LLMS]
        starts = [
            papers.get_left() + [-3.2, 1.7, 0],
            papers.get_left() + [-2.0, 0.6, 0],
            papers.get_left() + [-3.2, -0.6, 0],
            papers.get_left() + [-2.0, -1.7, 0],
        ]
        for glass, start in zip(glasses, starts):
            glass.move_to(start)
            self.play(FadeIn(glass, scale=1.2), run_time=0.3)

        # Scan: each magnifier drifts across the paper rows a couple of times.
        rows = [papers[i].get_center() for i in range(len(papers))]
        for step in range(3):
            anims = []
            for j, glass in enumerate(glasses):
                target_row = rows[(step * 2 + j) % len(rows)]
                offset = [(-1.0 if (j + step) % 2 else -2.2), 0, 0]
                anims.append(glass.animate.move_to([target_row[0] + offset[0], target_row[1], 0]))
            self.play(*anims, run_time=0.9)
            self.wait(0.4)
        self.wait(0.8)
