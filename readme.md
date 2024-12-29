## pyKachelmannwetter
Python wrapper for getting weather data from KachelmannWetter.com API. 
The wrapper is a work in progress and may never be finished. Ultimate goal would be to integrate it in Home Assistant.
Heavily inspired by [https://github.com/bieniu/accuweather].

## API key
You need a subscription and a login to create an API key. See [https://accounts.meteologix.com/login]

## API documentation
See [https://api.kachelmannwetter.com/v02/_doc.html#/]

## How to use 
```python
"""Example of usage."""
import asyncio
import logging

from aiohttp import ClientError, ClientSession

from KachelmannWetter import (
    KachelmannWetter,
    ApiError,
    InvalidApiKeyError,
    InvalidCoordinatesError,
)

from icecream import ic

LATITUDE = 51.000
LONGITUDE = 9.000
RADIUS = 10
API_KEY = ""

logging.basicConfig(level=logging.DEBUG)


async def main():
    """Run main function."""
    async with ClientSession() as websession:
        try:
            wetter = KachelmannWetter(
                API_KEY,
                websession,
                latitude=LATITUDE,
                longitude=LONGITUDE,
                units="metric",
            )
            ## Stations
            # Search for the closest weather station
            stations = await wetter.async_search_station(radius=RADIUS)
            if stations:
                station_id = stations[0]["id"]
            else:
                raise ApiError("No weather station found")
            observation_latest = await wetter.async_get_station_observation_latest(station_id)
            observations = await wetter.async_get_station_observations(station_id, "1d")
            ## Current Weather
            current_conditions = await wetter.async_get_current_conditions()
            ## Forecasts
            forecast_3days = await wetter.async_get_3day_forecast()
            trend_14days = await wetter.async_get_14day_trend()
            standard_forecast = await wetter.async_get_standard_forecast(
                timesteps="1h"
            )
            advanced_forecast = await wetter.async_get_advanced_forecast(
                timesteps="1h"
            )
            ## Tools
            astronomical = await wetter.async_get_astronomical_data()
            
        except (
            ApiError,
            InvalidApiKeyError,
            InvalidCoordinatesError,
            ClientError,
            ) as error:
            print(f"Error: {error}")
        else:
            ic(observation_latest)
            ic(observations)
            ic(current_conditions)
            ic(forecast_3days)
            ic(trend_14days)
            ic(standard_forecast)
            ic(advanced_forecast)
            ic(astronomical)

loop = asyncio.new_event_loop()
loop.run_until_complete(main())
loop.close()
```