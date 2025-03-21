from fastapi import APIRouter, HTTPException, Depends, Query, status
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.auth.jwt import TokenJwt, get_token
from app.config.configPostgresql import get_db
from app.models.user import User, CurrentUser, get_current_user
from app.schemas.user import UserCreate, UserDeleteResponse, UserFind, UserResponse, UserUpdateMail, UserUpdateResponse

from bcrypt import hashpw, gensalt

router = APIRouter(prefix="/users", tags=["Users PostgreSQL"])

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Registra un nuevo usuario."""
    # Verifica si el usuario ya existe por username o email

    db_user = db.query(User).filter(
        or_(
            User.username == user.username,
            User.email == user.email
        )
    ).first()

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso.")
        if db_user.email == user.email:
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

@router.post("/find", response_model=UserResponse)
def get_user(user: UserFind, db: Session = Depends(get_db), token: str = Depends(get_token)):
    """Devuelve los datos del usuario si esta registrado"""

    token_jwt = TokenJwt()
    payload, error = token_jwt.validate_token(token)

    if error:
        if error == "Token expirado":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expirado"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )
    
    # Busca los datos del usuario
    db_user = db.query(User).filter(
        or_(
            User.username == user.username_email,
            User.email == user.username_email
        )
    ).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Verificar que la contraseña sea la misma
    if not db_user.check_password(user.password):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")    
    
    # Devulve los datos del usuario
    return db_user

# Este metodo no es recomendado cuando se usan contraseñas, dado a que la información enviada por URL se almacena en el servidor o en el historial del navegador
# Se mantiene código como muestra de implementación con get
 
# @router.get("/find", response_model=UserResponse)
# def get_user(
#     username_email: str = Query(default="Jhondoe | johndoe@example.com", description="Username o email del usuario"),
#     password: str = Query(default = "securepassword", description = "Contraseña del usuario"),
#     db: Session = Depends(get_db)
# ):
#     """Devuelve los datos del usuario si está registrado y las credenciales son válidas."""
#     # Busca los datos del usuario
#     db_user = db.query(User).filter(
#         or_(
#             User.username == username_email,
#             User.email == username_email
#         )
#     ).first()

#     if not db_user:
#         raise HTTPException(status_code=404, detail="Usuario no encontrado")

#     # Verificar que la contraseña sea la misma
#     if not db_user.check_password(password):
#         raise HTTPException(status_code=401, detail="Contraseña incorrecta")

#     # Devuelve los datos del usuario
#     return db_user

@router.put("/update/mail", response_model=UserUpdateResponse)
def update_user(user:UserUpdateMail, db: Session = Depends(get_db)):
    """Actualiza el email del usuario"""
    db_user = db.query(User).filter(
        or_(
            User.username == user.username,
            User.email == user.current_email
        )
    ).first()

    if not db_user:
        raise HTTPException (status_code=404, detail="Usuario no se encuntra registrado, verifique los datos")
    
    # Verificar que la contraseña sea la misma
    # Todo: realizar validación de token para evitar pedir este dato directamente
    if not db_user.check_password(user.password):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta, no es posible actualizar los datos")
    
    # actualizar datos
    db_user.email = user.new_email
    db.commit()
    db.refresh(db_user)
    return {"message": "Email actualizado correctamente"}

@router.delete("/delete/user", response_model=UserDeleteResponse)
def delete_user(user:UserFind, db: Session = Depends(get_db)):
    """Elimina el usuario ingresado"""

    db_user = db.query(User).filter(
        or_(
            User.username == user.username_email,
            User.email == user.username_email
        )
    ).first()

    if not db_user:
        raise HTTPException (status_code=404, detail="Usuario no se encuntra registrado, verifique los datos")
    
    # Elimina el usuario
    db.delete(db_user)
    db.commit()
    
    return {"message": "Usuario eliminado correctamente"}

@router.get("/protected")
def protected_route(token: str = Depends(get_token)):
    """Ruta protegida que requiere autenticación."""
    token_jwt = TokenJwt()
    payload, error = token_jwt.validate_token(token)

    if error:
        if error == "Token expirado":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expirado"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )

    return {
        "message": "Acceso concedido",
        "user_info": payload
    }