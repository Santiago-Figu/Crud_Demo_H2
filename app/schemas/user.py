from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    username: str = "Jhondoe"
    password: str = "securepassword"
    email: EmailStr = "johndoe@example.com"

class UserResponse(BaseModel):
    id: int = 0
    username: str = "Jhondoe"
    email: str = "johndoe@example.com"

    class Config:
        from_attributes = True  # Permite la conversión automática de modelos SQLAlchemy a Pydantic