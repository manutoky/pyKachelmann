"""Constants for KachelmannWetter library."""

from __future__ import annotations

ATTR_STATION_OBSERVATION_LATEST: str = "station_observation_latest"
ATTR_STATION_SEARCH: str = "station_search"
ATTR_STATION_OBSERVATIONS: str = "station_observations"
ATTR_CURRENT_CONDITIONS: str = "currentconditions"
ATTR_FORECAST_3DAYS: str = "forecasts_3days"
ATTR_TREND_14DAYS: str = "trend_14days"
ATTR_FORECAST_STANDARD: str = "forecast_standard"
ATTR_FORECAST_ADVANCED: str = "forecast_advanced"
ATTR_ASTRONIMICAL: str = "astronomical"
ATTR_WEATHER_SYMBOL: str = "weather_symbol" # not supported yet

MAX_API_KEY_LENGTH = 128
MAX_LATITUDE = 90
MAX_LONGITUDE = 180
ALLOWED_FORECAST_TIMESTEPS = ("1h", "3h", "6h")
ALLOWED_OBSERVATIONS_TIMESTEPS = ("10min", "1h", "1d")
ALLOWED_UNITS = ("metric", "imperial")

ENDPOINT: str = "https://api.kachelmannwetter.com/v02/"
HTTP_HEADERS: dict[str, str] = {"Accept": "application/json", "X-API-Key": ""}
REQUESTS_EXCEEDED: str = "The allowed number of requests has been exceeded."

REMOVE_FROM_CURRENT_CONDITION: tuple[str, ...] = (

)
REMOVE_FROM_FORECAST: tuple[str, ...] = (

)
REMOVE_FROM_TREND: tuple[str, ...] = (

)

URLS: dict[str, str] = {
    
    ATTR_STATION_OBSERVATION_LATEST: (
        "station/{stationId}/observations/latest"
    ),
    ATTR_STATION_SEARCH: (
        "station/search/{lat}/{lon}"
        "?radius={radius}"
    ),
    ATTR_STATION_OBSERVATIONS: (
        "station/{stationId}/observations/{timeSteps}"
    ),        
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
    ATTR_FORECAST_STANDARD: (
        "forecast/{lat}/{lon}/standard/{timeSteps}"
        "?units={units}"
    ),
    ATTR_FORECAST_ADVANCED: (
        "forecast/{lat}/{lon}/advanced/{timeSteps}"
        "?units={units}"
    ),
    ATTR_ASTRONIMICAL: (
        "tools/astronomy/{lat}/{lon}"
    ),
    ATTR_WEATHER_SYMBOL: (
        "tools/weatherSymbol/{weatherSymbol}.{format}"
    ),
}