"""Python wrapper for getting weather data from KachelmannWetter API."""

from __future__ import annotations

import logging
from http import HTTPStatus
from typing import TYPE_CHECKING, Any

import orjson
from aiohttp import ClientSession

from icecream import ic

from .const import (
    ATTR_STATION_OBSERVATION_LATEST,
    ATTR_STATION_SEARCH,
    ATTR_STATION_OBSERVATIONS,
    ATTR_CURRENT_CONDITIONS,
    ATTR_FORECAST_3DAYS,
    ATTR_TREND_14DAYS,
    ATTR_FORECAST_STANDARD,
    ATTR_FORECAST_ADVANCED,
    ATTR_ASTRONIMICAL,
    ATTR_WEATHER_SYMBOL,
    HTTP_HEADERS,
    REMOVE_FROM_CURRENT_CONDITION,
    REMOVE_FROM_FORECAST,
    REMOVE_FROM_TREND,
)
from .exceptions import (
    ApiError,
    InvalidApiKeyError,
    InvalidCoordinatesError,
    InvalidTimestepsError,
)
from .utils import (
    construct_url,
    parse_current_condition,
    parse_3day_forecast,
    parse_14day_trend,
    valid_api_key,
    valid_coordinates,
    valid_forecast_timesteps,
    valid_observations_timesteps,
    valid_units,
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

    def set_units(self, units: str) -> None:
        """Set units."""
        if valid_units(units):
            self.units = units

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
                raise ApiError(f"Invalid response from KachelmannWetter API: {resp.status}: {error_text}")

            _LOGGER.debug("Data retrieved from %s, status: %s", url, resp.status)
            data = await resp.json()

        #return data if isinstance(data, dict) else data[0]
        return data
    
    async def async_search_station(self, radius: int = 10) -> dict[str, Any]:
        """Search for weather stations near the provided coordinates."""
        url = construct_url(
            ATTR_STATION_SEARCH,
            lat=self.latitude,
            lon=self.longitude,
            radius=radius,
        )
        data = await self._async_get_data(url)
        return data

    async def async_get_station_observation_latest(self, station_id: str) -> dict[str, Any]:
        """Retrieve last observation data from KachelmannWetter."""
        url = construct_url(
            ATTR_STATION_OBSERVATION_LATEST,
            stationId=station_id,
        )
        data = await self._async_get_data(url)
        return data

    async def async_get_station_observations(self, station_id: str, timesteps: str = "1d") -> dict[str, Any]:
        """Retrieve observation data from KachelmannWetter."""
        if not valid_observations_timesteps(timesteps):
            raise InvalidTimestepsError(
                "Your timesteps must be one of the following: 10min, 1h, 1d"
            )
        url = construct_url(
            ATTR_STATION_OBSERVATIONS,
            stationId=station_id,
            timeSteps=timesteps,
        )
        data = await self._async_get_data(url)
        return data
                                             
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
        self, 
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
        self, 
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

    async def async_get_standard_forecast(
        self, timesteps: str = "6h", 
    ) -> dict[str, Any]:
        """Retrieve standard forecast data from KachelmannWetter."""
        if not valid_forecast_timesteps(timesteps):
            raise InvalidTimestepsError(
                "Your timesteps must be one of the following: 1h, 3h, 6h"
            )
        url = construct_url(
            ATTR_FORECAST_STANDARD,
            lat=self.latitude,
            lon=self.longitude,
            timeSteps=timesteps,
            units=self.units,
        )
        data = await self._async_get_data(url)
        return data

    async def async_get_advanced_forecast(
            self, timesteps: str = "6h", 
    ) -> dict[str, Any]:
        """Retrieve advanced forecast data from KachelmannWetter."""
        if not valid_forecast_timesteps(timesteps):
            raise InvalidTimestepsError(
                "Your timesteps must be one of the following: 1h, 3h, 6h"
            )
        url = construct_url(
            ATTR_FORECAST_ADVANCED,
            lat=self.latitude,
            lon=self.longitude,
            timeSteps=timesteps,
            units=self.units,
        )
        data = await self._async_get_data(url)
        return data

    async def async_get_astronomical_data(self) -> dict[str, Any]:
        """Retrieve astronomical data from KachelmannWetter."""
        url = construct_url(
            ATTR_ASTRONIMICAL,
            lat=self.latitude,
            lon=self.longitude,
        )
        data = await self._async_get_data(url)
        return data
    
    ## Weather Symbol not supported yet
    # async def async_get_weather_symbol(self,
    #         weatherSymbol: str, format: str = "svg"                               
    #     ) -> dict[str, Any]:
    #     """Retrieve weather symbol data from KachelmannWetter."""
    #     url = construct_url(
    #         ATTR_WEATHER_SYMBOL,
    #         lat=self.latitude,
    #         lon=self.longitude,
    #     )
    #     data = await self._async_get_data(url)
    #     return data
