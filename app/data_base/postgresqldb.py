
import os
from dotenv import load_dotenv

load_dotenv()

class PostgresqlDataBase():
    dbname = None
    user = None
    password = None
    host = None
    port = None

    def __init__(self):
        self.dbname = os.getenv("DB_NAME", "test_tkinter")
        self.user = os.getenv("DB_USER", "api_user")
        self.password = os.getenv("DB_PASSWORD", "securepassword")
        self.host = os.getenv("DB_HOST", "localhost")
        self.port = os.getenv("DB_PORT", "5432")
    
    @property
    def __dbname(self):
        return self.dbname
    
    @property
    def __host(self):
        return self.host
    
    def get_url_postgresql(self):
        """Crear la URL de conexión a la base de datos"""
        return f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}"
    