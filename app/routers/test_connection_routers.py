# app/routers/test_connection_routes.py
from fastapi import APIRouter

from app.config.configPostgresql import test_connection
from app.config.configH2 import test_connection as test_db_h2

# Crear un router para los Test de conexión
router = APIRouter(prefix="/test/connection", tags=["Test DB"])


@router.get("/postgresql")
def test_connection_postgresql():
    """Verifica la conexión a la base de datos PostgreSQL."""
    message, status = test_connection()
    return {"message": message, "status": status}

# Ruta de prueba para H2
@router.get(f"/h2")
def test_connection_h2():
    """Verifica la conexión a la base de datos H2."""
    message, status = test_db_h2()
    return {"message": message, "status": status}
