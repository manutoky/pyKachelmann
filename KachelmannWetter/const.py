"""Constants for KachelmannWetter library."""

from __future__ import annotations

ATTR_CURRENT_CONDITIONS: str = "currentconditions"
ATTR_FORECAST_3DAYS: str = "forecasts_3days"
ATTR_TREND_14DAYS: str = "trend_14days"
ATTR_FORECAST_DAILY: str = "forecasts"
ATTR_FORECAST_HOURLY: str = "forecasts_hourly"
ATTR_GEOPOSITION: str = "geoposition"

MAX_API_KEY_LENGTH = 128
MAX_LATITUDE = 90
MAX_LONGITUDE = 180

ENDPOINT: str = "https://api.kachelmannwetter.com/v02/"
HTTP_HEADERS: dict[str, str] = {"Accept": "application/json", "X-API-Key": ""}
REQUESTS_EXCEEDED: str = "The allowed number of requests has been exceeded."

REMOVE_FROM_CURRENT_CONDITION: tuple[str, ...] = (

)
REMOVE_FROM_FORECAST: tuple[str, ...] = (

)
REMOVE_FROM_TREND: tuple[str, ...] = (

)
TEMPERATURES: tuple[str, ...] = (
    "Temperature",
    "RealFeelTemperature",
    "RealFeelTemperatureShade",
)
URLS: dict[str, str] = {
    
    ATTR_CURRENT_CONDITIONS: (
        "current/{lat}/{lon}"
        "?units={units}"
    ),
    ATTR_FORECAST_3DAYS: (
        "forecast/{lat}/{lon}/3day"
        "?units={units}"
    ),
    ATTR_TREND_14DAYS: (
        "forecast/{lat}/{lon}/trend14days"
        "?units={units}"
    ),
  
}