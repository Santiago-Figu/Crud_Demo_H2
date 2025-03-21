import os
from dotenv import load_dotenv
from fastapi import FastAPI
from app.routers.h2_routers import router as h2_router
from app.routers.test_connection_routers import router as test_router
from app.routers.user_routers import router as user_router
from app.routers.auth_routers import router as auth_router

# Cargar variables desde el archivo .env
load_dotenv()

# Inicializar la aplicación FastAPI
app = FastAPI(
    title="Demo de FastAPI con gestión de bases de datos H2 (SQLite) y PostgreSQL",
    description="Conjunto de apis para proceso de selección de la vacante Python Backend Developer Sr",
    version="1.1.0"
)

# Obtener el prefijo principal de las API´s
API_PREFIX = os.getenv("API_PREFIX", "/demo/api")

# Incluir los routers
app.include_router(auth_router, prefix= API_PREFIX)
app.include_router(test_router, prefix=API_PREFIX)
app.include_router(h2_router, prefix=API_PREFIX)
app.include_router(user_router, prefix=API_PREFIX)


if __name__ == "__main__":
    ##########Para asegurar la ejecución de Pytest##################
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
