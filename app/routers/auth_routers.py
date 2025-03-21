from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.auth.jwt import TokenJwt
from app.models.user import User
from app.config.configPostgresql import get_db
from app.schemas.token import LoginResponse
from app.schemas.user import UserFind

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=LoginResponse)
def login(form_data: UserFind, db: Session = Depends(get_db)):
    """Genera un token JWT si las credenciales son válidas."""
    # Busca el usuario por username o email
    db_user = db.query(User).filter(
        or_(
            User.username == form_data.username_email,
            User.email == form_data.username_email
        )
    ).first()

    # Verifica si el usuario existe
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    # Verifica si la contraseña es correcta
    if not db_user.check_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Contraseña incorrecta"
        )

    # Genera el token JWT
    token_data = {
        "sub": str(db_user.id),  # Subject (usuario)
        "username": db_user.username,
        "email": db_user.email
    }

    auth = TokenJwt()

    token = auth.create_access_token(token_data)

    auth.get_tokenJwt(token['access_token'])

    return token


# folio: LS94 Miercoles 9 de marzo, salon mexica, hotel gama xalapa, salón mexica, de 6 a 9 pm