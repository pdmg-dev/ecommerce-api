# app/db/init_db.py

from app.db import Base, engine
from app.models import user, product, cart_item, order  # ensure model is imported

def init_db():
    Base.metadata.create_all(bind=engine)
