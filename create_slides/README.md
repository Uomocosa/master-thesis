# create_slides

Thesis presentation tooling: a static slide deck (`python-pptx`) and math/data
animations (Manim Community Edition, used by 3blue1brown).

## Slides (pptx)

```
uv run python -m create_slides.build_deck
```

Outputs `output/thesis_slides.pptx` with one placeholder slide per thesis chapter.

## Discussion slides (per-slide scripts)

Each slide of the thesis discussion talk (see repo-root `DISCUSSION.md`) has its
own script under `src/create_slides/scripts/`, e.g. `create_slide_1.py`. Each
script hardcodes a `Slide(...)` literal (title, visual bullets, speech, todos)
transcribed from the matching `DISCUSSION.md` section, and writes one `.pptx`
file to the repo-root `SLIDES/` folder.

```
uv run create-slide-1
```

To add the next slide, copy an existing `create_slide_N.py`, edit the `Slide`
literal for the new section, bump `OUTPUT_PATH`'s filename, and register a
matching entry under `[project.scripts]` in `pyproject.toml`.

## Animations (manim)

```
uv run manim -pql src/create_slides/scenes/example.py ExampleScene
```

`-p` previews the render, `-ql` renders at low quality for fast iteration.
Rendered videos land in `media/`. Candidate animations to design next:
capacity-prediction fit across hyperparameter sweeps, AHC dendrogram build-up,
FMO HOMO/LUMO gap diagram, generative-model validity/novelty bar chart.
