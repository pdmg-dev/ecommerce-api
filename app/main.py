# app/main.py

from fastapi import FastAPI
from app.core.settings import get_settings
from app.db.init_db import init_db


settings = get_settings()

app = FastAPI(title=settings.app_name, debug=settings.debug)
init_db()


@app.get("/")
def read_root():
    return {
        "message": f"{settings.app_name} is up",
        "debug_mode": settings.debug
    }
