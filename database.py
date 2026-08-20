import sqlite3

def conectar():
    """Crea la conexión a la base de datos."""
    return sqlite3.connect("database/carpinteria.db")

def crear_tablas():
    """Crea todas las tablas necesarias si no existen."""
    conexion = conectar()
    cursor = conexion.cursor()

    # Tabla Clientes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        telefono TEXT NOT NULL,
        direccion TEXT NOT NULL
    )
    """)

    # Tabla Materiales
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS materiales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        stock INTEGER NOT NULL,
        precio_unitario REAL NOT NULL
    )
    """)

    # Tabla Pedidos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL,
        descripcion TEXT NOT NULL,
        estado TEXT NOT NULL,
        precio_total REAL NOT NULL,
        FOREIGN KEY (cliente_id) REFERENCES clientes (id)
    )
    """)

    conexion.commit()
    conexion.close()
    print("Tablas verificadas y listas.")

if __name__ == "__main__":
    crear_tablas()