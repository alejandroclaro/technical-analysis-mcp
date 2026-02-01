"""File manipulation helper functions."""

from pathlib import Path
from tempfile import NamedTemporaryFile


def write_to_temporal_file(content: str | bytes, extension: str | None = None) -> Path:
    """Write the given content into a temporal file.

    Args:
      content: The content to write.
      extension: The file extension.

    Returns:
        The path to the create file.

    """
    mode = "w" if isinstance(content, str) else "wb"

    with NamedTemporaryFile(suffix=f".{extension}", mode=mode, delete=False) as file:
        result = Path(file.name)
        file.write(content)

    return result
