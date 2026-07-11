from pathlib import Path

from create_slides.DeckBuilding import build_single_slide_deck
from create_slides.Slide import Slide
from create_slides.UnisiBackground import UNISI_CONTENT_SLIDE

REPO_ROOT = Path(__file__).resolve().parents[4]
OUTPUT_PATH = REPO_ROOT / "SLIDES" / "slide_01_problema_obiettivo.pptx"
PAPERS_DIR = REPO_ROOT / "create_slides" / "assets" / "papers"

SLIDE = Slide(
    number=1,
    title="Il Problema, gli Esempi & l'Obiettivo della Tesi",
    visual_bullets=[
        "Acque reflue: farmaci, coloranti e contaminanti difficili da rimuovere",
        "In letteratura: \"spugne molecolari\" con buoni risultati sperimentali",
        "Obiettivo: predire e generare polimeri adsorbenti per via computazionale",
    ],
    images=[PAPERS_DIR / "cryogel_dual_sponge_photo.png"],
    speech=(
        "Partiamo dal problema: le acque reflue contengono molecole inquinanti — farmaci, "
        "coloranti, altri contaminanti — che i trattamenti standard faticano a rimuovere in "
        "modo mirato. In letteratura esistono già esempi di \"spugne molecolari\", polimeri "
        "progettati per adsorbire selettivamente queste molecole, con risultati sperimentali "
        "incoraggianti. Il problema è che ogni nuovo polimero richiede tipicamente sintesi e "
        "test in laboratorio, un processo lento e costoso. L'obiettivo della mia tesi è quindi "
        "predire e generare polimeri — le \"spugne molecolari\" — capaci di adsorbire molecole "
        "inquinanti target dalle acque reflue, ma per via computazionale: invece di scegliere a "
        "mano un polimero e testarlo in laboratorio, ho costruito una pipeline in grado di "
        "proporre e valutare automaticamente polimeri candidati."
    ),
    todos=[
        "Trovare una foto generica di acque reflue contaminate e un diagramma schematico "
        "polimero-spugna/molecola (non presenti nel vault Obsidian). Altre figure "
        "disponibili: vedi create_slides/assets/papers/paper_mapping.json.",
    ],
)


def main() -> None:
    build_single_slide_deck(SLIDE, OUTPUT_PATH, background=UNISI_CONTENT_SLIDE)


if __name__ == "__main__":
    main()
