"""Error Data structure."""

from pydantic import BaseModel


class Error(BaseModel):
    """Structured model for error responses."""

    reason: str
