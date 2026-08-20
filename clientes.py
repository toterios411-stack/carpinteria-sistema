from database import conectar

def agregar_cliente(nombre, telefono, direccion):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
    INSERT INTO clientes (nombre, telefono, direccion)
    VALUES (?, ?, ?)
    """, (nombre, telefono, direccion))
    conexion.commit()
    conexion.close()
    print(f"✅ Cliente '{nombre}' registrado correctamente.")

def listar_clientes():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    conexion.close()
    
    print("\n--- LISTA DE CLIENTES ---")
    if not clientes:
        print("No hay clientes registrados.")
    else:
        for c in clientes:
            print(f"ID: {c[0]} | Nombre: {c[1]} | Teléfono: {c[2]} | Dirección: {c[3]}")

def editar_cliente(cliente_id, nuevo_nombre, nuevo_telefono, nueva_direccion):
    conexion = conectar()
    cursor = conexion.cursor()
    
    # Verificar si el cliente existe
    cursor.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,))
    if not cursor.fetchone():
        print(f"❌ No existe ningún cliente con el ID {cliente_id}.")
        conexion.close()
        return

    cursor.execute("""
    UPDATE clientes 
    SET nombre = ?, telefono = ?, direccion = ?
    WHERE id = ?
    """, (nuevo_nombre, nuevo_telefono, nueva_direccion, cliente_id))
    
    conexion.commit()
    conexion.close()
    print(f"✅ Cliente ID {cliente_id} actualizado con éxito.")

def eliminar_cliente(cliente_id):
    conexion = conectar()
    cursor = conexion.cursor()
    
    # Verificar si el cliente existe
    cursor.execute("SELECT nombre FROM clientes WHERE id = ?", (cliente_id,))
    cliente = cursor.fetchone()
    
    if not cliente:
        print(f"❌ No existe ningún cliente con el ID {cliente_id}.")
        conexion.close()
        return

    cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
    
    conexion.commit()
    conexion.close()
    print(f"🗑️ Cliente '{cliente[0]}' eliminado con éxito.")