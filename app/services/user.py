# app/services/user.py

from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.token import EmailPayload, RefreshRequest, Token, TokenPair
from app.schemas.user import UserCreate, UserLogin, UserRead
from app.utils import auth, exceptions


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register_user(self, registration_data: UserCreate) -> UserRead:
        existing_user = self.user_repository.get_by_email(registration_data.email)
        if existing_user:
            raise exceptions.bad_request("Email already registered")

        hashed_password = auth.hash_password(registration_data.password)
        new_user = User(
            **registration_data.model_dump(exclude={"password"}),
            hashed_password=hashed_password
        )

        saved_user = self.user_repository.create(new_user)
        return UserRead.model_validate(saved_user)

    def authenticate_user(self, login_data: UserLogin) -> Token:
        user = self.user_repository.get_by_email(login_data.email)
        if not user or not auth.verify_password(
            login_data.password, hashed_password=user.hashed_password
        ):
            raise exceptions.unauthorized("Invalid email or password")

        access_token = auth.create_access_token({"sub": user.email})
        refresh_token = auth.create_refresh_token({"sub": user.email})
        return TokenPair(access_token=access_token, refresh_token=refresh_token)

    def refresh_access_token(self, refresh_request: RefreshRequest) -> TokenPair:
        try:
            payload = auth.decode_token(refresh_request.refresh_token)
            if payload.get("scope") != "refresh_token":
                raise exceptions.unauthorized("Invalid refresh token")

            email_payload = EmailPayload(email=payload.get("sub"))
            user = self.user_repository.get_by_email(email_payload.email)
            if not user or not user.is_active:
                raise exceptions.unauthorized("User no longer active")

            new_access_token = auth.create_access_token({"sub": email_payload.email})
            new_refresh_token = auth.create_refresh_token({"sub": email_payload.email})
            return TokenPair(
                access_token=new_access_token, refresh_token=new_refresh_token
            )

        except ValueError:
            raise exceptions.unauthorized("Expired or invalid refresh token")
