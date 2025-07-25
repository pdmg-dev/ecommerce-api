# app/db/deps.py

from contextlib import contextmanager

from app.db import SessionLocal


# if using Depends in routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
