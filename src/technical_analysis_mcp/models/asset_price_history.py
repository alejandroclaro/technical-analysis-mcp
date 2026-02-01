"""Model for asset price history."""

from pydantic import BaseModel, Field

from .interval import Interval
from .period import Period
from .price import Price


class AssetPriceHistory(BaseModel):
    """Represents a collection of asset price history."""

    ticker: str = Field(description="The ticker symbol of the asset.")
    lookback_period: Period = Field(description="The time period for which the historical data was fetched.")
    interval: Interval = Field(description="The interval between data points.")
    prices: list[Price] = Field(description="The list of price entries.")
