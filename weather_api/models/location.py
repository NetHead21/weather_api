from typing import Optional

import fastapi
from pydantic import BaseModel

router = fastapi.APIRouter()


class Location(BaseModel):
    city: str
    state: Optional[str] = None
    country: str = "US"
