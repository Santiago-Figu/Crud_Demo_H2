from fastapi import APIRouter, HTTPException, Depends, Query, status
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.auth.jwt import TokenJwt, get_token
from app.config.configPostgresql import get_db
from app.config.logger import LoggerConfig
from app.models.user import User, CurrentUser, get_current_user
from app.schemas.user import UserCreate, UserDeleteResponse, UserFind, UserResponse, UserUpdateMail, UserUpdateResponse

from bcrypt import hashpw, gensalt

router = APIRouter(prefix="/users", tags=["Users PostgreSQL"])

# obtener el logger
logger = LoggerConfig(file_name='user_routers',debug=True).get_logger()

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Registra un nuevo usuario."""
    # Verifica si el usuario ya existe por username o email
    logger.info('Registrando nuevo usuario')
    db_user = db.query(User).filter(
        or_(
            User.username == user.username,
            User.email == user.email
        )
    ).first()

    if db_user:
        if db_user.username == user.username:
            message = "El nombre de usuario ya está en uso."
            logger.warning(message)
            raise HTTPException(status_code=400, detail=message)
        if db_user.email == user.email:
            message = "El correo electrónico ya está registrado."
            logger.warning(message)
            raise HTTPException(status_code=400, detail=message)

    # Crea un nuevo usuario
    new_user = User(username=user.username, email=user.email)
    new_user.set_password(user.password)  # Cifra la contraseña

    # Guarda el usuario en la base de datos
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logger.info('Usuario registrado con correctamente!!')
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
    logger.info('Buscando Usuario en la BD')
    db_user = db.query(User).filter(
        or_(
            User.username == user.username_email,
            User.email == user.username_email
        )
    ).first()

    if not db_user:
        message = "Usuario no encontrado, verificar datos."
        logger.warning(message)
        raise HTTPException(status_code=404, detail=message)
    
    # Verificar que la contraseña sea la misma
    if not db_user.check_password(user.password):
        message = "Contraseña incorrecta."
        logger.warning(message)
        raise HTTPException(status_code=401, detail=message)    
    
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
def update_user_email(user: UserUpdateMail, db: Session = Depends(get_db), token: str = Depends(get_token)):
    """Actualiza el email del usuario"""
    
    logger.info('Iniciando actualización de email...')
    
    # Validar token
    token_jwt = TokenJwt()
    _, error = token_jwt.validate_token(token)
    
    if error:
        logger.error(f"Error de autenticación: {error}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error
        )
    
    if user.username:
        logger.info(f"Buscando usuario por username: {user.username}")
        db_user = db.query(User).filter(User.username == user.username).first()
        search_criteria = f"username: {user.username}"
    else:
        logger.info(f"Buscando usuario por email: {user.current_email}")
        db_user = db.query(User).filter(User.email == user.current_email).first()
        search_criteria = f"email: {user.current_email}"
    
    # Verificar si el usuario existe
    if not db_user:
        message = f"Usuario no encontrado con {search_criteria}"
        logger.error(message)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=message
        )
    
    # Verificar que el current_email coincida si se proporcionó
    if user.current_email and db_user.email != user.current_email:
        message = "El email actual no coincide con el registrado"
        logger.error(message)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )
    
    # Actualizar email
    try:
        logger.info(f"Actualizando email de {db_user.username} de {db_user.email} a {user.new_email}")
        db_user.email = user.new_email
        db.commit()
        db.refresh(db_user)
        
        logger.info("Email actualizado correctamente")
        return {"message": "Email actualizado correctamente"}
    
    except Exception as e:
        db.rollback()
        logger.error(f"Error al actualizar email: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al actualizar el email"
        )

@router.delete("/delete/user", response_model=UserDeleteResponse)
def delete_user(user: UserFind, db: Session = Depends(get_db), token: str = Depends(get_token)
):
    """Elimina el usuario del sistema"""
    
    logger.info('Iniciando proceso de eliminación de usuario')
    
    # Validar token JWT
    token_jwt = TokenJwt()
    _, error = token_jwt.validate_token(token)
    
    if error:
        logger.error(f"Error de autenticación: {error}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error
        )
    
    logger.info(f"Buscando usuario por username o email: {user.username_email}")
    
    try:
        # Buscar usuario (manteniendo el OR como solicitaste)
        db_user = db.query(User).filter(
            or_(
                User.username == user.username_email,
                User.email == user.username_email
            )
        ).first()

        if not db_user:
            message = f"Usuario no encontrado con el criterio: {user.username_email}"
            logger.error(message)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=message
            )
        
        logger.info(f"Usuario encontrado - ID: {db_user.id}, Username: {db_user.username}, Email: {db_user.email}")
        
        # Eliminar usuario
        db.delete(db_user)
        db.commit()
        
        logger.info(f"Usuario eliminado correctamente - ID: {db_user.id}")
        return {"message": "Usuario eliminado correctamente"}
    
    except HTTPException:
        raise  # Re-lanzamos las excepciones HTTP que ya habíamos capturado
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error al eliminar usuario: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al eliminar el usuario"
        )

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