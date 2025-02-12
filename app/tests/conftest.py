import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_call(item):
    print(f"Iniciando la prueba: {item.name}")
    outcome = yield
    result = "Prueba completada correctamente" if outcome.excinfo is None else "Falló la ejecución de la prueba"
    print(f"Resultado de {item.name}: {result}")
