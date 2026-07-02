# images_into_ascii

Converts photos to colored ASCII art PNGs sized for the thesis (`\ttfamily\tiny` on A4).
Output PNGs are dropped into `ascii_output/` alongside a ready-to-paste `.tex` snippet.

## Requirements

[uv](https://docs.astral.sh/uv/) — the script is self-contained, dependencies are declared inline.

## Usage

```bash
# single image
uv run convert.py images/photo.jpg

# multiple images at once
uv run convert.py images/photo1.jpg images/photo2.jpg images/photo3.jpg

# custom output directory
uv run convert.py images/photo.jpg --output-dir ascii_output/
```

## Options

| Flag | Default | Description |
|---|---|---|
| `--width` | `120` | Characters per row. 120 fills the thesis text width at `\tiny`. |
| `--font-size` | `14` | Font size in pixels for the rendered PNG. Increase for sharper print. |
| `--contrast` | `1.4` | Contrast boost before conversion. Higher = more defined edges. |
| `--bg` | `10,10,10` | Background color as `R,G,B`. Default is near-black. |
| `--output-dir` | `ascii_output/` | Directory where PNGs and `.tex` snippets are saved. |

## Tuning tips

- **Portrait / face photos** — `--width 100` tends to give better proportions for single faces.
- **Group photos** — `--width 140` or higher to keep faces distinguishable.
- **Washed out result** — raise `--contrast` to `1.8` or `2.0`.
- **Too dark / crushed shadows** — lower `--contrast` to `1.1` or `1.2`.
- **Sharper print quality** — raise `--font-size` to `18` or `20`.

## Output

For each input `photo.jpg` the script produces:

```
ascii_output/
  photo.png   ← include this in LaTeX via \includegraphics
  photo.tex   ← ready-made LaTeX snippet to paste into 10_acknow.tex
```

The `.tex` snippet looks like:

```latex
\begin{figure}[htbp]
\centering
\includegraphics[width=0.85\textwidth]{images_into_ascii/ascii_output/photo.png}
\end{figure}
```

## Folder structure

```
images_into_ascii/
  convert.py          ← the script
  README.md           ← this file
  images/             ← put your source photos here
    Originals/        ← keep unedited originals here
  ascii_output/       ← generated PNGs and .tex snippets (git-ignored or not)
```
