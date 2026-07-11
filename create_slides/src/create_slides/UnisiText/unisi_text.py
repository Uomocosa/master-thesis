from dataclasses import dataclass
from typing import Self

LEVEL_SIZES_PT = {1: 28, 2: 24, 3: 20}


@dataclass
class UnisiText:
    size_pt: int
    font_name: str = "Optima"
    bold: bool = False
    color: str = "000000"

    @classmethod
    def level(cls, level: int) -> Self:
        return cls(size_pt=LEVEL_SIZES_PT[level])
