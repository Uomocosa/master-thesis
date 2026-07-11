from dataclasses import dataclass


@dataclass
class UnisiTitle:
    font_name: str = "Optima"
    size_pt: int = 28
    bold: bool = False
    caps: bool = True
    color: str = "000000"
