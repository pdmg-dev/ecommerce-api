# app/utils/auth.py

from datetime import datetime, timedelta
from typing import Union

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.settings import get_settings

settings = get_settings()

# password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# =========================
# Password Hashing
# =========================


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# =========================
# JWT Token Functions
# =========================


def create_access_token(data: dict, expires_delta: Union[int, None] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=expires_delta or settings.access_token_expire_minutes
    )
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
        )
        return payload
    except JWTError:
        raise ValueError("Invalid or expired token")
