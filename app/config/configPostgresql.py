import sys
from pathlib import Path

# Agregar la ruta del proyecto a sys.path para ejecución en local
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from app.data_base.postgresqldb import PostgresqlDataBase
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
from app.config.logger import LoggerConfig


# Cargar variables desde el archivo .env
load_dotenv()

# crear instancia del logger
logger = LoggerConfig(file_name='configPostgreSQL', debug=False).get_logger()

# crear instancia con la informaciíon para conexión a postgresql
# DB_CONFIG = PostgresqlDataBase()

# Crear la URL de conexión a la base de datos
DATABASE_URL = PostgresqlDataBase().get_url_postgresql()

# Crear motor de SQLAlchemy


if PostgresqlDataBase()._schema == None:
    logger.info('Inicializando sin schema asignado')
    engine = create_engine(DATABASE_URL)
else:
    logger.info('Inicializando con schema asignado')
    engine = create_engine(
        DATABASE_URL,
        connect_args={"options": f"-c search_path={PostgresqlDataBase()._schema}"}
    )

# Crear sesión local para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos de SQLAlchemy
Base = declarative_base()

# obtener el logger
logger = LoggerConfig().get_logger()


def get_db():
    """Genera una instancia de sesión para la base de datos."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def ensure_database():
    """Verifica si la base de datos existe y la crea si no existe."""
    from sqlalchemy import inspect

    inspector = inspect(engine)
    if not inspector.get_schema_names():
        Base.metadata.create_all(bind=engine)
        logger.info(f"Base de datos '{PostgresqlDataBase()._dbname}' y tablas creadas exitosamente.")
    else:
         logger.info(f"La base de datos '{PostgresqlDataBase()._dbname}' ya existe.")

def test_connection():
    """Prueba de conexión a la base de datos."""
    status = False
    message = ""
    try:
        # Obtener la conexión desde el engine
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            message= "Conexión a la base de datos exitosa."
            # status = f'{result.fetchone()}'
            status = True
    except SQLAlchemyError as e:
        message = f"Error en la conexión: {e}"
        logger.error(message)
    finally:
        return message, status

if __name__ == "__main__":
    message, status = test_connection()
    ensure_database()
    logger.info(message)
    logger.info(f"Resultado de la consulta: {status}")