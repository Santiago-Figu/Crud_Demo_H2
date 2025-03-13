import sys
from pathlib import Path

# Agregar la ruta del proyecto a sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
import os
import pytest
from app.config.logger import Logger as LoggerConfig

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
logger = LoggerConfig().get_logger()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_call(item):
    logger.warning(f"Iniciando la prueba: {item.name}")
    outcome = yield
    result = "Prueba completada correctamente" if outcome.excinfo is None else "Falló la ejecución de la prueba"
    logger.info(f"Resultado de {item.name}: {result}")
