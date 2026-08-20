from database import conectar

def crear_pedido(cliente_id, descripcion, precio_total, estado="Pendiente"):
    conexion = conectar()
    cursor = conexion.cursor()
    
    # Verificar si el cliente existe antes de crear el pedido
    cursor.execute("SELECT nombre FROM clientes WHERE id = ?", (cliente_id,))
    cliente = cursor.fetchone()
    
    if not cliente:
        print(f"❌ Error: El cliente con ID {cliente_id} no existe.")
        conexion.close()
        return

    cursor.execute("""
    INSERT INTO pedidos (cliente_id, descripcion, estado, precio_total)
    VALUES (?, ?, ?, ?)
    """, (cliente_id, descripcion, estado, precio_total))
    
    conexion.commit()
    conexion.close()
    print(f"Pedido registrado con éxito para el cliente {cliente[0]}.")

def listar_pedidos():
    conexion = conectar()
    cursor = conexion.cursor()
    
    # Unimos (JOIN) la tabla pedidos con la tabla clientes para mostrar el nombre del cliente
    cursor.execute("""
    SELECT p.id, c.nombre, p.descripcion, p.estado, p.precio_total 
    FROM pedidos p
    JOIN clientes c ON p.cliente_id = c.id
    """)
    pedidos = cursor.fetchall()
    conexion.close()
    
    print("\n--- LISTA DE PEDIDOS ---")
    if not pedidos:
        print("No hay pedidos registrados.")
    else:
        for p in pedidos:
            print(f"ID Pedido: {p[0]} | Cliente: {p[1]} | Trabajo: {p[2]} | Estado: {p[3]} | Total: ${p[4]:.2f}")