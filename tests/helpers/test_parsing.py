"""Test utility functions for dictionary parsing."""

from typing import Any

import pytest
from hamcrest import assert_that, is_

from technical_analysis_mcp.helpers import (
    get_dictionary_float,
    get_dictionary_optional_float,
    get_dictionary_optional_string,
    get_dictionary_string,
)

TEST_PRICE_FLOAT = 123.45
TEST_PRICE_INT = 123.0


def test_given_valid_string_field_when_get_dictionary_string_then_returns_string_value() -> None:
    """Test get_dictionary_string with a valid string field."""
    data: dict[str, Any] = {"name": "Apple"}

    assert_that(get_dictionary_string(data, "name"), is_("Apple"))


def test_given_missing_field_when_get_dictionary_string_then_raises_value_error() -> None:
    """Test get_dictionary_string with a missing field."""
    data: dict[str, Any] = {}

    with pytest.raises(ValueError, match="Field 'name' is missing"):
        get_dictionary_string(data, "name")


def test_given_invalid_type_when_get_dictionary_string_then_raises_type_error() -> None:
    """Test get_dictionary_string with an invalid type."""
    data: dict[str, Any] = {"name": 123}

    with pytest.raises(TypeError, match="Field 'name' is not a string"):
        get_dictionary_string(data, "name")


def test_given_valid_string_field_when_get_dictionary_optional_string_then_returns_string_value() -> None:
    """Test get_dictionary_optional_string with a valid string field."""
    data: dict[str, Any] = {"name": "Apple"}

    assert_that(get_dictionary_optional_string(data, "name"), is_("Apple"))


def test_given_missing_field_when_get_dictionary_optional_string_then_returns_none() -> None:
    """Test get_dictionary_optional_string with a missing field."""
    data: dict[str, Any] = {}

    assert_that(get_dictionary_optional_string(data, "name"), is_(None))


def test_given_invalid_type_when_get_dictionary_optional_string_then_raises_type_error() -> None:
    """Test get_dictionary_optional_string with an invalid type."""
    data: dict[str, Any] = {"name": 123}

    with pytest.raises(TypeError, match="Field 'name' is not a string"):
        get_dictionary_optional_string(data, "name")


def test_given_valid_float_field_when_get_dictionary_float_then_returns_float_value() -> None:
    """Test get_dictionary_float with a valid float field."""
    data: dict[str, Any] = {"price": TEST_PRICE_FLOAT}

    assert_that(get_dictionary_float(data, "price"), is_(TEST_PRICE_FLOAT))


def test_given_valid_int_field_when_get_dictionary_float_then_returns_float_value() -> None:
    """Test get_dictionary_float with a valid int field."""
    data: dict[str, Any] = {"price": TEST_PRICE_INT}

    assert_that(get_dictionary_float(data, "price"), is_(TEST_PRICE_INT))


def test_given_missing_field_when_get_dictionary_float_then_raises_value_error() -> None:
    """Test get_dictionary_float with a missing field."""
    data: dict[str, Any] = {}

    with pytest.raises(ValueError, match="Field 'price' is missing"):
        get_dictionary_float(data, "price")


def test_given_invalid_type_when_get_dictionary_float_then_raises_type_error() -> None:
    """Test get_dictionary_float with an invalid type."""
    data: dict[str, Any] = {"price": "123.45"}

    with pytest.raises(TypeError, match="Field 'price' is not a float or int"):
        get_dictionary_float(data, "price")


def test_given_valid_float_field_when_get_dictionary_optional_float_then_returns_float_value() -> None:
    """Test get_dictionary_optional_float with a valid float field."""
    data: dict[str, Any] = {"price": TEST_PRICE_FLOAT}

    assert_that(get_dictionary_optional_float(data, "price"), is_(TEST_PRICE_FLOAT))


def test_given_valid_int_field_when_get_dictionary_optional_float_then_returns_float_value() -> None:
    """Test get_dictionary_optional_float with a valid int field."""
    data: dict[str, Any] = {"price": TEST_PRICE_INT}

    assert_that(get_dictionary_optional_float(data, "price"), is_(TEST_PRICE_INT))


def test_given_missing_field_when_get_dictionary_optional_float_then_returns_none() -> None:
    """Test get_dictionary_optional_float with a missing field."""
    data: dict[str, Any] = {}

    assert_that(get_dictionary_optional_float(data, "price"), is_(None))


def test_given_invalid_type_when_get_dictionary_optional_float_then_raises_type_error() -> None:
    """Test get_dictionary_optional_float with an invalid type."""
    data: dict[str, Any] = {"price": "123.45"}

    with pytest.raises(TypeError, match="Field 'price' is not a float or int"):
        get_dictionary_optional_float(data, "price")
