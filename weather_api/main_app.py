from pathlib import Path
import json

import fastapi
import uvicorn
from starlette.staticfiles import StaticFiles
from services import openweather_service

from api import weather_api
from views import home

app = fastapi.FastAPI()


def configure():
    configure_routing()
    configure_api_keys()


def configure_api_keys():  # sourcery skip: raise-specific-error
    file = Path("settings.json").absolute()
    if not file.exists():
        print(f"WARNING: {file} file not found.")
        raise Exception("settings.json file not found.")

    with open(file) as fin:
        settings = json.load(fin)
        openweather_service.api_key = settings.get("api_key")


def configure_routing() -> None:
    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.include_router(home.router)
    app.include_router(weather_api.router)


if __name__ == "__main__":
    configure()
    uvicorn.run(app)
else:
    configure()
