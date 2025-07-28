# app/core/dependencies.py

from fastapi import Depends
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.security import oauth2_scheme
from app.db.deps import get_db
from app.models.user import User
from app.repositories.cart import CartRepository
from app.repositories.order import OrderRepository
from app.repositories.product import ProductRepository
from app.repositories.user import UserRepository
from app.services.cart import CartService
from app.services.order import OrderService
from app.services.payment import PaymentService
from app.services.product import ProductService
from app.services.user import UserService
from app.utils import exceptions
from app.utils.auth import decode_access_token


# User Dependencies
def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(user_repository)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repository: UserRepository = Depends(get_user_repository),
) -> User:
    try:
        payload = decode_access_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise exceptions.unauthorized("Invalid token")

        user = user_repository.get_by_email(email)
        if not user:
            raise exceptions.not_found("User not found")

        return user

    except JWTError:
        raise exceptions.unauthorized("Invalid or expired token")


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_admin:
        raise exceptions.forbidden("Admin privileges required")
    return current_user


# Product Dependencies
def get_product_repository(db: Session = Depends(get_db)):
    return ProductRepository(db)


def get_product_service(
    product_repository: ProductRepository = Depends(get_product_repository),
):
    return ProductService(product_repository)


# Cart Dependencies
def get_cart_repository(db: Session = Depends(get_db)):
    return CartRepository(db)


def get_cart_service(
    cart_repository: CartRepository = Depends(get_cart_repository),
    product_repository: ProductRepository = Depends(get_product_repository),
):
    return CartService(cart_repository, product_repository)


# Payment Dependencies
def get_payment_service(cart_repository: CartRepository = Depends(get_cart_repository)):
    return PaymentService(cart_repository)


# Order Dependencies
def get_order_repository(db: Session = Depends(get_db)):
    return OrderRepository(db)


def get_order_service(
    order_repository: OrderRepository = Depends(get_order_repository),
):
    return OrderService(order_repository)
