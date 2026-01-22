"""Model for interval."""

from typing import Annotated, Literal

from pydantic import Field

Interval = Annotated[
    Literal["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"],
    Field(description="The interval between data points."),
]
