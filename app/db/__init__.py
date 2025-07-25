# app/db/__init__.py

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.settings import get_settings

settings = get_settings()

engine = create_engine(
    settings.database_url,
    connect_args=(
        {"check_same_thread": False} if "sqlite" in settings.database_url else {}
    ),
    echo=settings.debug,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass
