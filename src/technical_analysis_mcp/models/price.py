"""Model for price."""

from datetime import datetime

from pydantic import BaseModel, Field


class Price(BaseModel):
    """Represents a single price entry."""

    date: datetime = Field(description="The date and time of the price entry.")
    open: float = Field(description="The opening price of the asset.")
    high: float = Field(description="The highest price of the asset during the interval.")
    low: float = Field(description="The lowest price of the asset during the interval.")
    close: float = Field(description="The closing price of the asset.")
    volume: int = Field(description="The trading volume of the asset.")
    dividends: float = Field(description="The dividends paid during the interval.")
    stock_splits: float = Field(description="The stock splits that occurred during the interval.")
