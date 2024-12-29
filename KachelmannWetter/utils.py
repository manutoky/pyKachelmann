"""Utils for KachelmannWetter."""

from __future__ import annotations

from typing import Any

from .const import (
    ENDPOINT,
    MAX_API_KEY_LENGTH,
    MAX_LATITUDE,
    MAX_LONGITUDE,
    TEMPERATURES,
    URLS,
    HTTP_HEADERS
)

from icecream import ic

def valid_coordinates(latitude: float | None, longitude: float | None) -> bool:
    """Return True if coordinates are valid."""
    return (
        isinstance(latitude, int | float)
        and isinstance(longitude, int | float)
        and abs(latitude) <= MAX_LATITUDE
        and abs(longitude) <= MAX_LONGITUDE
    )


def valid_api_key(api_key: str) -> bool:
    """Return True if API key is valid."""
    return isinstance(api_key, str) and len(api_key) == MAX_API_KEY_LENGTH


def construct_url(arg: str, **kwargs: str) -> str:
    """Construct AccuWeather API URL."""
    return ENDPOINT + URLS[arg].format(**kwargs)

def update_http_headers(api_key : str) -> str:
    HTTP_HEADERS["X-API-Key"] = api_key

def parse_current_condition(
    data: dict[str, Any], to_remove: tuple[str, ...]
) -> dict[str, Any]:
    """Clean current condition API response."""
    
    result = {key: data[key] for key in data if key not in to_remove}
    return result


def parse_3day_forecast(
    data: dict[str, Any], to_remove: tuple[str, ...]
) -> list[dict[str, Any]]:
    """Parse and clean forecast API response."""
    # parsed_data = [
    #     {key: value for key, value in item.items() if key not in to_remove}
    #     for item in data["data"]
    # ]

    return data

def parse_14day_trend(
    data: dict[str, Any], to_remove: tuple[str, ...]
) -> list[dict[str, Any]]:
    """Parse and clean trend API response."""
    # parsed_data = [
    #     {key: value for key, value in item.items() if key not in to_remove}
    #     for item in data["data"]
    # ]

    return data