from dataclasses import dataclass


@dataclass
class UnisiLineTitleSeparation:
    position: tuple[int, int]
    length: int
    color: str = "000000"
    weight: int = 38100
