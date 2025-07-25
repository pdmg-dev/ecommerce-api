# app/schemas/user.py

from pydantic import BaseModel, EmailStr


# For incoming registration/login requests
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# For outgoing (response to client)
class UserRead(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    is_admin: bool

    class Config:
        from_attributes = True  # Needed for SQLAlchemy model conversion
