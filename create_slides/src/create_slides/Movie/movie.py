from dataclasses import dataclass
from pathlib import Path


@dataclass
class Movie:
    video_path: Path
    poster_path: Path
