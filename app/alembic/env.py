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
sqlalchemy_url = PostgresqlDataBase().get_url_postgresql()

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

def include_object(object, name, type_, reflected, compare_to):
    """Filtra los objetos del esquema deseado"""
    if hasattr(object, 'schema'):
        return object.schema == PostgresqlDataBase()._schema
    return True

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        version_table_schema=PostgresqlDataBase()._schema,
        include_schemas=True,  
        include_object=include_object  # Filtro para esquema
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        # Crea el esquema si no existe
        try:
            connection.execute(f"CREATE SCHEMA IF NOT EXISTS {PostgresqlDataBase()._schema}")
        except:
            print("No tiene permisos para ejecutar esta acción")
        
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            version_table_schema=PostgresqlDataBase()._schema,
            include_schemas=True,  # Debe ser True en ambos modos
            include_object=include_object  # Filtramos por esquema
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()