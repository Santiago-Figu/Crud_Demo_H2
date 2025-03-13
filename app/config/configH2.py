import os
import sqlite3

"""
    Nota: No utilice jpype para la conexión a H2 por que en mi sistema operativo
    nunca funciono el driver, así que encontre esta alternativa con sqlite3 para evitar problemas de compatibilidad
    
"""

# Ruta donse se va a crear el archivo fisico para la base de datos H2
FILE_DB = os.path.join(os.getcwd(), "app", "data_base", "test_db").replace("\\", "/")

# URL de conexión para H2 en modo archivo
DATABASE_URL = f"{FILE_DB}.db"

def get_db_connection():
    """Abre una conexión a la base de datos H2 (SQLite) y devuelve resultados como diccionario."""
    try:
        conn = sqlite3.connect(DATABASE_URL)
        conn.row_factory = sqlite3.Row  # Convierte los resultados en diccionarios
        return conn
    except Exception as e:
        print(f"Error al conectar con la base de datos H2: {e}")
        return None


def close_db_connection(conn):
    """Cierra la conexión a la base de datos."""
    if conn:
        conn.close()
        print("Conexión cerrada correctamente.")

def test_connection():
    """Función para probar la conexión a la base de datos H2."""
    status=False
    message= ""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT 1;")
            resultado = cursor.fetchone()
            status=True
            message=f"Prueba de conexión ejecutada con éxito: {resultado}"
            cursor.close()
        except Exception as e:
            message=f"Error ejecutando consulta de prueba: {e}"
            
        finally:
            close_db_connection(conn)
    else:
        message= "No fue posible establecer la conexión"
    print(f"{message} : {status}")
    return message, status

if __name__ == "__main__":
    _,_=test_connection()
