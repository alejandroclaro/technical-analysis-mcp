"""Model for price source."""

from typing import Annotated, Literal

from pydantic import Field

PriceSource = Annotated[
    Literal["open", "close", "high", "low"],
    Field(description="The price source for the computation of an indicator, typically 'close'."),
]
