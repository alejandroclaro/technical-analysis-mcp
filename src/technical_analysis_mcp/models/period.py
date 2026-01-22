"""Model for period."""

from typing import Annotated, Literal

from pydantic import Field

Period = Annotated[
    Literal["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"],
    Field(description="The time period for which the historical data was fetched."),
]
