from typing import Optional,Literal
from fastapi import FastAPI, HTTPException, Depends
from app.config.config import get_api_prefix, test_connection as test_db
from app.controller.insumos_controller import (
    create_insumo, create_table, get_insumos, get_insumo, update_insumo, delete_insumo
)
from app.models.insumos import Alimento, Bebida

from pydantic import BaseModel

# Inicializar la aplicación FastAPI con metadatos
app = FastAPI(
    title="API de testing para proceso de selección de la vacante Python Backend Developer Sr",
    description="Gestión de Alimentos y Bebidas usando FastAPI con H2 (SQLite).",
    version="1.0.0"
)

API_PREFIX = get_api_prefix()

########Models para Fastapi##########

class InsumoCreate(BaseModel):
    nombre: str
    descripcion: str
    estatus: Literal["Pendiente", "Preparando", "Entregado"]
    comentarios: Optional[str] = None
    estrellas: Optional[int] = 1  # Calificación del 1 al 5
    tipo: Literal["Alimento", "Bebida"]


#############################Test#################################################
@app.get(f"{API_PREFIX}/test_connection", tags=["Test"])
def test_connection():
    """Ejecuta la función test_connection para verificar que exista una correcta conexión con la base de datos"""
    message, status = test_db()
    return {"message": message, "status": status}

#############################DataBase##############################################

@app.post(f"{API_PREFIX}/create/database/demo", tags=["Gestión de Base de Datos"])
def create_database_demo():
    """Crea la base de datos y la tabla de insumos si no existen e inserta datos demo."""
    status,message = create_table()
    if status:
        return {"message": message}
    else:
        raise HTTPException(status_code=500, detail=message)


###################CRUD Principal############################
@app.post(f"{API_PREFIX}/insumos", tags=["Insumos"])
def create_insumo_endpoint(insumo: InsumoCreate):
    """Crea un nuevo Alimento o Bebida."""
    if insumo.tipo not in ["Alimento", "Bebida"]:
        raise HTTPException(status_code=400, detail="Tipo de insumo no permitido. Debe ser 'Alimento' o 'Bebida'.")
    status, message, data = create_insumo(insumo)
    if not status:
        raise HTTPException(status_code=500, detail=message)
    return {"status": status, "message": message, "data": data}

@app.get(f"{API_PREFIX}/insumos", tags=["Insumos"])
def get_all_insumos(tipo: Optional[str] = None):
    """Obtiene todos los Insumos (Alimentos y Bebidas) si se ingres el tipo puede filtrar por Alimento|Bebida."""
    status, message, data = get_insumos(tipo)

    if not status:
        raise HTTPException(status_code=500, detail=message)

    return {"status": status, "message": message, "data": data}

@app.get(f"{API_PREFIX}"+"/insumos/{id}", tags=["Insumos"])
def get_insumo_endpoint(id: int):
    """Obtiene un Insumo por ID."""
    status, message, data = get_insumo(id)

    if not status:
        raise HTTPException(status_code=404, detail=message)

    return {"status": status, "message": message, "data": data}

@app.put(f"{API_PREFIX}"+"/insumos/{id}", tags=["Insumos"])
def update_insumo_endpoint(id: int, insumo: InsumoCreate):
    """Actualiza un Insumo por ID."""
    status, message = update_insumo(id, insumo)
    if not status:
        raise HTTPException(status_code=404, detail=message)

    return {"status": status, "message": message}


@app.delete(f"{API_PREFIX}"+"/insumos/{id}", tags=["Insumos"])
def delete_insumo_endpoint(id: int):
    """Elimina un Insumo por ID."""
    status, message = delete_insumo(id)
    if not status:
        raise HTTPException(status_code=404, detail=message)

    return {"status": status, "message": message}


if __name__ == "__main__":
    ##########Para asegurar la ejecución de Pytest##################
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
