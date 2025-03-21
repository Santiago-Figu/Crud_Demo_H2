from pydantic import BaseModel

class LoginResponse(BaseModel):
    access_token: str = "token"
    token_type: str = "bearer"
    