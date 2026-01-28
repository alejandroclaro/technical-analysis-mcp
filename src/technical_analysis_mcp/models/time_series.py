"""Model for time series."""

from pydantic import BaseModel, Field

from .data_point import DataPoint

_DESCRIPTIONS = {
    "ticker": "The ticker symbol for this time series.",
    "data_points": "List of data points in chronological order for the time series.",
}


class TimeSeries(BaseModel):
    """A time series of data points for a specific ticker, typically representing an indicator like RSI."""

    ticker: str = Field(description=_DESCRIPTIONS["ticker"])
    data_points: list[DataPoint] = Field(default_factory=list, description=_DESCRIPTIONS["data_points"])
