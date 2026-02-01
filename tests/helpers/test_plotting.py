"""Tests for plotting helper functions."""

from datetime import UTC, datetime

from hamcrest import assert_that, equal_to, greater_than, is_

from technical_analysis_mcp.helpers import plot_time_series
from technical_analysis_mcp.models.data_point import DataPoint
from technical_analysis_mcp.models.time_series import TimeSeries


def test_given_time_series_when_plot_then_image_file_is_created() -> None:
    """Test simple plotting time series.

    Given a single time series.
    When plotting,
    Then the plot file is create and it is PNG image.

    """
    points = [
        DataPoint(date=datetime(2024, 1, 1, tzinfo=UTC), value=0.0),
        DataPoint(date=datetime(2024, 1, 2, tzinfo=UTC), value=100.0),
    ]

    series = TimeSeries(ticker="AAPL", points=points)

    path = plot_time_series([series], "Unit test")

    assert_that(path.exists(), is_(True))
    assert_that(path.stat().st_size, greater_than(0))
    assert_that(path.suffix, equal_to(".png"))
