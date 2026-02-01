"""Tests for viewing helper functions."""

from pathlib import Path
from tempfile import NamedTemporaryFile
from unittest.mock import patch

import pytest

from technical_analysis_mcp.helpers import open_image


def test_given_image_file_when_open_image_then_image_is_shown() -> None:
    """Test open_image opens the file.

    Given a PNG file,
    When open_image,
    Then the viewer is called with the right path.

    """
    with NamedTemporaryFile(suffix=".png") as file:
        path = Path(file.name)

        with patch("webbrowser.open", return_value=True) as mock_viewer:
            open_image(path)

            mock_viewer.assert_called_once_with(path.resolve().as_uri())


def test_given_wrong_path_when_open_image_then_error_is_thrown() -> None:
    """Test open_image throws an error if file does not exists.

    Given a path to a file that does not exists,
    When open_image,
    Then an error is thrown.

    """
    path = Path("does_not_exist.png")

    with pytest.raises(FileNotFoundError):
        open_image(path)


def test_given_viewer_error_when_open_image_then_error_is_thrown() -> None:
    """Test open_image report viewer failure to open the image.

    Given viewer cannot open the file,
    When open_image,
    Then an error is thrown.

    """
    with NamedTemporaryFile(suffix=".png") as file:
        path = Path(file.name)

        with patch("webbrowser.open", return_value=False), pytest.raises(RuntimeError):
            open_image(path)
