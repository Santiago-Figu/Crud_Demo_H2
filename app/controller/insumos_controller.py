from app.config.config import get_db_connection, close_db_connection


def create_table():
    """Crea la tabla en la base de datos si no existe e inserta datos demo."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        status= False
        message = ""
        # Crear la tabla si no existe
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS insumos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT NOT NULL,
                estatus TEXT NOT NULL,
                comentarios TEXT,
                estrellas INTEGER CHECK(estrellas BETWEEN 1 AND 5),
                tipo TEXT NOT NULL CHECK(tipo IN ('Alimento', 'Bebida'))
            );
        """)
        # verificar si existen datos
        cursor.execute("SELECT COUNT(*) FROM insumos;")
        count = cursor.fetchone()[0]
        if count == 0:
            cursor.execute("""
                INSERT INTO insumos (nombre, descripcion, estatus, comentarios, estrellas, tipo)
                VALUES 
                    ('Hamburguesa', 'Deliciosa hamburguesa con queso', 'Disponible', 'Recomendada', 5, 'Alimento'),
                    ('Café', 'Café americano recién hecho', 'Disponible', 'Aroma increíble', 4, 'Bebida');
            """)
            conn.commit()
            status = True
            message= "La base de datos fue creada con datos demo insertados correctamente."
        else:
            status = True
            message= "La Base de datos ya existe, no se insertaron datos demo."
    except Exception as e:
        status= False
        message= f"Ocurrio un error al crear la base de datos: {e}"
    finally:
        close_db_connection(conn)
    return status,message

def create_insumo(data):
    """Función para insertar un nuevo insumo en la base de datos."""
    
    status = False
    message = ""
    inserted_id = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO insumos (nombre, descripcion, estatus, comentarios, estrellas, tipo)
            VALUES (?, ?, ?, ?, ?, ?);
        """, (data.nombre, data.descripcion, data.estatus, data.comentarios, data.estrellas, data.tipo))
        conn.commit()
        inserted_id = cursor.lastrowid  # Obtener el ID del nuevo insumo
        
        status = True
        message = "Insumo creado correctamente."

    except Exception as e:
        status = False
        message = f"Error al crear el insumo: {e}"
    
    finally:
        close_db_connection(conn)
        return status, message, {"id": inserted_id, "nombre": data.nombre, "tipo": data.tipo} if inserted_id else None


def get_insumos(tipo: str = None):
    """Función para obtener todos los registros de la BD."""
    status = False
    message = ""
    data = []

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Filtra por tipo si es ingresado un valor
        if tipo:
            cursor.execute("SELECT * FROM insumos WHERE tipo = ?;", (tipo,))
        else:
            cursor.execute("SELECT * FROM insumos;")

        rows = cursor.fetchall()

        if not rows:
            status = True
            message = "No hay insumos registrados." if not tipo else f"No hay insumos del tipo {tipo}."
        else:
            status = True
            message = "Insumos recuperados correctamente."
            data = [dict(row) for row in rows]

    except Exception as e:
        status = False
        message = f"Error al obtener los insumos: {e}"

    finally:
        close_db_connection(conn)
        return status, message, data

def get_insumo(id: int):
    """Función para obtener un insumo por ID."""

    status = False
    message = ""
    data = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM insumos WHERE id = ?;", (id,))
        row = cursor.fetchone()

        if not row:
            status = False
            message = "No se encontró un insumo con el ID proporcionado."
        else:
            status = True
            message = "Insumo encontrado."
            data = dict(row)

    except Exception as e:
        status = False
        message = f"Error al obtener el insumo: {e}"

    finally:
        close_db_connection(conn)
        return status, message, data


def update_insumo(id: int, data):
    """Función para actualizar un insumo por ID."""
    status = False
    message = ""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Verificar si el insumo existe
        cursor.execute("SELECT COUNT(*) FROM insumos WHERE id = ?;", (id,))
        count = cursor.fetchone()[0]

        if count == 0:
            status = False
            message = "No se encontró un insumo con el ID proporcionado."
        else:
            cursor.execute("""
                UPDATE insumos
                SET nombre = ?, descripcion = ?, estatus = ?, comentarios = ?, estrellas = ?, tipo = ?
                WHERE id = ?;
            """, (data.nombre, data.descripcion, data.estatus, data.comentarios, data.estrellas, data.tipo, id))
            conn.commit()

            status = True
            message = "Insumo actualizado correctamente."

    except Exception as e:
        status = False
        message = f"Error al actualizar el insumo: {e}"

    finally:
        close_db_connection(conn)
        return status, message



def delete_insumo(id: int):
    """Función para eliminar un insumo por ID."""
    status = False
    message = ""

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Verificar si el insumo existe
        cursor.execute("SELECT COUNT(*) FROM insumos WHERE id = ?;", (id,))
        count = cursor.fetchone()[0]

        if count == 0:
            status = False
            message = "No se encontró un insumo con el ID proporcionado."
        else:
            cursor.execute("DELETE FROM insumos WHERE id = ?;", (id,))
            conn.commit()

            status = True
            message = "Insumo eliminado correctamente."

    except Exception as e:
        status = False
        message = f"Error al eliminar el insumo: {e}"

    finally:
        close_db_connection(conn)
        return status, message

