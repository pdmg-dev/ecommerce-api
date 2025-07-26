# app/core/dependencies.py

from fastapi import Depends
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.security import oauth2_scheme
from app.db.deps import get_db
from app.models.user import User
from app.repositories.user import UserRepository
from app.utils.auth import decode_access_token
from app.utils.exception import Exception


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    try:
        payload = decode_access_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise Exception.unauthorized("Invalid token")

        user = UserRepository(db).get_by_email(email)
        if not user:
            raise Exception.not_found("User not found")

        return user

    except JWTError:
        raise Exception.unauthorized("Invalid or expired token")

def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_admin:
        raise Exception.forbidden("Admin privileges required")
    return current_user
