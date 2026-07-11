from pathlib import Path

from loguru import logger
from pptx import Presentation

from create_slides.DeckBuilding.AddUnisiSlideMethod import add_unisi_slide
from create_slides.DeckBuilding.ClearTemplateSlidesMethod import clear_template_slides
from create_slides.Slide import Slide
from create_slides.UnisiBackground import UnisiBackground


def build_single_slide_deck(
    slide: Slide, output_path: Path, background: UnisiBackground | None = None
) -> Path:
    if background is not None:
        prs = Presentation(str(background.template_path))
        clear_template_slides(prs)
    else:
        prs = Presentation()

    add_unisi_slide(prs, slide, background)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    prs.save(output_path)
    logger.info(f"Saved slide {slide.number} to {output_path}")
    return output_path
