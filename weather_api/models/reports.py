from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from models.location import Location


class Report(BaseModel):
    description: str
    location: Location
    created_date: Optional[datetime]

class ReportSubmittal(Report):
    id: str
    created_date: Optional[datetime]
