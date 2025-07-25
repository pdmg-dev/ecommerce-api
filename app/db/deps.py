# app/db/deps.py

from app.db import SessionLocal
from contextlib import contextmanager

# if using Depends in routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
