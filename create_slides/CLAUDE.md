# create_slides

uv package that builds the thesis discussion deck (`SLIDES/*.pptx`) with
`python-pptx`, styled after the UniSi reference deck `unisi_skyline.pptx`.

## Package structure convention

Every reusable concept gets its own PascalCase folder under
`src/create_slides/`, one class or function per folder:

- Class concept: `Foo/foo.py` defining `class Foo`, plus `Foo/__init__.py`
  doing `from create_slides.Foo.foo import Foo` + `__all__ = ["Foo"]`.
- Function/"Method" concept: nested under a noun-phrase category, e.g.
  `DeckBuilding/BuildSingleSlideDeckMethod/build_single_slide_deck.py`. The
  outer category's `__init__.py` re-exports every method in it so callers do
  `from create_slides.DeckBuilding import build_single_slide_deck` without
  knowing about the nested `*Method` folder.
- `scripts/create_all_slides.py` (`create-all-slides`) is the **main entry**:
  it holds all 22 discussion slides as `Slide` literals (transcribed from
  repo-root `DISCUSSION.md`) and builds the whole deck to
  `SLIDES/thesis_discussion_deck.pptx` via `build_full_deck`. Edit slide
  content here.
- `scripts/create_slide_N.py` are single-slide scripts (e.g. `create-slide-1`)
  kept for iterating on one slide in isolation; each is a `[project.scripts]`
  entry in `pyproject.toml`.
- `build_full_deck` (`DeckBuilding/BuildFullDeckMethod/`) takes
  `list[tuple[Slide, UnisiBackground | None]]` and calls `add_unisi_slide`
  per slide; `build_single_slide_deck` wraps `add_unisi_slide` for one slide.
  All per-slide construction lives in `add_unisi_slide`
  (`DeckBuilding/AddUnisiSlideMethod/`) — edit layout there, not in the two
  build wrappers.

Follow this pattern for any new concept — don't add loose files to the
package root.

## The UniSi visual system

`unisi_skyline.pptx` (root of this folder) is a converted copy of a real
UniSi presentation (`Presentazione_panoramico_skyline.ppt`, provided by the
user) and is the template/basis every generated deck is built from —
`build_single_slide_deck` opens `Presentation(background.template_path)`
and strips its 8 original slides (`clear_template_slides`) to inherit its
slide master, widescreen size (12192000×6858000 EMU), and theme fonts
(Calibri Light/Calibri) without carrying its content.

The reference deck has two distinct visual layouts, each with its own
background preset and matching text styles — **don't mix them**:

| | `UNISI_TITLE_SLIDE` | `UNISI_CONTENT_SLIDE` |
|---|---|---|
| Reference | slide 1 (opening) | slides 2-8 (content) |
| Banner | full skyline photo | none |
| Logo | big (`assets/unisi/logo.png`) | small (`assets/unisi/logo_small.png`) |
| Title style | `UnisiCenterTitle` (Optima 54, non-bold) | `UnisiTitle` (Optima 28, caps, non-bold) |
| Subtitle/body style | `UnisiSubtitle` (Optima 24, red, bold) | `UnisiText.level(1/2/3)` (Optima 28/24/20) |

All EMU positions in `UnisiBackground` (`UnisiBackground/unisi_background.py`)
were read directly out of `unisi_skyline.pptx`'s slide XML (via
`unzip unisi_skyline.pptx` + reading `ppt/slides/slideN.xml` — no GUI tool
was used or is needed). If you need to adjust a position, re-derive it the
same way rather than eyeballing it, and keep title/body boxes positioned
relative to the logo/divider like the reference does (they are **not** at
python-pptx's generic layout-placeholder position — `build_single_slide_deck`
explicitly repositions them from `background.title_position` /
`background.body_position`).

`UnisiLineTitleSeparation` is the vertical divider line between the logo and
the title text; `apply_unisi_background` (`DeckBuilding/ApplyUnisiBackgroundMethod/`)
draws it as a real connector shape, not an image.

`apply_unisi_text_style` (`DeckBuilding/ApplyUnisiTextStyleMethod/`) applies
any of the five style dataclasses (font/size/bold/color/caps) to a
paragraph's runs — it's the only place that touches `run.font`.

## Images on slides

`Slide.images` (list of `Path`) embeds real picture shapes. When a slide has
images, `add_unisi_slide` uses a **two-column layout**: bullets take the left
~half of the body, images fill the right column. `add_slide_images`
(`DeckBuilding/AddSlideImagesMethod/`) fits them into their area centered as a
group — a row for wide areas, a column for tall areas, always
aspect-preserved. It reads pixel dimensions via
`pptx.parts.image.Image.from_file` — no PIL dependency.

Curated paper figures live in `assets/papers/`, cataloged in
`assets/papers/paper_mapping.json` — each entry has `paper_title`,
`paper_pdf` (path into the Obsidian vault), `paper_description`, and per
image a repo `path` + `image_description` (including which figures are
presentation-friendly vs technical/supporting). **Check the mapping first**
when a slide needs a figure; only go back to the Obsidian vault for
something not already cataloged.

The banner/background is a per-slide choice: each `create_slide_N.py` picks
its own preset (`UNISI_CONTENT_SLIDE`, `UNISI_TITLE_SLIDE`, or `None`) —
there is deliberately no global default.

## Known gaps

- `UnisiCenterTitle` / `UnisiSubtitle` are defined but not wired into any
  script yet — nothing currently builds an actual UniSi-style opening title
  slide (`UNISI_TITLE_SLIDE` background exists and is ready for one).
- Slide 1 still needs a generic contaminated-wastewater photo and a
  schematic polymer-sponge diagram (not found in the Obsidian vault).

## Regenerating a slide

```
cd create_slides
uv run create-slide-1
```

Close the target `.pptx` in PowerPoint first — python-pptx cannot overwrite
a file that's open (you'll get a `PermissionError`).

## Seeing what a slide looks like (ALWAYS do this after generating)

`tools/render_pptx.ps1` renders every slide of a `.pptx` to PNG via
PowerPoint COM automation (PowerPoint is installed on this machine; no
LibreOffice needed):

```powershell
& create_slides/tools/render_pptx.ps1 -PptxPath SLIDES/thesis_discussion_deck.pptx
```

PNGs land in `SLIDES/renders/<name>_slideNN.png`. After any slide change,
regenerate → render → **look at the PNG** (Read tool) and iterate on the
layout — don't judge a slide from the XML alone. Note the renders are cached
by filename; always re-run the render script after rebuilding before reading.
