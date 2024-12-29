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
            current_conditions = await wetter.async_get_current_conditions()
            forecast_3days = await wetter.async_get_3day_forecast(
                units="metric"
            )
            trend_14days = await wetter.async_get_14day_trend(
                units="metric"
            )

        except (
            ApiError,
            InvalidApiKeyError,
            InvalidCoordinatesError,
            ClientError,
            ) as error:
            print(f"Error: {error}")
        else:
            ic(current_conditions)
            ic(forecast_3days)
            ic(trend_14days)

loop = asyncio.new_event_loop()
loop.run_until_complete(main())
loop.close()
```