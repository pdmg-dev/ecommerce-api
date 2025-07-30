# app/main.py

from fastapi import FastAPI

from app.api import auth, cart, order, payment, product, webhook
from app.core.settings import get_settings
from app.db.init_db import init_db

settings = get_settings()
app = FastAPI(title=settings.app_name, debug=settings.debug)

init_db()

app.include_router(auth.router)
app.include_router(product.router)
app.include_router(cart.router)
app.include_router(payment.router)
app.include_router(webhook.router)
app.include_router(order.router)


@app.get("/")
def root():
    return {"message": f"{settings.app_name} is up", "debug_mode": settings.debug}
