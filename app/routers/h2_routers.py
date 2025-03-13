# app/routers/h2_routes.py
from fastapi import APIRouter, HTTPException
from app.controller.insumosController import (
    create_insumo, create_table, get_insumos, get_insumo, update_insumo, delete_insumo
)
from app.models.insumos import Alimento, Bebida
from pydantic import BaseModel
from typing import Optional, Literal

# Crear un router para H2
router = APIRouter(prefix="/h2", tags=["Insumos con H2"])

# Modelo para la creación de insumos
class InsumoCreate(BaseModel):
    nombre: str
    descripcion: str
    estatus: Literal["Pendiente", "Preparando", "Entregado"]
    comentarios: Optional[str] = None
    estrellas: Optional[int] = 1  # Calificación del 1 al 5
    tipo: Literal["Alimento", "Bebida"]

# Rutas para H2
@router.post("/insumos")
def create_insumo_endpoint(insumo: InsumoCreate):
    """Crea un nuevo Alimento o Bebida."""
    if insumo.tipo not in ["Alimento", "Bebida"]:
        raise HTTPException(status_code=400, detail="Tipo de insumo no permitido. Debe ser 'Alimento' o 'Bebida'.")
    status, message, data = create_insumo(insumo)
    if not status:
        raise HTTPException(status_code=500, detail=message)
    return {"status": status, "message": message, "data": data}

@router.get("/insumos")
def get_all_insumos(tipo: Optional[str] = None):
    """Obtiene todos los Insumos (Alimentos y Bebidas)."""
    status, message, data = get_insumos(tipo)
    if not status:
        raise HTTPException(status_code=500, detail=message)
    return {"status": status, "message": message, "data": data}

@router.get("/insumos/{id}")
def get_insumo_endpoint(id: int):
    """Obtiene un Insumo por ID."""
    status, message, data = get_insumo(id)
    if not status:
        raise HTTPException(status_code=404, detail=message)
    return {"status": status, "message": message, "data": data}

@router.put("/insumos/{id}")
def update_insumo_endpoint(id: int, insumo: InsumoCreate):
    """Actualiza un Insumo por ID."""
    status, message = update_insumo(id, insumo)
    if not status:
        raise HTTPException(status_code=404, detail=message)
    return {"status": status, "message": message}

@router.delete("/insumos/{id}")
def delete_insumo_endpoint(id: int):
    """Elimina un Insumo por ID."""
    status, message = delete_insumo(id)
    if not status:
        raise HTTPException(status_code=404, detail=message)
    return {"status": status, "message": message}