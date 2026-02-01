"""Tests for file manipulation helper functions."""

from hamcrest import assert_that, equal_to, is_

from technical_analysis_mcp.helpers import write_to_temporal_file


def test_given_content_when_write_to_temporal_file_then_file_is_created() -> None:
    """Test simple valid write case.

    Given string content,
    When writing to a temporal file,
    Then the file should contain the content.

    """
    content = "Lorem ipsum dolor sit amet"

    path = write_to_temporal_file(content)

    assert_that(path.exists(), is_(True))

    with path.open() as file:
        assert_that(file.read(), equal_to(content))


def test_given_suffix_when_write_to_temporal_file_then_file_has_correct_suffix() -> None:
    """Suffix test case.

    Given a suffix,
    when writing to a temporal file,
    then the file should have the correct suffix.

    """
    content = "Test Content"
    suffix = ".csv"

    path = write_to_temporal_file(content, suffix)

    assert_that(path.exists(), is_(True))
    assert_that(path.suffix, equal_to(suffix))
