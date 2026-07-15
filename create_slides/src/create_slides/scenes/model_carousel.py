from manim import (
    DOWN,
    RIGHT,
    UP,
    Circle,
    Create,
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
EDGE_GRAY = "#C4C4D0"

# Representative subset of RESULTS/mlp_experiments/q2_leaderboard.md, ascending to the
# finalized model (last). (label, hidden-layer sizes, Q2)
MODELS = [
    ("experiment_default", [8, 8], 0.460),
    ("hd_16_16_16", [16, 16, 16], 0.888),
    ("hd_8_8_8_8", [8, 8, 8, 8], 0.894),
    ("hd_16_8_8_8", [16, 8, 8, 8], 0.913),
    ("hd_16_8_4_4_4_mae", [16, 8, 4, 4, 4], 0.972),
    ("hd_16_8_4_4_4", [16, 8, 4, 4, 4], 0.984),  # finalized
]
CENTER_Y = 0.2
ENTER_Y = -3.2


def network(sizes: list[int]) -> VGroup:
    # Cap drawn nodes so tall layers stay compact; edges between adjacent columns.
    layers = []
    for i, size in enumerate(sizes):
        drawn = min(size, 8)
        nodes = VGroup(
            *[
                Circle(radius=0.07, stroke_color=INK, stroke_width=2, fill_color="#FFFFFF", fill_opacity=1)
                for _ in range(drawn)
            ]
        ).arrange(DOWN, buff=0.12)
        nodes.move_to(RIGHT * i * 0.75)
        layers.append(nodes)
    edges = VGroup(
        *[
            Line(a.get_center(), b.get_center(), stroke_color=EDGE_GRAY, stroke_width=1)
            for left, right in zip(layers, layers[1:])
            for a in left
            for b in right
        ]
    )
    return VGroup(edges, *layers)


def entry(label: str, sizes: list[int], q2: float) -> VGroup:
    net = network(sizes)
    name = Text(label, font="Consolas", weight="BOLD", color=INK, font_size=24)
    score = Text(f"Q2 = {q2:.3f}", font="Consolas", weight="BOLD", color=INK, font_size=26)
    text = VGroup(name, score).arrange(DOWN, buff=0.22)
    text.next_to(net, RIGHT, buff=0.7)
    return VGroup(net, text)


class ModelCarouselScene(Scene):
    def construct(self):
        current = None
        for i, (label, sizes, q2) in enumerate(MODELS):
            item = entry(label, sizes, q2)
            is_last = i == len(MODELS) - 1
            if current is None:
                item.move_to([0, CENTER_Y, 0])
                self.play(FadeIn(item, shift=UP * 0.4), run_time=0.5)
            else:
                item.move_to([0, ENTER_Y, 0])
                self.play(
                    FadeOut(current, shift=UP * 3.4),
                    item.animate.move_to([0, CENTER_Y, 0]),
                    run_time=0.55,
                )
                self.remove(current)
            current = item
            self.wait(1.0 if is_last else 0.55)

        # Highlight the finalized model's Q2.
        score = current[1][1]
        box = RoundedRectangle(
            corner_radius=0.12,
            width=score.width + 0.5,
            height=score.height + 0.35,
            stroke_color=ACCENT,
            stroke_width=4,
        ).move_to(score.get_center())
        self.play(score.animate.set_color(ACCENT).scale(1.25), Create(box), run_time=0.7)
        self.wait(1.6)
