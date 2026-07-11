from manim import BLUE, FadeIn, FadeOut, Scene, Text


class ExampleScene(Scene):
    def construct(self):
        title = Text("Polymer Discovery Pipeline", color=BLUE)
        self.play(FadeIn(title))
        self.wait(1)
        self.play(FadeOut(title))
