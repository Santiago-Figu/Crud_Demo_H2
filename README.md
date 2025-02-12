# 🚀 API de Insumos con FastAPI y H2/SQLite 

## Descripción

Este proyecto consiste en un CRUD de API´s de testing desarrollada para el proceso de selección de la vacante Python Backend Developer Sr, en la cual se plantea un CRUD para gestionar insumos de alimentos y bebidas, almacenándolos en una base de datos **H2 con SQLite**.

Como tecnologías de desarrollo se ha utilizado **FastAPI**, **Pydantic** y **Uvicorn**, con pruebas unitarias en **pytest**, para probar la inserción de datos desde las funciones del controlador con **sqlite3**, inserción y validación de datos con **Pydantic** desde la api con **Uvicorn**.

---

## Requisitos

Antes de ejecutar el proyecto, asegúrate de tener:

✅ **Python 3.11+** instalado. 
✅ **Pip y virtualenv** instalados.
✅ **Java 11 o superior** (para H2).

---

## Instalación

1️⃣ **Clonar el repositorio:**

```sh
git clone https://github.com/tu_usuario/tu_repositorio.git
cd tu_repositorio
```

2️⃣ **Crear un entorno virtual e instalar dependencias:**

```sh
python -m venv env
source env/bin/activate  # En Windows: env\Scripts\activate
python -m pip install --upgrade pip #actualiza tu entorno
pip install -r requirements.txt
```

---

## Descarga de Drivers

### 🔹 **H2 Database Driver**

Para utilizar H2, descarga el driver desde: 🔗 [https://www.h2database.com/html/download.html](https://www.h2database.com/html/download.html)

Después de descargarlo, colócalo en:

```
app/DB/driver_h2/bin/h2-2.3.232.jar
```

### 🔹 **SQLite-JDBC Driver**

Para utilizar SQLite, descarga el driver desde: 🔗 [https://github.com/xerial/sqlite-jdbc](https://github.com/xerial/sqlite-jdbc)

Después de descargarlo, colócalo en:

```
app/DB/driver_sqlite/bin/sqlite-jdbc-3.41.2.jar
```

---

## Configuración

El proyecto utiliza variables de entorno para definir la base de datos:

📌 \*\*Configuración en \*\*\`\`:

```python
H2_JAR_PATH = "app/DB/driver_h2/bin/h2-2.3.232.jar"
DATABASE_URL = "jdbc:h2:file:./app/DB/test_db;AUTO_SERVER=TRUE"
```

Si prefieres SQLite:

```python
DATABASE_URL = "sqlite:///app/DB/test_db.sqlite"
```

---

## Ejecutar el Servidor

Para iniciar la API con **Uvicorn**, ejecuta:

```sh
uvicorn app.main:app
```
Si quieres que la API se recarge en automático al realizar cambios en el cófigo, ejecuta:

```sh
uvicorn app.main:app --reload
```

La Documentación de la API estará disponible en el: **Swagger UI de FastApi:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Rutas de la API para consumo por **POSTMAN** o tu **APP**

| Método   | Endpoint                          | Descripción                              |
| -------- | --------------------------------- | ---------------------------------------- |
| `GET`    | `/demo/api/test_connection`       | Verifica la conexión a la base de datos  |
| `POST`   | `/demo/api/insumos`               | Crea un nuevo insumo (alimento o bebida) |
| `GET`    | `/demo/api/insumos`               | Obtiene todos los insumos                |
| `GET`    | `/demo/api/insumos?tipo=Alimento` | Filtra insumos por tipo (opcional)       |
| `PUT`    | `/demo/api/insumos/{id}`          | Actualiza un insumo existente            |
| `DELETE` | `/demo/api/insumos/{id}`          | Elimina un insumo                        |

---

## Ejecutar Pruebas

Para correr las pruebas unitarias con **pytest**, ejecuta:

```sh
pytest app/tests/ --verbose
```

Si deseas ver los `print()` en las pruebas, usa:

```sh
pytest -s app/tests/
```

Para limpiar la caché de pytest:

```sh
pytest --cache-clear
```

---

## To Do



## Contribuciones

Si deseas contribuir, puedes hacer un **fork** del repositorio, crear una nueva rama y hacer un **pull request** con tus cambios.

🔹 **Autor:** [Santiago Figueroa](https://github.com/Santiago-Figu)


