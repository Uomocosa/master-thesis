from dataclasses import dataclass


@dataclass
class UnisiCenterTitle:
    font_name: str = "Optima"
    size_pt: int = 54
    bold: bool = False
    color: str = "000000"
