"""Python wrapper for getting weather data from KachelmannWetter API."""

from __future__ import annotations

import logging
from http import HTTPStatus
from typing import TYPE_CHECKING, Any

import orjson
from aiohttp import ClientSession

from icecream import ic

from .const import (
    ATTR_CURRENT_CONDITIONS,
    ATTR_FORECAST_3DAYS,
    ATTR_TREND_14DAYS,
    HTTP_HEADERS,
    REMOVE_FROM_CURRENT_CONDITION,
    REMOVE_FROM_FORECAST,
    REMOVE_FROM_TREND,
)
from .exceptions import (
    ApiError,
    InvalidApiKeyError,
    InvalidCoordinatesError,
)
from .utils import (
    construct_url,
    parse_current_condition,
    parse_3day_forecast,
    parse_14day_trend,
    valid_api_key,
    valid_coordinates,
    update_http_headers
)

_LOGGER = logging.getLogger(__name__)


class KachelmannWetter:
    """Main class to perform KachelmannWetter API requests."""

    def __init__(
        self,
        api_key: str,
        session: ClientSession,
        latitude: float | None = None,
        longitude: float | None = None,
        units: str = "metric"
    ) -> None:
        """Initialize."""
        if not valid_api_key(api_key):
            raise InvalidApiKeyError(
                "Your API Key must be a 128-character hexadecimal string"
            )
        self.latitude = latitude
        self.longitude = longitude
        if not valid_coordinates(self.latitude, self.longitude):
            raise InvalidCoordinatesError(
                "Your coordinates must be a float between -90 and 90 for latitude and -180 and 180 for longitude"
            )
        self._api_key = api_key
        self._session = session
        self.units = units
        update_http_headers(self._api_key)

    async def _async_get_data(self, url: str) -> Any:
        """Retrieve data from AccuWeather API."""
        async with self._session.get(url, headers=HTTP_HEADERS) as resp:
            if resp.status == HTTPStatus.UNAUTHORIZED.value:
                raise InvalidApiKeyError("Invalid API key")

            if resp.status != HTTPStatus.OK.value:
                try:
                    error_text = orjson.loads(await resp.text())
                except orjson.JSONDecodeError as exc:
                    raise ApiError(f"Can't decode API response: {exc}") from exc
                raise ApiError(f"Invalid response from KachelmannWetter API: {resp.status}")

            _LOGGER.debug("Data retrieved from %s, status: %s", url, resp.status)
            data = await resp.json()

        return data if isinstance(data, dict) else data[0]

    async def async_get_current_conditions(self) -> dict[str, Any]:
        """Retrieve current conditions data from KachelmannWetter."""

        url = construct_url(
            ATTR_CURRENT_CONDITIONS,
            lat=self.latitude,
            lon=self.longitude,
            units=self.units,
        )
        data = await self._async_get_data(url)
        return parse_current_condition(data, REMOVE_FROM_CURRENT_CONDITION)

    async def async_get_3day_forecast(
        self, units: str = "metric"
    ) -> list[dict[str, Any]]:
        """Retrieve 3 day forecast data from KachelmannWetter."""

        url = construct_url(
            ATTR_FORECAST_3DAYS,
            lat=self.latitude,
            lon=self.longitude,
            units=self.units,
        )
        data = await self._async_get_data(url)
        return parse_3day_forecast(data, REMOVE_FROM_FORECAST)

    async def async_get_14day_trend(
        self, units: str = "metric"
    ) -> list[dict[str, Any]]:
        """Retrieve 14 day trend data from KachelmannWetter."""

        url = construct_url(
            ATTR_TREND_14DAYS,
            lat=self.latitude,
            lon=self.longitude,
            units=self.units,
        )
        data = await self._async_get_data(url)
        return parse_14day_trend(data, REMOVE_FROM_TREND)

    async def async_get_hourly_forecast(
        self, hours: int = 12, metric: bool = True
    ) -> list[dict[str, Any]]:
        """Retrieve hourly forecast data from AccuWeather."""
        if not self._location_key:
            await self.async_get_location()

        if TYPE_CHECKING:
            assert self._location_key is not None

        url = construct_url(
            ATTR_FORECAST_HOURLY,
            api_key=self._api_key,
            location_key=self._location_key,
            hours=str(hours),
            metric=str(metric).lower(),
        )
        data = await self._async_get_data(url)
        return parse_hourly_forecast(data, REMOVE_FROM_FORECAST)
