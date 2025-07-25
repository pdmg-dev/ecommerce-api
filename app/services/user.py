# app/services/user.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.schemas.user import UserCreate, UserLogin
from app.schemas.token import Token
from app.schemas.user import UserRead
from app.repositories.user import UserRepository
from app.utils.auth import hash_password, verify_password, create_access_token

class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def register_user(self, user_data: UserCreate) -> UserRead:
        existing_user = self.repo.get_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        hashed_pw = hash_password(user_data.password)
        user = self.repo.create(user_data, hashed_pw)

        return UserRead.model_validate(user)

    def authenticate_user(self, credentials: UserLogin) -> Token:
        user = self.repo.get_by_email(credentials.email)
        if not user or not verify_password(credentials.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        access_token = create_access_token({"sub": user.email})
        return Token(access_token=access_token)
