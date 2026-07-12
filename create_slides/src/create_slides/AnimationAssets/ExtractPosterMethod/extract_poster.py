from pathlib import Path

import av


def extract_poster(video_path: Path, seconds: float, output_path: Path) -> Path:
    """Save the frame at `seconds` of the video as a PNG poster image."""
    container = av.open(str(video_path))
    stream = container.streams.video[0]
    container.seek(int(seconds / stream.time_base), stream=stream)
    for frame in container.decode(stream):
        frame.to_image().save(output_path)
        break
    container.close()
    return output_path
