import uuid
from datetime import datetime
from typing import List

from models.reports import Report
from models.location import Location

__reports: List[Report] = []


async def get_reports() -> List[Report]:
    return list(__reports)


async def add_report(description: str, location: Location) -> Report:
    now = datetime.now()
    report = Report(
        id=str(uuid.uuid4()),
        location=location,
        description=description,
        created_date=now,
    )

    __reports.append(report)
    __reports.sort(key=lambda r: r.created_date, reverse=True)
    return report
