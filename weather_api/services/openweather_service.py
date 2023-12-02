from typing import Optional
import httpx

api_key: Optional[str] = None


async def get_report(
    city: str, state: Optional[str], country: Optional[str], units: str
) -> str:
    q = f"{city},{state},{country}" if state else f"{city},{country}"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={q}&appid={api_key}&units={units}"

    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()

    data = resp.json()
    return data["main"]
