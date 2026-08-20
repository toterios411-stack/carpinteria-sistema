from clientes import agregar_cliente, listar_clientes, editar_cliente, eliminar_cliente
from materiales import agregar_material, listar_materiales
from pedidos import crear_pedido, listar_pedidos
from reportes import generar_resumen_general

def menu_clientes():
    while True:
        print("\n--- MÓDULO CLIENTES ---")
        print("1. Ver lista de clientes")
        print("2. Registrar nuevo cliente")
        print("3. Editar cliente")
        print("4. Eliminar cliente")
        print("5. Volver al menú principal")
        
        sub_opcion = input("\nSeleccione una opción: ")

        if sub_opcion == "1":
            listar_clientes()

        elif sub_opcion == "2":
            print("\n--- REGISTRAR NUEVO CLIENTE ---")
            nombre = input("Nombre completo: ")
            telefono = input("Teléfono: ")
            direccion = input("Dirección: ")
            
            if nombre and telefono and direccion:
                agregar_cliente(nombre, telefono, direccion)
            else:
                print("❌ Todos los campos son obligatorios.")

        elif sub_opcion == "3":
            print("\n--- EDITAR CLIENTE ---")
            listar_clientes()
            try:
                cliente_id = int(input("\nIngrese el ID del cliente a editar: "))
                nuevo_nombre = input("Nuevo nombre: ")
                nuevo_telefono = input("Nuevo teléfono: ")
                nueva_direccion = input("Nueva dirección: ")
                
                if nuevo_nombre and nuevo_telefono and nueva_direccion:
                    editar_cliente(cliente_id, nuevo_nombre, nuevo_telefono, nueva_direccion)
                else:
                    print("❌ Todos los campos son obligatorios.")
            except ValueError:
                print("❌ El ID debe ser un número entero válido.")

        elif sub_opcion == "4":
            print("\n--- ELIMINAR CLIENTE ---")
            listar_clientes()
            try:
                cliente_id = int(input("\nIngrese el ID del cliente a eliminar: "))
                confirmacion = input(f"¿Está seguro de eliminar al cliente con ID {cliente_id}? (s/n): ")
                if confirmacion.lower() == 's':
                    eliminar_cliente(cliente_id)
                else:
                    print("Operación cancelada.")
            except ValueError:
                print("❌ El ID debe ser un número entero válido.")

        elif sub_opcion == "5":
            break
        else:
            print("❌ Opción incorrecta")

def menu_materiales():
    while True:
        print("\n--- MÓDULO MATERIALES ---")
        print("1. Ver inventario de materiales")
        print("2. Registrar nuevo material")
        print("3. Volver al menú principal")
        
        sub_opcion = input("\nSeleccione una opción: ")

        if sub_opcion == "1":
            listar_materiales()
        elif sub_opcion == "2":
            print("\n--- REGISTRAR NUEVO MATERIAL ---")
            nombre = input("Nombre del material: ")
            try:
                stock = int(input("Cantidad en stock: "))
                precio = float(input("Precio unitario: "))
                
                if nombre and stock >= 0 and precio >= 0:
                    agregar_material(nombre, stock, precio)
                else:
                    print("❌ Ingrese valores válidos.")
            except ValueError:
                print("❌ El stock y el precio deben ser números válidos.")
        elif sub_opcion == "3":
            break
        else:
            print("❌ Opción incorrecta")

def menu_pedidos():
    while True:
        print("\n--- MÓDULO PEDIDOS ---")
        print("1. Ver lista de pedidos")
        print("2. Registrar nuevo pedido")
        print("3. Volver al menú principal")
        
        sub_opcion = input("\nSeleccione una opción: ")

        if sub_opcion == "1":
            listar_pedidos()
        elif sub_opcion == "2":
            print("\n--- REGISTRAR NUEVO PEDIDO ---")
            listar_clientes()
            try:
                cliente_id = int(input("\nIngrese el ID del cliente: "))
                descripcion = input("Descripción del trabajo: ")
                precio_total = float(input("Precio total: "))
                
                if descripcion and precio_total > 0:
                    crear_pedido(cliente_id, descripcion, precio_total)
                else:
                    print("❌ Complete los datos correctamente.")
            except ValueError:
                print("❌ El ID y el precio deben ser valores numéricos válidos.")
        elif sub_opcion == "3":
            break
        else:
            print("❌ Opción incorrecta")

def menu_principal():
    while True:
        print("\n=== CARPINTERIA 4 HERMANOS ===")
        print("1. Clientes")
        print("2. Pedidos")
        print("3. Materiales")
        print("4. Reportes")
        print("5. Salir")

        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            menu_clientes()
        elif opcion == "2":
            menu_pedidos()
        elif opcion == "3":
            menu_materiales()
        elif opcion == "4":
            generar_resumen_general()
        elif opcion == "5":
            print("¡Hasta luego!")
            break
        else:
            print("Opción incorrecta")

if __name__ == "__main__":
    menu_principal()