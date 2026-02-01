"""Model for price."""

from datetime import datetime

import pandas as pd
from pydantic import BaseModel, Field

from .price_source import PriceSource


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


def convert_prices_to_panda_series(prices: list[Price], source: PriceSource) -> pd.Series:
    """Convert price data to a pandas Series with datetime index.

    Args:
        prices: The list of prices to convert.
        source: The price field to extract (open, high, low, close).

    Returns:
        The pandas series with datetime index and price values.

    """
    result = {}

    for price in prices:
        if source == "open":
            result[price.date] = price.open
        elif source == "high":
            result[price.date] = price.high
        elif source == "low":
            result[price.date] = price.low
        else:  # close
            result[price.date] = price.close

    return pd.Series(result, dtype=float)
