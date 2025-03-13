import sys
from pathlib import Path

from app.data_base.postgresqldb import PostgresqlDataBase

# Agregar la ruta del proyecto a sys.path para ejecu
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

# Imports por defecto
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Nota: Importar los modelos para que se registren en la metadata, es necesario para que alembic los detecte al ejecutar las migraciones
from app.models.user import User

# Importa la clase Base para los modelos de SQLAlchemy que usara target_metadata
# Nota: Base debe estar declarado como variable publica o alembic no puede reconocerlo

from app.config.configPostgresql import Base

# El archivo base de documentación incluye estos valores pero solo se usan para construir la url

# DB_USER = os.getenv("DB_USER")
# DB_PASSWORD = os.getenv("DB_PASSWORD")
# DB_HOST = os.getenv("DB_HOST")
# DB_PORT = os.getenv("DB_PORT")
# DB_NAME = os.getenv("DB_NAME")

# Construir URL de conexión
sqlalchemy_url = PostgresqlDataBase().__get_url_postgresql()

# Configurar el objeto Alembic Config
config = context.config

# Configurar la URL de SQLAlchemy
config.set_main_option("sqlalchemy.url", sqlalchemy_url)

# Configurar el logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Configurar target_metadata
# attribute_db = PostgreSQLSettings("costos_ventas").base
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Ejecutar migraciones en modo 'offline'.

    En este modo, no se requiere una conexión a la base de datos.
    Las llamadas a context.execute() emiten el SQL generado a la salida del script.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        version_table_schema='costos_ventas',  # Especificar el esquema para alembic_version
        include_schemas=False,  # Incluir otros esquemas en las migraciones
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Ejecutar migraciones en modo 'online'.

    En este modo, se requiere una conexión a la base de datos.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            version_table_schema='costos_ventas',  # Especificar el esquema para alembic_version
            include_schemas=True,  # Incluir otros esquemas en las migraciones
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()