from database import conectar

def generar_resumen_general():
    conexion = conectar()
    cursor = conexion.cursor()
    
    # Contar total de clientes
    cursor.execute("SELECT COUNT(*) FROM clientes")
    total_clientes = cursor.fetchone()[0]
    
    # Contar total de pedidos
    cursor.execute("SELECT COUNT(*) FROM pedidos")
    total_pedidos = cursor.fetchone()[0]
    
    # Sumar el total de ingresos por pedidos
    cursor.execute("SELECT SUM(precio_total) FROM pedidos")
    suma_ingresos = cursor.fetchone()[0] or 0.0
    
    # Contar total de materiales
    cursor.execute("SELECT COUNT(*) FROM materiales")
    total_materiales = cursor.fetchone()[0]
    
    conexion.close()
    
    print("\n==================================")
    print("      RESUMEN GENERAL DEL NEGOCIO")
    print("==================================")
    print(f"👥 Clientes registrados: {total_clientes}")
    print(f"📦 Pedidos realizados:  {total_pedidos}")
    print(f"🛠️ Materiales en stock: {total_materiales}")
    print(f"💰 Ingresos totales:    ${suma_ingresos:.2f}")
    print("==================================")