"""Test utility functions for dictionary parsing."""

from typing import Any

import pytest
from hamcrest import assert_that, is_

from technical_analysis_mcp.utils import (
    get_dictionary_float,
    get_dictionary_optional_float,
    get_dictionary_optional_string,
    get_dictionary_string,
)

TEST_PRICE_FLOAT = 123.45
TEST_PRICE_INT = 123.0


def test_get_dictionary_string() -> None:
    """Test get_dictionary_string with a valid string field."""
    data: dict[str, Any] = {"name": "Apple"}
    assert_that(get_dictionary_string(data, "name"), is_("Apple"))


def test_get_dictionary_string_missing_field() -> None:
    """Test get_dictionary_string with a missing field."""
    data: dict[str, Any] = {}
    with pytest.raises(ValueError, match="Field 'name' is missing"):
        get_dictionary_string(data, "name")


def test_get_dictionary_string_invalid_type() -> None:
    """Test get_dictionary_string with an invalid type."""
    data: dict[str, Any] = {"name": 123}
    with pytest.raises(TypeError, match="Field 'name' is not a string"):
        get_dictionary_string(data, "name")


def test_get_dictionary_optional_string() -> None:
    """Test get_dictionary_optional_string with a valid string field."""
    data: dict[str, Any] = {"name": "Apple"}
    assert_that(get_dictionary_optional_string(data, "name"), is_("Apple"))


def test_get_dictionary_optional_string_missing_field() -> None:
    """Test get_dictionary_optional_string with a missing field."""
    data: dict[str, Any] = {}
    assert_that(get_dictionary_optional_string(data, "name"), is_(None))


def test_get_dictionary_optional_string_invalid_type() -> None:
    """Test get_dictionary_optional_string with an invalid type."""
    data: dict[str, Any] = {"name": 123}
    with pytest.raises(TypeError, match="Field 'name' is not a string"):
        get_dictionary_optional_string(data, "name")


def test_get_dictionary_float() -> None:
    """Test get_dictionary_float with a valid float field."""
    data: dict[str, Any] = {"price": TEST_PRICE_FLOAT}
    assert_that(get_dictionary_float(data, "price"), is_(TEST_PRICE_FLOAT))


def test_get_dictionary_float_int() -> None:
    """Test get_dictionary_float with a valid int field."""
    data: dict[str, Any] = {"price": TEST_PRICE_INT}
    assert_that(get_dictionary_float(data, "price"), is_(TEST_PRICE_INT))


def test_get_dictionary_float_missing_field() -> None:
    """Test get_dictionary_float with a missing field."""
    data: dict[str, Any] = {}
    with pytest.raises(ValueError, match="Field 'price' is missing"):
        get_dictionary_float(data, "price")


def test_get_dictionary_float_invalid_type() -> None:
    """Test get_dictionary_float with an invalid type."""
    data: dict[str, Any] = {"price": "123.45"}
    with pytest.raises(TypeError, match="Field 'price' is not a float or int"):
        get_dictionary_float(data, "price")


def test_get_dictionary_optional_float() -> None:
    """Test get_dictionary_optional_float with a valid float field."""
    data: dict[str, Any] = {"price": TEST_PRICE_FLOAT}
    assert_that(get_dictionary_optional_float(data, "price"), is_(TEST_PRICE_FLOAT))


def test_get_dictionary_optional_float_int() -> None:
    """Test get_dictionary_optional_float with a valid int field."""
    data: dict[str, Any] = {"price": TEST_PRICE_INT}
    assert_that(get_dictionary_optional_float(data, "price"), is_(TEST_PRICE_INT))


def test_get_dictionary_optional_float_missing_field() -> None:
    """Test get_dictionary_optional_float with a missing field."""
    data: dict[str, Any] = {}
    assert_that(get_dictionary_optional_float(data, "price"), is_(None))


def test_get_dictionary_optional_float_invalid_type() -> None:
    """Test get_dictionary_optional_float with an invalid type."""
    data: dict[str, Any] = {"price": "123.45"}
    with pytest.raises(TypeError, match="Field 'price' is not a float or int"):
        get_dictionary_optional_float(data, "price")
