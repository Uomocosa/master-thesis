from pptx.dml.color import RGBColor
from pptx.text.text import _Paragraph
from pptx.util import Pt

from create_slides.UnisiCenterTitle import UnisiCenterTitle
from create_slides.UnisiSubtitle import UnisiSubtitle
from create_slides.UnisiText import UnisiText
from create_slides.UnisiTitle import UnisiTitle

UnisiTextStyle = UnisiCenterTitle | UnisiSubtitle | UnisiTitle | UnisiText


def apply_unisi_text_style(paragraph: _Paragraph, style: UnisiTextStyle) -> None:
    for run in paragraph.runs:
        run.font.name = style.font_name
        run.font.size = Pt(style.size_pt)
        run.font.bold = style.bold
        run.font.color.rgb = RGBColor.from_string(style.color)
        if getattr(style, "caps", False):
            run.font._rPr.set("cap", "all")
