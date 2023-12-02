from typing import Optional

import fastapi
from fastapi import Depends
from pydantic import BaseModel

from models.location import Location

from services import openweather_service

router = fastapi.APIRouter()


@router.get("/api/weather/{city}")
async def weather(loc: Location = Depends(), units: Optional[str] = "metric"):
    return await openweather_service.get_report(
        loc.city, loc.state, loc.country, units
    )
