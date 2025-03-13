from bcrypt import gensalt, hashpw
from sqlalchemy import Column, Integer, String
from app.config.configPostgresql import Base

# Obtener la base declarativa
# attribute_db = PostgreSQLSettings("costos_ventas")

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "costos_ventas"}

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

