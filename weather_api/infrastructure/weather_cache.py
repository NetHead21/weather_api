from datetime import datetime, timedelta
from typing import Optional, Tuple
from cachetools import TTLCache


lifetime_in_hours: float = 1.0
__cache = TTLCache(maxsize=100, ttl=timedelta(hours=lifetime_in_hours).total_seconds())


def format_key(value: str) -> Optional[str]:
    return value.strip().lower() if value else None


# def format_keys(city_info: dict) -> tuple: #97
#     return (
#         format_key(city_info["city"]),
#         format_key(city_info["state"]),
#         format_key(city_info["country"]),
#         format_key(city_info["units"]),
#     )


def format_keys(city_info: dict) -> tuple:  # 98
    keys = ["city", "state", "country", "units"]
    return tuple(format_key(city_info[key]) for key in keys)


# def __create_key(city_info: dict) -> Tuple:  # sourcery skip: raise-specific-error
#     if (
#         city_info["city"] is None
#         or city_info["country"] is None
#         or city_info["units"] is None
#     ):
#         raise Exception("City, country and units are required.")

#     if city_info["state"] is None:
#         city_info["state"] = ""

#     return format_keys(city_info)


def __create_key(city_info: dict) -> Tuple:  # 86
    required_keys = ["city", "country", "units"]
    for key in required_keys:
        if city_info.get(key) is None:
            raise ValueError(f"{key} is required.")

    state = city_info.get("state", "")
    city_info["state"] = state

    return format_keys(city_info)


# def __create_key(city_info: dict) -> Tuple:  #
#     required_keys = ["city", "country", "units"]
#     if missing_keys := [key for key in required_keys if key not in city_info]:
#         raise ValueError(f"Missing required keys: {', '.join(missing_keys)}")
#     return format_keys(city_info)


# def get_weather(city_info: dict) -> Optional[dict]: # 81
#     key: tuple = __create_key(city_info)
#     data: dict = __cache.get(key)

#     if not data:
#         return None

#     last = data["time"]
#     if datetime.now() - last < timedelta(hours=lifetime_in_hours):
#         return data["value"]

#     del __cache[key]
#     return None


def get_weather(city_info: dict) -> Optional[dict]:  # 99
    key: tuple = __create_key(city_info)
    return __cache.get(key)


# def __clean_out_of_date() -> None:
#     for key, data in list(__cache.items()):
#         dt = datetime.now() - data.get("time")
#         if dt / timedelta(minutes=60) > lifetime_in_hours:
#             del __cache[key]


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
