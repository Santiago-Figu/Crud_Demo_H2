
# 🚀 API de Insumos con FastAPI y H2/SQLite 

## Descripción

Este proyecto consiste en un CRUD de API´s de testing desarrollada para el proceso de selección de la vacante Python Backend Developer Sr, en la cual se plantea un CRUD para gestionar insumos de alimentos y bebidas, almacenándolos en una base de datos **H2 con SQLite**.

Como tecnologías de desarrollo se ha utilizado **FastAPI**, **Pydantic** y **Uvicorn**, con pruebas unitarias en **pytest**, para probar la inserción de datos desde las funciones del controlador con **sqlite3**, inserción y validación de datos con **Pydantic** desde la api con **Uvicorn**.

---
## Requisitos

Antes de ejecutar el proyecto, asegúrate de tener:

✅ **Python 3.11+** instalado.

✅ **Pip y virtualenv** instalados y actualizados.

✅ **Java 11 o superior** (para H2).

✅ **Instancia de PostgreSQL** con usuarios con permisos de creación (para PostgreSQL).

Si lo necesitas puedes usar pyenv para manejar diferentes versiones de python

- [Doc](https://github.com/pyenv-win/pyenv-win)
- [Installation](https://github.com/pyenv-win/pyenv-win/blob/master/docs/installation.md)

---
## Environment Variables

Para levantar este proyecto necesitas agregar las siguientes variables a tu **.env** file:

#### PostgreSQL
`DB_NAME=tu_database_name`

`DB_USER=tu_postgres_user`

`DB_PASSWORD=tu_admin_password`

`DB_HOST=tu_localhost`

`DB_PORT=5432`

`SCHEMA=tu_schema`

#### Django - Configuración
`DJANGO_SECRET_KEY = tu_django_secret_key`

`ADMIN_PASSWORD=tu_password_admin`

#### Tokens y cifrado

> [!NOTE]
> Nota en los archivos jwt_utils.py y aes_cipher.py cuentas con funciones para generar tu FERNET_KEY y probar las funciones de cifrado

`SECRET_KEY=tu_secret_key`

`FERNET_KEY=tu_fernet_key`

> [!NOTE]
Ingresa el valor que prefieras, si no ingresas este valor por defecto se asigna el valor "/demo/api":

`API_PREFIX = tu_ruta_personalizada` 


## Instalación

1️⃣ **Clonar el repositorio:**

```sh
git clone https://github.com/Santiago-Figu/Crud_Demo_H2.git
cd Crud_Demo_H2
```

2️⃣ **Crear un entorno virtual e instalar dependencias:**

```sh
python -m venv env
```
En Windows run 
```sh
  env\Scripts\activate
```
En Mac run 
```sh
  source env/bin/activate
```
Actualiza tu gestor de paquetes

```sh
  python -m pip install --upgrade pip
```

Instala las dependencias

```sh
  pip install -r requirements.txt
```

---

## Descarga de Drivers

### 🔹 **H2 Database Driver**

Para utilizar H2, descarga el driver H2 🔗 [Driver](https://www.h2database.com/html/download.html)

Después de descargarlo, colócalo en:

```
app/DB/driver_h2/bin/h2-2.3.232.jar
```

### 🔹 **SQLite-JDBC Driver**

Para utilizar SQLite, descarga el driver JDBC 🔗 [https://github.com/xerial/sqlite-jdbc](https://github.com/xerial/sqlite-jdbc)

Después de descargarlo, colócalo en:

```
app/DB/driver_sqlite/bin/sqlite-jdbc-3.41.2.jar
```

## Migraciones

> [!NOTE]
> Si quieres crear tus propias Migraciones ejecuta el siguiente comando para crear una nueva migración en la ruta **app\alembic\versions**:

```sh
  alembic revision --autogenerate -m "initial migration"
```
Ejecuta las migraciones actuales:


```sh
  alembic upgrade head
```


---
## Deployment

Para iniciar la API con **Uvicorn**, ejecuta:

```sh
uvicorn main:app
```
Si quieres que la API se recarge en automático al realizar cambios en el cófigo, ejecuta:

```sh
uvicorn main:app --reload
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
## Testing

Para correr las pruebas unitarias con **pytest**, ejecuta:

```sh
pytest app/tests/ --verbose
```

Si deseas ver los `print()` en las pruebas, usa:

```sh
pytest -s app/tests/
```

Para ejecutar limpiaando la caché de pytest:

```sh
pytest --cache-clear
```

---
## ToDo

- Agregado de tokens a apis para evitar ejecuciones no autorizadas
- Mejorar modelos de entidades
- Agregar validaciones de datos en apis
- Agregar más productos
## Authors

- **Autor:** [Santiago Figueroa](https://github.com/Santiago-Figu)


## Feedback

If you have any feedback, please reach out to us at sfigu@outlook.com

