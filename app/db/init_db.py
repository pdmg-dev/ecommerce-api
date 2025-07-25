# app/db/init_db.py

from app.db import Base, engine
from app.models import (cart_item, order, product,  # ensure model is imported
                        user)


def init_db():
    Base.metadata.create_all(bind=engine)
