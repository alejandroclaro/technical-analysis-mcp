"""Model for asset price history."""

import pandas as pd
from pydantic import BaseModel, Field

from .interval import Interval
from .period import Period
from .price import Price
from .price_source import PriceSource


class AssetPriceHistory(BaseModel):
    """Represents a collection of asset price history."""

    ticker: str = Field(description="The ticker symbol of the asset.")
    period: Period = Field(description="The time period for which the historical data was fetched.")
    interval: Interval = Field(description="The interval between data points.")
    prices: list[Price] = Field(description="The list of price entries.")


def get_price_series(history: AssetPriceHistory, source: PriceSource) -> pd.Series:
    """Convert price data to a pandas Series with datetime index.

    Args:
        history: The asset price history.
        source: The price field to extract (open, high, low, close).

    Returns:
        The pandas series with datetime index and price values.

    """
    data_dict = {}

    for price in history.prices:
        if source == "open":
            data_dict[price.date] = price.open
        elif source == "high":
            data_dict[price.date] = price.high
        elif source == "low":
            data_dict[price.date] = price.low
        else:  # close
            data_dict[price.date] = price.close

    return pd.Series(data_dict, dtype=float)
