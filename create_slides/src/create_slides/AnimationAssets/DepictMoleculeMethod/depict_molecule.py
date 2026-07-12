from pathlib import Path

from rdkit import Chem
from rdkit.Chem.Draw import rdMolDraw2D


def depict_molecule(
    smiles: str,
    output_path: Path,
    image_size: tuple[int, int] = (1000, 700),
) -> Path:
    """Render a single SMILES (or P-SMILES with `*` attachment points) to a PNG."""
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"Unparseable SMILES: {smiles}")
    drawer = rdMolDraw2D.MolDraw2DCairo(*image_size)
    options = drawer.drawOptions()
    options.clearBackground = False
    options.bondLineWidth = 3
    rdMolDraw2D.PrepareAndDrawMolecule(drawer, mol)
    drawer.FinishDrawing()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(drawer.GetDrawingText())
    return output_path
