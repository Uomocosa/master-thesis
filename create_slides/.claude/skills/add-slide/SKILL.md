---
name: add-slide
description: >
  Add a new UniSi-styled slide to the create_slides/ thesis deck. Use when
  the user asks to create, add, or regenerate a slide for the thesis
  discussion presentation, or references DISCUSSION.md sections that need
  turning into a slide. Scoped to the create_slides/ package in this repo.
---

Read `create_slides/CLAUDE.md` first for the package's atomic-folder
convention and the UniSi visual-system rules — don't skip it, this skill
assumes it.

## Steps to add / edit a slide

The whole 22-slide deck lives in
`create_slides/src/create_slides/scripts/create_all_slides.py` as a list of
`Slide` literals, built to `SLIDES/thesis_discussion_deck.pptx` by
`create-all-slides`. To add or change a slide, edit that list — don't make a
new per-slide script unless you specifically want to iterate on one slide in
isolation.

1. Find the slide's content in repo-root `DISCUSSION.md` (blocks marked
   `_**POWERPOINT SLIDE**_` / `_**SPEACH**_`) — that's the authoritative
   source, not a guess. Keep bullets short; put the full narration in
   `speech` and open questions in `todos`.
2. Add/edit the `Slide(...)` entry in `create_all_slides.py`. (A standalone
   `create_slide_<N>.py` + `[project.scripts]` entry is only for isolated
   single-slide iteration.)
3. Pick the right background:
   - A regular content slide (title + bullets, the common case) →
     `UNISI_CONTENT_SLIDE`.
   - An actual opening/section title slide → `UNISI_TITLE_SLIDE` (not yet
     wired into any script — you'll be the first; use `UnisiCenterTitle`
     for the title and `UnisiSubtitle` for the subtitle, matching how
     `build_single_slide_deck` applies `UnisiTitle`/`UnisiText` for content
     slides).
4. Run `uv run create-all-slides` from inside `create_slides/`. If it fails
   with `PermissionError`, the target `.pptx` is open in PowerPoint — ask
   the user to close it.
5. Render the result to PNG and LOOK at it:
   `& create_slides/tools/render_pptx.ps1 -PptxPath SLIDES/thesis_discussion_deck.pptx`
   writes `SLIDES/renders/<name>_slideNN.png` (PowerPoint COM). Renders are
   cached by filename, so always re-run the render after rebuilding. Read the
   PNGs and iterate on layout until clean — never judge a slide from a clean
   exit code or the XML alone.

## Adding images to a slide

Set `Slide(images=[...])` with paths to files under
`create_slides/assets/papers/` — `build_single_slide_deck` places them as
real picture shapes, side by side in the lower half of the body area
(bullets keep the top half).

To pick figures, read `create_slides/assets/papers/paper_mapping.json`
FIRST — it catalogs every extracted paper figure with a `paper_description`
and per-image `image_description` (flagging which are presentation-friendly
vs technical/supporting). Only if nothing there fits, go hunting in
`C:\Users\SamueleMaggiori\[Tesi] (Obsidian Vault)`: it has per-paper
`Paper • <title> • ChatGPT Analysis.md` summaries and `Graph N • <title>.md`
notes linking to already-cropped figure screenshots
(`Immagine YYYY-MM-DD HHMMSS.png`) — legitimate paper-figure crops, not
stock photos. Copy anything you use into `create_slides/assets/papers/`
with a descriptive filename and add it to `paper_mapping.json`.

To pull figures straight out of a paper PDF (the vault screenshots don't
cover everything — e.g. the dual-sponge photo was only in the PDF), extract
embedded images with PyMuPDF, no install needed:
`uv run --with pymupdf python <script>` opening the PDF via `fitz.open` and
saving each `page.get_images(full=True)` xref as PNG (skip images smaller
than ~150px; they're icons/logos). Then view the PNGs to pick the good ones.
