from dataclasses import dataclass
from pathlib import Path

from create_slides.UnisiLineTitleSeparation import UnisiLineTitleSeparation

CREATE_SLIDES_DIR = Path(__file__).resolve().parents[3]
ASSETS_DIR = CREATE_SLIDES_DIR / "assets" / "unisi"


@dataclass
class UnisiBackground:
    template_path: Path
    logo_image: Path
    logo_position: tuple[int, int]
    logo_size: tuple[int, int]
    line_separator: UnisiLineTitleSeparation
    title_position: tuple[int, int]
    title_size: tuple[int, int]
    body_position: tuple[int, int]
    body_size: tuple[int, int]
    banner_image: Path | None = None
    banner_position: tuple[int, int] | None = None
    banner_size: tuple[int, int] | None = None


# Reference: unisi_skyline.pptx slide 1 (opening/title slide) — big banner + big
# logo + long divider, paired with UnisiCenterTitle / UnisiSubtitle.
UNISI_TITLE_SLIDE = UnisiBackground(
    template_path=CREATE_SLIDES_DIR / "unisi_skyline.pptx",
    banner_image=ASSETS_DIR / "skyline_banner.png",
    banner_position=(0, 2105025),
    banner_size=(12192000, 4745038),
    logo_image=ASSETS_DIR / "logo.png",
    logo_position=(588963, 676275),
    logo_size=(1870075, 1927225),
    line_separator=UnisiLineTitleSeparation(position=(2663825, 479425), length=2374900),
    title_position=(3111500, 773113),
    title_size=(7081838, 1755775),
    body_position=(3092450, 2790825),
    body_size=(5537200, 849313),
)

# Reference: unisi_skyline.pptx slides 2-8 (content slides) — no banner, small
# logo top-left, short divider, text boxes right next to it, paired with
# UnisiTitle / UnisiText.
UNISI_CONTENT_SLIDE = UnisiBackground(
    template_path=CREATE_SLIDES_DIR / "unisi_skyline.pptx",
    logo_image=ASSETS_DIR / "logo_small.png",
    logo_position=(449263, 412750),
    logo_size=(1127125, 1162050),
    line_separator=UnisiLineTitleSeparation(position=(1730375, 331788), length=1323975),
    title_position=(2019300, 542925),
    title_size=(6934200, 954088),
    body_position=(1739900, 1971675),
    body_size=(9394825, 4000500),
)
