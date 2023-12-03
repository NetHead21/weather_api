from typing import Optional


def format_value(value: str) -> Optional[str]:
    return value.strip().lower() if value else None


def format_values(values: dict, keys: list) -> tuple:  # 98
    return tuple(format_value(values[key]) for key in keys)
