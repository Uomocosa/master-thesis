# create_slides

Thesis presentation tooling: a static slide deck (`python-pptx`) and math/data
animations (Manim Community Edition, used by 3blue1brown).

## Slides (pptx)

```
uv run python -m create_slides.build_deck
```

Outputs `output/thesis_slides.pptx` with one placeholder slide per thesis chapter.

## Animations (manim)

```
uv run manim -pql src/create_slides/scenes/example.py ExampleScene
```

`-p` previews the render, `-ql` renders at low quality for fast iteration.
Rendered videos land in `media/`. Candidate animations to design next:
capacity-prediction fit across hyperparameter sweeps, AHC dendrogram build-up,
FMO HOMO/LUMO gap diagram, generative-model validity/novelty bar chart.
