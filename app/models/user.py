from app.data_base.postgresqldb import PostgresqlDataBase
from bcrypt import gensalt, hashpw
from fastapi import Depends, HTTPException, status
from sqlalchemy import Column, Integer, String
from app.auth.jwt import TokenJwt
from app.config.configPostgresql import Base
from fastapi.security import OAuth2PasswordBearer

# Obtener la base declarativa
# attribute_db = PostgreSQLSettings("costos_ventas")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": PostgresqlDataBase()._schema}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=True)

    @property
    def _encoding(self):
        """Devuelve el metodo de encoding"""
        return 'utf-8'

    def set_password(self, password:str):
        """Cifra la contraseña antes de almacenarla"""
        self.password = hashpw(password.encode(self._encoding),gensalt()).decode(self._encoding)

    def check_password(self, password:str):
        "Verica que la contraseña ingresada sea la misma que la almacenada en base de datos"
        return hashpw(password.encode(self._encoding), self.password.encode(self._encoding)) == self.password.encode(self._encoding)

class CurrentUser:
    def __init__(self):
        self._name = None
        self._email = None
        # Configurar OAuth2PasswordBearer
        
    @property
    def name(self):
        """Obtener el nombre del usuario."""
        return self._name

    @property
    def email(self):
        """Obtener el email del usuario."""
        return self._email

    def set_data(self, user):
        """Establecer los datos del usuario."""
        if user and isinstance(user, User):  # Validar que user sea una instancia de User
            self._name = user.username
            self._email = user.email
        else:
            self._name = None
            self._email = None
    
# Dependencia para validar el token
def get_current_user(token: str = Depends(oauth2_scheme)):
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

    return payload

