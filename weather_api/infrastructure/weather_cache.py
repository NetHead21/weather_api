from datetime import datetime, timedelta
from typing import Optional, Tuple
from cachetools import TTLCache

from utils.format_data import format_values

lifetime_in_hours: float = 1.0
__cache = TTLCache(maxsize=100, ttl=timedelta(hours=lifetime_in_hours).total_seconds())


def __create_key(city_info: dict) -> Tuple:  # 86
    required_keys = ["city", "country", "units"]
    for key in required_keys:
        if city_info.get(key) is None:
            raise ValueError(f"{key} is required.")

    state = city_info.get("state", "")
    city_info["state"] = state
    return format_values(city_info, list(city_info.keys()))


def get_weather(city_info: dict) -> Optional[dict]:  # 99
    key: tuple = __create_key(city_info)
    return __cache.get(key)


def __clean_out_of_date() -> None:
    global __cache
    __cache = {
        key: data
        for key, data in __cache.items()
        if (datetime.now() - data.get("time")) / timedelta(minutes=60)
        <= lifetime_in_hours
    }


def set_weather(city_info: dict, value: dict) -> None:
    key: tuple = __create_key(city_info)
    data = {
        "time": datetime.now(),
        "value": value,
    }
    __cache[key] = data
    __clean_out_of_date()
