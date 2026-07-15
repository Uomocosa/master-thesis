"""Entry point: build the reveal.js web presentation from the edited pptx.

Renders the (hand-edited) `master-thesis-slides/Slide_Samuele_Maggiori.pptx` into a
static, self-contained site under `master-thesis-slides/docs/`, ready for GitHub Pages.
"""

from pathlib import Path

from create_slides.WebExport import build_web_export

CREATE_SLIDES_DIR = Path(__file__).resolve().parents[3]
RENDER_PS1 = CREATE_SLIDES_DIR / "tools" / "render_pptx.ps1"
REVEAL_SRC = CREATE_SLIDES_DIR / "assets" / "reveal"

# The slides repo sits next to master-thesis on disk.
SLIDES_REPO = CREATE_SLIDES_DIR.parents[1] / "master-thesis-slides"
PPTX_PATH = SLIDES_REPO / "Slide_Samuele_Maggiori.pptx"
OUT_DIR = SLIDES_REPO / "docs"


def main() -> None:
    build_web_export(PPTX_PATH, OUT_DIR, RENDER_PS1, REVEAL_SRC)


if __name__ == "__main__":
    main()
