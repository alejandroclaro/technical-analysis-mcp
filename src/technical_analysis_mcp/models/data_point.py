"""Model for a time data point."""

from datetime import datetime

from pydantic import BaseModel, Field


class DataPoint(BaseModel):
    """Represents a single data point in a time series, consisting of a timestamp and a value."""

    date: datetime = Field(description="The timestamp for this data point in ISO 8601 format.")
    value: float = Field(description="The numerical value, e.g., an indicator value ranging from 0 to 100 for RSI.")
