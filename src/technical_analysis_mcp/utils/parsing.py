"""Parsing utilities for dictionary parsing."""

from typing import Any

MESSAGE_MISSING_FIELD = "Field '{}' is missing."
MESSAGE_INVALID_STRING_TYPE = "Field '{}' is not a string."
MESSAGE_INVALID_FLOAT_TYPE = "Field '{}' is not a float or int."


def get_dictionary_string(data: dict[str, Any], field: str) -> str:
    """Get a string field from a dictionary.

    Args:
        data: The input dictionary.
        field: The field to retrieve.

    Returns:
        The string value of the field.

    Raises:
        ValueError: If the field is missing.
        TypeError: If the field is not a string.

    """
    if field not in data:
        raise ValueError(MESSAGE_MISSING_FIELD.format(field))

    if not isinstance(data[field], str):
        raise TypeError(MESSAGE_INVALID_STRING_TYPE.format(field))

    return data[field]


def get_dictionary_optional_string(data: dict[str, Any], field: str) -> str | None:
    """Get an optional string field from a dictionary.

    Args:
        data: The input dictionary.
        field: The field to retrieve.

    Returns:
        The string value of the field, or None if the field is missing.

    Raises:
        TypeError: If the field is not a string.

    """
    if field not in data:
        return None

    if not isinstance(data[field], str):
        raise TypeError(MESSAGE_INVALID_STRING_TYPE.format(field))

    return data[field]


def get_dictionary_float(data: dict[str, Any], field: str) -> float:
    """Get a float field from a dictionary.

    Args:
        data: The input dictionary.
        field: The field to retrieve.

    Returns:
        The float value of the field.

    Raises:
        ValueError: If the field is missing.
        TypeError: If the field is not a float or int.

    """
    if field not in data:
        raise ValueError(MESSAGE_MISSING_FIELD.format(field))

    if not isinstance(data[field], (int, float)):
        raise TypeError(MESSAGE_INVALID_FLOAT_TYPE.format(field))

    return float(data[field])


def get_dictionary_optional_float(data: dict[str, Any], field: str) -> float | None:
    """Get an optional float field from a dictionary.

    Args:
        data: The input dictionary.
        field: The field to retrieve.

    Returns:
        The float value of the field, or None if the field is missing.

    Raises:
        TypeError: If the field is not a float or int.

    """
    if field not in data:
        return None

    if not isinstance(data[field], (int, float)):
        raise TypeError(MESSAGE_INVALID_FLOAT_TYPE.format(field))

    return float(data[field])
