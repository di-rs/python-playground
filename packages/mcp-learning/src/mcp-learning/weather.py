from typing import Annotated

import requests
from fastmcp import FastMCP

mcp = FastMCP("Weather Server")


@mcp.tool(
    name="get_weather",
    title="Get Current Weather",
    description="Get the current weather for a given latitude and longitude",
)
def get_weather(
    latitude: Annotated[float, "Latitude coordinate"],
    longitude: Annotated[float, "Longitude coordinate"],
) -> dict:
    try:
        data = fetch_weather(latitude, longitude)
        current_vars = data.get("current", {})

        return {
            "temperature": {
                "current": current_vars.get("temperature_2m"),
                "feelsLike": current_vars.get("apparent_temperature"),
                "unit": "celsius",
            },
            "humidity": {
                "value": current_vars.get("relative_humidity_2m"),
                "unit": "percent",
            },
            "wind": {
                "speed": current_vars.get("wind_speed_10m"),
                "unit": "km/h",
            },
            "precipitation": {
                "total": current_vars.get("precipitation"),
                "rain": current_vars.get("rain"),
                "unit": "millimeters",
            },
            "conditions": {
                "isDay": current_vars.get("is_day") == 1,
                "dayNight": "day"
                if current_vars.get("is_day") == 1
                else "night",
            },
        }
    except requests.HTTPError as e:
        raise Exception(f"Error getting weather: {e}")


def fetch_weather(latitude: float, longitude: float) -> dict:
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        query = {
            "latitude": latitude,
            "longitude": longitude,
            "current": ",".join(
                [
                    "temperature_2m",
                    "relative_humidity_2m",
                    "apparent_temperature",
                    "is_day",
                    "precipitation",
                    "rain",
                    "wind_speed_10m",
                ]
            ),
        }
        response = requests.get(url, params=query)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.HTTPError as e:
        raise Exception(f"Error getting weather: {e}")
    except Exception as e:
        raise Exception(f"Error getting weather: {e}")


if __name__ == "__main__":
    mcp.run()
