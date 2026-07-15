from dataclasses import dataclass, field
from pathlib import Path

from create_slides.Movie import Movie


@dataclass
class Slide:
    number: int
    title: str
    visual_bullets: list[str]
    speech: str
    todos: list[str] = field(default_factory=list)
    images: list[Path] = field(default_factory=list)
    # Stacked layout: full-width bullets on top, images below (instead of the
    # default two-column bullets-left / images-right layout).
    images_below: bool = False
    movies: list[Movie] = field(default_factory=list)
    # Draw the faint Siena skyline band behind the content (UNISI_CONTENT_SLIDE_SKYLINE).
    skyline: bool = False
    # Keep the slide in the .pptx but hide it from slideshow mode (reversible).
    hidden: bool = False
