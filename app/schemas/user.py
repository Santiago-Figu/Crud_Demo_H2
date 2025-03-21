from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    username: str = "Jhondoe"
    password: str = "securepassword"
    email: EmailStr = "johndoe@example.com"

class UserFind(BaseModel):
    username_email: str = "Jhondoe | johndoe@example.com"
    password: str = "securepassword"

class UserResponse(BaseModel):
    id: int = 0
    username: str = "Jhondoe"
    email: str = "johndoe@example.com"

    class Config:
        from_attributes = True  # Permite la conversión automática de modelos SQLAlchemy a Pydantic

class UserUpdateMail(BaseModel):
    username: str = "Jhondoe"
    password: str = "securepassword"
    current_email: EmailStr = "johndoe@example.com"
    new_email: EmailStr = "newjohndoe@example.com"

class UserUpdateResponse(BaseModel):
    message: str = "Datos actualizados correctamente"

class UserDeleteResponse(BaseModel):
    message: str = "usuario eliminado correctamente"