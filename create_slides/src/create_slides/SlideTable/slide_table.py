from dataclasses import dataclass


@dataclass
class SlideTable:
    headers: list[str]
    rows: list[list[str]]
