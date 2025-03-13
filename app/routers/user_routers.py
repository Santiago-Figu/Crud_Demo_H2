from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.config.configPostgresql import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse

from bcrypt import hashpw, gensalt

router = APIRouter(prefix="/users", tags=["Users PostgreSQL"])

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Registra un nuevo usuario."""
    # Verifica si el usuario ya existe
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso.")

    # Verifica si el correo ya está registrado
    db_email = db.query(User).filter(User.email == user.email).first()
    if db_email:
        raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado.")

    # Crea un nuevo usuario
    new_user = User(username=user.username, email=user.email)
    new_user.set_password(user.password)  # Cifra la contraseña

    # Guarda el usuario en la base de datos
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Devuelve el usuario sin la contraseña
    return new_user