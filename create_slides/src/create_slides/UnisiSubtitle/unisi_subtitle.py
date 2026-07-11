from dataclasses import dataclass


@dataclass
class UnisiSubtitle:
    font_name: str = "Optima"
    size_pt: int = 24
    bold: bool = True
    color: str = "990000"
