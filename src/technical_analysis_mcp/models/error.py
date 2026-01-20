"""Error Data structure."""

from pydantic import BaseModel, Field


class Error(BaseModel):
    """Structured model for error responses."""

    what: str = Field(..., description="Error message")
