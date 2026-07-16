from manim import (
    DOWN,
    LEFT,
    RIGHT,
    Circle,
    Create,
    FadeIn,
    Line,
    RoundedRectangle,
    Scene,
    ShowPassingFlash,
    Text,
    VGroup,
    config,
)

config.background_color = "#FFFFFF"

INK = "#1A1A2E"
ACCENT = "#B31939"
EDGE_GRAY = "#B8B8C4"

INPUTS = [
    ("SMILES", "CC(=O)OC1=CC=CC=C1C(=O)O"),
    ("PSMILES", "*CCCCCOc1ccc(...)C(=O)O*"),
    ("CONCENTRAZIONE", "12.5"),
    ("PH", "8.2"),
]
LAYER_SIZES = [4, 6, 6, 3]


def input_chip(label: str, value: str) -> VGroup:
    title = Text(label, font="Calibri", weight="BOLD", color=ACCENT, font_size=26)
    body = Text(value, font="Calibri", color=INK, font_size=20)
    body.next_to(title, DOWN, buff=0.12)
    text = VGroup(title, body)
    box = RoundedRectangle(
        corner_radius=0.15,
        width=max(text.width + 0.5, 3.4),
        height=text.height + 0.45,
        stroke_color=INK,
        stroke_width=2,
    )
    text.move_to(box.get_center())
    return VGroup(box, text)


def build_network() -> tuple[VGroup, list[VGroup], list[VGroup]]:
    layers: list[VGroup] = []
    for i, size in enumerate(LAYER_SIZES):
        nodes = VGroup(
            *[
                Circle(radius=0.16, stroke_color=INK, stroke_width=2.5, fill_color="#FFFFFF", fill_opacity=1)
                for _ in range(size)
            ]
        )
        nodes.arrange(DOWN, buff=0.45)
        nodes.move_to(RIGHT * (i * 1.9))
        layers.append(nodes)
    edge_groups: list[VGroup] = []
    for left_layer, right_layer in zip(layers, layers[1:]):
        edges = VGroup(
            *[
                Line(a.get_center(), b.get_center(), stroke_color=EDGE_GRAY, stroke_width=1.5)
                for a in left_layer
                for b in right_layer
            ]
        )
        edge_groups.append(edges)
    network = VGroup(*edge_groups, *layers)
    return network, layers, edge_groups


class PredictionPipelineScene(Scene):
    def construct(self):
        chips = VGroup(*[input_chip(label, value) for label, value in INPUTS])
        chips.arrange(DOWN, buff=0.4)
        chips.to_edge(LEFT, buff=0.6)

        network, layers, edge_groups = build_network()
        network.move_to(RIGHT * 1.2)

        for chip in chips:
            self.play(FadeIn(chip, shift=RIGHT * 0.5), run_time=0.45)
        self.wait(0.3)

        self.play(Create(network), run_time=1.2)

        arrows = VGroup(
            *[
                Line(
                    chip.get_right(),
                    node.get_left(),
                    stroke_color=ACCENT,
                    stroke_width=2.5,
                )
                for chip, node in zip(chips, layers[0])
            ]
        )
        self.play(Create(arrows), run_time=0.7)

        for edges in edge_groups:
            flash = edges.copy().set_stroke(color=ACCENT, width=4)
            self.play(
                ShowPassingFlash(flash, time_width=0.6),
                run_time=0.9,
            )

        output_title = Text("CAPACITÀ", font="Calibri", weight="BOLD", color=ACCENT, font_size=30)
        output_value = Text("0.40", font="Calibri", weight="BOLD", color=INK, font_size=48)
        output_value.next_to(output_title, DOWN, buff=0.15)
        output = VGroup(output_title, output_value)
        output.next_to(layers[-1], RIGHT, buff=0.9)

        output_arrow = Line(
            layers[-1].get_right() + RIGHT * 0.1,
            output.get_left() + LEFT * 0.1,
            stroke_color=ACCENT,
            stroke_width=3,
        )
        self.play(Create(output_arrow), run_time=0.4)
        self.play(FadeIn(output, scale=1.4), run_time=0.6)
        # Hold the final frame: the video must end on the full pipeline, not fade to blank.
        self.wait(1.2)
