"""Viewing functions for some data types."""

import webbrowser
from pathlib import Path


def open_image(file_path: Path) -> None:
    """Open an image file using the system's default viewer.

    Args:
        file_path: The path to the image file to open.

    Raises:
        FileNotFoundError: If the image file doesn't exist.
        RuntimeError: If the system command fails.
    """
    file_path = file_path.resolve(strict=True)

    if not file_path.exists():
        msg = f"Image file not found: {file_path}"
        raise FileNotFoundError(msg)

    ok = webbrowser.open(file_path.as_uri())

    if not ok:
        msg = "Failed to open image."
        raise RuntimeError(msg)
