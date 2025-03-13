import pytest
from fastapi.testclient import TestClient
from app.config.configH2 import get_api_prefix
from main import app
from app.controller.insumosController import create_insumo, delete_insumo
from app.models.insumos import Alimento

client = TestClient(app)

API_PREFIX = get_api_prefix()

@pytest.fixture
def setup_test_insumo():
    """Inserta un insumo de prueba."""
    insumo_test = Alimento(
        nombre="Pizza",
        descripcion="Pizza de pepperoni",
        estatus="Disponible",
        comentarios="Muy buena",
        estrellas=5,
        tipo="Alimento"
    )
    create_insumo(insumo_test)

    # Obtener el ID del insumo insertado
    response = client.get(f"{API_PREFIX}/insumos")
    data = response.json()["data"]
    test_id = next((insumo["id"] for insumo in data if insumo["nombre"] == "Pizza"), None)

    yield test_id

    if test_id:
        delete_insumo(test_id)

def test_get_insumos_api(setup_test_insumo):
    """Prueba si el endpoint GET /api/insumos/insumos devuelve datos correctamente."""
    response = client.get(f"{API_PREFIX}/insumos")

    assert response.status_code == 200
    json_response = response.json()

    assert json_response["status"] is True
    assert "message" in json_response
    assert "data" in json_response
    assert isinstance(json_response["data"], list)
    assert any(insumo["nombre"] == "Pizza" for insumo in json_response["data"])

def test_create_insumo_api():
    """Prueba si el endpoint POST /api/insumos crea un nuevo insumo correctamente y sigue el formato esperado."""

    new_insumo = {
        "nombre": "Jugo de Manzana",
        "descripcion": "Jugo natural sin azúcar",
        "estatus": "Pendiente",  # Ingresar solo un valor de los permitidos
        "comentarios": "Muy refrescante",
        "estrellas": 4,
        "tipo": "Bebida"  # Ingresar solo "Alimento" o "Bebida", no "Alimento|Bebida"
    }

    response = client.post(f"{API_PREFIX}/insumos", json=new_insumo)
    assert response.status_code == 200

    json_response = response.json()

    assert json_response["status"] is True
    assert "message" in json_response
    assert "data" in json_response
    assert isinstance(json_response["data"], dict)
    assert json_response["data"]["nombre"] == "Jugo de Manzana"
    assert json_response["data"]["tipo"] == "Bebida"

    # Verificar si se insertó en la BD
    response = client.get(f"{API_PREFIX}/insumos")
    json_response = response.json()

    assert any(insumo["nombre"] == "Jugo de Manzana" for insumo in json_response["data"])

    # Eliminar el objeto creado para el test
    insumo_id = next((insumo["id"] for insumo in json_response["data"] if insumo["nombre"] == "Jugo de Manzana"), None)
    if insumo_id:
        delete_insumo(insumo_id)

def test_create_insumo_invalid_type():
    """Prueba si la API rechaza un insumo con tipo incorrecto."""

    invalid_insumo = {
        "nombre": "Jugo de Manzana",
        "descripcion": "Jugo natural sin azúcar",
        "estatus": "Pendiente",
        "comentarios": "Muy refrescante",
        "estrellas": 4,
        "tipo": "Comida"  # No es un valor permitido en el modelo
    }

    response = client.post(f"{API_PREFIX}/insumos", json=invalid_insumo)
    #uso 422 por que fastapi se encarga de validar los datos con pydantic por lo que no devuelve el 400 o 402 por defecto
    assert response.status_code == 422

    json_response = response.json()
  
    assert "detail" in json_response
    assert isinstance(json_response["detail"], list)
    error_detail = json_response["detail"][0]
    assert "msg" in error_detail
    assert "should be 'Alimento' or 'Bebida'" in error_detail["msg"]



