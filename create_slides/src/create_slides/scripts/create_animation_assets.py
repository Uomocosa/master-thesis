import subprocess
import sys
import tempfile
from pathlib import Path

from loguru import logger

from create_slides.AnimationAssets import depict_molecule, depict_polymers, extract_poster

CREATE_SLIDES_DIR = Path(__file__).resolve().parents[3]
REPO_ROOT = CREATE_SLIDES_DIR.parent
ANIMATIONS_DIR = CREATE_SLIDES_DIR / "assets" / "animations"
SCENES_DIR = CREATE_SLIDES_DIR / "src" / "create_slides" / "scenes"
VALID_POLYMERS_CSV = (
    REPO_ROOT / "RESULTS" / "find_polymer_for_target_molecule" / "aspirin" / "02_valid_polymers.csv"
)

ASPIRIN_SMILES = "CC(=O)OC1=CC=CC=C1C(=O)O"
REPEAT_UNIT_PSMILES = "*CC(c1ccccc1)*"

# (scene file, scene class, output mp4 stem, poster frame time in seconds)
SCENES = [
    ("polymer_carousel.py", "PolymerCarouselScene", "polymer_carousel", 1.5),
    ("prediction_pipeline.py", "PredictionPipelineScene", "prediction_pipeline", 8.3),
    ("pdcc_carousel.py", "PDCCCarouselScene", "pdcc_carousel", 4.0),
    ("smiles_reveal.py", "SmilesRevealScene", "smiles_reveal", 1.5),
    ("smiles_reveal.py", "PsmilesRevealScene", "psmiles_reveal", 1.5),
    ("featurization_clock.py", "FeaturizationClockScene", "featurization_clock", 10.5),
    ("interpolation_curves.py", "InterpolationCurvesScene", "interpolation_curves", 7.5),
    ("generative_transformer.py", "GenerativeTransformerScene", "generative_transformer", 6.6),
    ("model_carousel.py", "ModelCarouselScene", "model_carousel", 8.2),
    ("pscp_io.py", "PscpIoScene", "pscp_io", 5.0),
    ("pscp_schematic.py", "PscpSchematicScene", "pscp_schematic", 2.4),
    ("internet_papers.py", "InternetPapersScene", "internet_papers", 4.2),
    ("llm_magnifiers.py", "LlmMagnifiersScene", "llm_magnifiers", 5.5),
]


def render_scene(scene_file: str, scene_class: str, out_stem: str, poster_seconds: float) -> None:
    with tempfile.TemporaryDirectory() as media_dir:
        subprocess.run(
            [
                sys.executable,
                "-m",
                "manim",
                "render",
                "-qh",
                "--media_dir",
                media_dir,
                str(SCENES_DIR / scene_file),
                scene_class,
            ],
            check=True,
        )
        rendered = next(Path(media_dir).rglob(f"{scene_class}.mp4"))
        out_mp4 = ANIMATIONS_DIR / f"{out_stem}.mp4"
        out_mp4.write_bytes(rendered.read_bytes())
    extract_poster(out_mp4, poster_seconds, ANIMATIONS_DIR / f"{out_stem}_poster.png")
    logger.info(f"Rendered {out_stem}.mp4 (+ poster)")


def main() -> None:
    ANIMATIONS_DIR.mkdir(parents=True, exist_ok=True)
    depict_polymers(VALID_POLYMERS_CSV, ANIMATIONS_DIR / "polymers")
    depict_molecule(ASPIRIN_SMILES, ANIMATIONS_DIR / "molecule_aspirin.png")
    depict_molecule(REPEAT_UNIT_PSMILES, ANIMATIONS_DIR / "molecule_repeat_unit.png")
    for scene in SCENES:
        render_scene(*scene)
    logger.info(f"All animation assets regenerated in {ANIMATIONS_DIR}")


if __name__ == "__main__":
    main()
