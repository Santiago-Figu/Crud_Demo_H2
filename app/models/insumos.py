from pydantic import BaseModel
from typing import Optional

class Insumo(BaseModel):
    """Clase base para los insumos, ya sean Alimentos y Bebidas."""
    nombre: str
    descripcion: str
    estatus: str  # Ejemplo: "Pendiente", "Preparando", "Entregado"
    comentarios: Optional[str] = None
    estrellas: Optional[int] = None  # Calificación del 1 al 5

class Alimento(Insumo):
    """Modelo para Alimentos."""
    tipo: str = "Alimento"

class Bebida(Insumo):
    """Modelo para Bebidas."""
    tipo: str = "Bebida"
