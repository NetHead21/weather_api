from typing import Optional
import httpx
from infrastructure import weather_cache

api_key: Optional[str] = None


async def get_report(
    city: str, state: Optional[str], country: Optional[str], units: str
) -> str:
    city_info: dict = {
        "city": city,
        "state": state,
        "country": country,
        "units": units,
    }

    if forecast := weather_cache.get_weather(city_info):
        return forecast

    q = ",".join(filter(None, (city_info[key] for key in ["city", "state", "country"])))

    url = f"https://api.openweathermap.org/data/2.5/weather?q={q}&appid={api_key}&units={units}"

    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()

    return await process_response(city_info, resp)


async def process_response(city_info: dict, resp):
    data = resp.json()
    weather_cache.set_weather(city_info, data)
    return data["main"]
