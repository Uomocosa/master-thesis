from manim import (
    DOWN,
    LEFT,
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
EDGE_GRAY = "#C4C4D0"

INPUTS = ["SMILES", "P-SMILES", "Concentrazione", "pH"]
HIDDEN = [16, 8, 4, 4, 4]


def node_column(count: int, x: float, cap: int = 8) -> VGroup:
    drawn = min(count, cap)
    nodes = VGroup(
        *[
            Circle(radius=0.1, stroke_color=INK, stroke_width=2, fill_color="#FFFFFF", fill_opacity=1)
            for _ in range(drawn)
        ]
    ).arrange(DOWN, buff=0.16)
    nodes.move_to([x, 0, 0])
    return nodes


class PscpSchematicScene(Scene):
    def construct(self):
        title = Text(
            "PSCP — PSmileCapacityPredictor",
            font="Calibri",
            weight="BOLD",
            color=ACCENT,
            font_size=34,
        )
        title.to_edge(UP, buff=0.6)

        # Input feature chips on the left.
        chips = VGroup(
            *[
                VGroup(
                    RoundedRectangle(
                        corner_radius=0.1, width=2.9, height=0.7, stroke_color=INK, stroke_width=2
                    ),
                    Text(name, font="Calibri", weight="BOLD", color=INK, font_size=22),
                )
                for name in INPUTS
            ]
        )
        for chip in chips:
            chip[1].move_to(chip[0].get_center())
        chips.arrange(DOWN, buff=0.35).to_edge(LEFT, buff=0.8)

        # Hidden layers as node columns.
        columns = VGroup(*[node_column(size, i * 1.0) for i, size in enumerate(HIDDEN)])
        columns.move_to([1.2, 0, 0])
        edges = VGroup(
            *[
                Line(a.get_center(), b.get_center(), stroke_color=EDGE_GRAY, stroke_width=1)
                for left, right in zip(columns, columns[1:])
                for a in left
                for b in right
            ]
        )
        network = VGroup(edges, columns)

        # Output capacity node on the right.
        out_node = Circle(radius=0.22, stroke_color=ACCENT, stroke_width=3, fill_color="#FFFFFF", fill_opacity=1)
        out_label = Text("Capacità", font="Calibri", weight="BOLD", color=ACCENT, font_size=24)
        out_node.next_to(columns, RIGHT, buff=1.0)
        out_label.next_to(out_node, DOWN, buff=0.2)
        output = VGroup(out_node, out_label)

        in_arrows = VGroup(
            *[
                Line(
                    chip[0].get_right() + RIGHT * 0.1,
                    columns[0].get_left() + LEFT * 0.1,
                    stroke_color=ACCENT,
                    stroke_width=2,
                )
                for chip in chips
            ]
        )
        out_arrow = Line(
            columns[-1].get_right() + RIGHT * 0.1,
            out_node.get_left() + LEFT * 0.1,
            stroke_color=ACCENT,
            stroke_width=2.5,
        )

        self.play(FadeIn(title), FadeIn(chips), run_time=0.6)
        self.play(FadeIn(network), FadeIn(in_arrows), run_time=0.7)
        self.play(FadeIn(out_arrow), FadeIn(output, scale=1.2), run_time=0.6)
        self.wait(1.5)
