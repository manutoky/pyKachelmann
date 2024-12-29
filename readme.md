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
    RequestsExceededError,
)

LATITUDE = 51.000
LONGITUDE = 10.000
API_KEY = "xxxx"

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
            # forecast_hourly = await wetter.async_get_hourly_forecast(
            #     hours=12, metric=True
            # )
        except (
            ApiError,
            InvalidApiKeyError,
            InvalidCoordinatesError,
            ClientError,
            RequestsExceededError,
        ) as error:
            print(f"Error: {error}")
        else:
            #print(f"Location: {wetter.location_name} ({wetter.location_key})")
            #print(f"Requests remaining: {wetter.requests_remaining}")
            print(f"Current: {current_conditions}")
            print(f"Forecast: {forecast_3days}")


loop = asyncio.new_event_loop()
loop.run_until_complete(main())
loop.close()
```