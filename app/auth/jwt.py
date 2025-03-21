import sys
from pathlib import Path

from fastapi import Depends

# Agregar la ruta del proyecto a sys.path para ejecución en local
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from cryptography.fernet import Fernet
from app.config.logger import Logger as LoggerConfig
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# obtener el logger
logger = LoggerConfig().get_logger()

# Cargar variables desde el archivo .env
load_dotenv()

# Crear una instancia de HTTPBearer
security = HTTPBearer()

class TokenJwt:

    def __init__(self):

        # Clave secreta para firmar los tokens JWT
        self.SECRET_KEY = os.getenv("SECRET_KEY")
        if not self.SECRET_KEY:
            raise ValueError("SECRET_KEY no está configurada.")
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 10  # El token expira en 10 minutos

        # Clave para cifrar el token JWT
        self.FERNET_KEY = os.getenv("FERNET_KEY")
        # Verificar que la clave sea válida
        if not self.FERNET_KEY:
            raise ValueError("FERNET_KEY no está configurada.")
        self.cipher_suite = Fernet(self.FERNET_KEY)

    def create_access_token(self,data: dict):
        """Genera un token JWT con la información del usuario."""
        token=None
        try:
            logger.info("Generando token de acceso")
            to_encode = data.copy()
            expire = datetime.now(timezone.utc) + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
            to_encode.update({"exp": expire})
            encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
            
            # Cifra el token JWT
            encrypted_token = self.cipher_suite.encrypt(encoded_jwt.encode())
            token = encrypted_token.decode()
        except Exception as e:
            logger.error(f"Ocurrio un error al generar el Token: {e}")
        finally:
            return {"access_token": str(token), "token_type": "bearer"}
        
    def get_tokenJwt(self, token):
        jwt_token = self.cipher_suite.decrypt(token).decode()
        print("tokenJwt", jwt_token)

    def validate_token(self, token: str):
        """Valida el token JWT y devuelve la información del usuario o un error."""
        payload = None
        error = None
        try:
            # Descifra el token JWT
            decrypted_token = self.cipher_suite.decrypt(token.encode()).decode()
            # Decodifica el token JWT
            payload = jwt.decode(decrypted_token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            # Verifica si el token ha expirado
            expire = payload.get("exp")
            if expire is None or datetime.fromtimestamp(expire) < datetime.now(timezone.utc):
                error = "Token expirado"
        except JWTError as e:
            logger.error(f"Error al validar el token: {e}")
            error = "Token inválido"
        finally:
            return payload, error

        
    @staticmethod
    def generate_fernet_key():
        # Generar una clave válida
        FERNET_KEY = Fernet.generate_key()
        print(FERNET_KEY)
        
# Función para extraer el token de las credenciales de autorización
def get_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Extrae el token de las credenciales de autorización."""
    return credentials.credentials

if __name__ == "__main__":
    TokenJwt.generate_fernet_key()
