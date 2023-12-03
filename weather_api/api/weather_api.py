from typing import Optional, List

import fastapi
from fastapi import Depends

from models.location import Location
from services import openweather_service, report_service
from models.validatiaon_error import ValidationError
from models.reports import Report

from models.reports import ReportSubmittal

router = fastapi.APIRouter()


@router.get("/api/weather/{city}")
async def weather(loc: Location = Depends(), units: Optional[str] = "metric"):
    try:
        return await openweather_service.get_report_async(
            loc.city, loc.state, loc.country, units
        )
    except ValidationError as ve:
        return fastapi.Response(content=ve.error_msg, status_code=ve.status_code)
    except Exception as x:
        return fastapi.Response(content=str(x), status_code=500)


@router.get("/api/reports", name="all_reports", response_model=List[Report])
async def reports_get() -> List[Report]:
    await report_service.add_report("Eartquake", Location(city="Surigao"))
    await report_service.add_report("Bombing Incident", Location(city="Marawi"))
    return await report_service.get_reports()


@router.post("/api/reports", name="add_reports", status_code=201, response_model=Report)
async def reports_post(submitted_report: ReportSubmittal) -> Report:
    description = submitted_report.description
    location = submitted_report.location
    return await report_service.add_report(description=description, location=location)
