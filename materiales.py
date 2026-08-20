from database import conectar

def agregar_material(nombre, stock, precio_unitario):
    conexion = conectar()
    cursor = conexion.cursor()
    
    cursor.execute("""
    INSERT INTO materiales (nombre, stock, precio_unitario)
    VALUES (?, ?, ?)
    """, (nombre, stock, precio_unitario))
    
    conexion.commit()
    conexion.close()
    print(f"Material '{nombre}' guardado correctamente.")

def listar_materiales():
    conexion = conectar()
    cursor = conexion.cursor()
    
    cursor.execute("SELECT * FROM materiales")
    materiales = cursor.fetchall()
    conexion.close()
    
    print("\n--- INVENTARIO DE MATERIALES ---")
    if not materiales:
        print("No hay materiales registrados.")
    else:
        for m in materiales:
            print(f"ID: {m[0]} | Material: {m[1]} | Stock: {m[2]} unidades | Precio Unitario: ${m[3]:.2f}")