from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Slide:
    number: int
    title: str
    visual_bullets: list[str]
    speech: str
    todos: list[str] = field(default_factory=list)
    images: list[Path] = field(default_factory=list)
