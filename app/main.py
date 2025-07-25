from fastapi import FastAPI
from app.core.settings import get_settings

settings = get_settings()

app = FastAPI(title=settings.app_name, debug=settings.debug)

@app.get("/")
def read_root():
    return {
        "message": f"{settings.app_name} is up",
        "debug_mode": settings.debug
    }
