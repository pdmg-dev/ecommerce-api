# app/main.py

from fastapi import FastAPI
from app.core.settings import get_settings
from app.db.init_db import init_db
from app.api import auth, product, cart, order


settings = get_settings()
app = FastAPI(title=settings.app_name, debug=settings.debug)

init_db()

# include routes
app.include_router(auth.router)
app.include_router(product.router)
app.include_router(cart.router)
app.include_router(order.router)



@app.get("/")
def read_root():
    return {
        "message": f"{settings.app_name} is up",
        "debug_mode": settings.debug
    }
