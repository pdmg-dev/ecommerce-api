# app/api/auth.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin, UserRead
from app.schemas.token import Token
from app.services.user import UserService
from app.db.deps import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserRead, status_code=201)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.register_user(user_data)

@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.authenticate_user(credentials)
