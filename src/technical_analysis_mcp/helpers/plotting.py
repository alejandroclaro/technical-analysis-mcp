"""Simple plotting utilities for financial time series data."""

import io
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

from technical_analysis_mcp.models import TimeSeries

from .files import write_to_temporal_file


def plot_time_series(series: list[TimeSeries], title: str) -> Path:
    """Plot the given time series as simple points with connecting lines.

    Args:
      series: The list of time series to plot.
      title: The plot title.

    Returns:
        The path to the saved plot image in a temporal directory.

    """
    figure, axes = plt.subplots(figsize=(10, 5))

    axes.set_title(title)
    axes.set_xlabel("Date")
    axes.set_ylabel("Value")
    axes.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d %H:%M"))
    axes.grid(visible=True, alpha=0.3)

    for s in series:
        dates = [point.date for point in s.points]
        y = [point.value for point in s.points]
        x = mdates.date2num(dates)
        axes.plot(x, y, "o-", linewidth=2, markersize=6, color="blue")

    figure.autofmt_xdate()
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png", dpi=150)
    plt.close(figure)
    buffer.seek(0)

    return write_to_temporal_file(buffer.getvalue(), extension="png")
