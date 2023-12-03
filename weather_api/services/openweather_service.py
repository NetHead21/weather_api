from typing import Optional, Tuple
import httpx
from infrastructure import weather_cache

from models.validatiaon_error import ValidationError

from utils.format_data import format_value

api_key: Optional[str] = None


async def get_report_async(
    city: str, state: Optional[str], country: Optional[str], units: str
) -> str:
    city, state, country, units = validate_units(city, state, country, units)
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
        if resp.status_code != 200:
            raise ValidationError(resp.text, status_code=resp.status_code)

    return await process_response(city_info, resp)


async def process_response(city_info: dict, resp):
    data = resp.json()
    weather_cache.set_weather(city_info, data)
    return data["main"]


def validate_length(field_name: str, value: str, length: int) -> str:
    if len(value) != length:
        error = (
            f"Invalid {field_name}: {value}. It must be a {length} letter abbreviation."
        )
        raise ValidationError(status_code=400, error_msg=error)
    return value


def validate_units(
    city: str,
    state: Optional[str],
    country: Optional[str],
    units: str,
) -> Tuple[str, Optional[str], str, str]:
    fields = {
        "city": format_value(city),
        "country": format_value(country),
        "state": format_value(state),
        "units": format_value(units),
    }

    validate_length("country", fields["country"], 2)

    if fields["state"]:
        validate_length("state", fields["state"], 2)

    valid_units = {"standard", "metric", "imperial"}
    if fields["units"] not in valid_units:
        error = f"Invalid units '{fields['units']}', it must be one of {valid_units}."
        raise ValidationError(status_code=400, error_msg=error)

    return fields["city"], fields["state"], fields["country"], fields["units"]


if __name__ == "__main__":
    city = "Surigao"
    country = "PH"
    state = None
    units = "imperial"

    city, state, country, units = validate_units(city, state, country, units)
