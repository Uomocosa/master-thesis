import csv
from pathlib import Path

from loguru import logger
from rdkit import Chem
from rdkit.Chem.Draw import rdMolDraw2D


def depict_polymers(
    csv_path: Path,
    output_dir: Path,
    count: int = 6,
    image_size: tuple[int, int] = (1200, 700),
) -> list[Path]:
    """Render the first `count` parseable PSMILES of the CSV to transparent PNGs."""
    output_dir.mkdir(parents=True, exist_ok=True)
    rendered: list[Path] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        if len(rendered) >= count:
            break
        psmiles = row["PSMILES"]
        mol = Chem.MolFromSmiles(psmiles)
        if mol is None:
            logger.warning(f"Skipping unparseable PSMILES: {psmiles}")
            continue
        drawer = rdMolDraw2D.MolDraw2DCairo(*image_size)
        options = drawer.drawOptions()
        options.clearBackground = False
        options.bondLineWidth = 3
        rdMolDraw2D.PrepareAndDrawMolecule(drawer, mol)
        drawer.FinishDrawing()
        output_path = output_dir / f"polymer_{len(rendered) + 1:02d}.png"
        output_path.write_bytes(drawer.GetDrawingText())
        rendered.append(output_path)
        logger.info(f"Rendered {output_path.name}: {psmiles}")
    return rendered
