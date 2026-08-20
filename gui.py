import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import webbrowser
import urllib.parse

# --- BASE DE DATOS ---
def conectar():
    return sqlite3.connect("carpinteria.db")

def crear_tablas():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        telefono TEXT,
        direccion TEXT
    )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS materiales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        stock INTEGER NOT NULL,
        precio_unitario REAL NOT NULL
    )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL,
        descripcion TEXT NOT NULL,
        estado TEXT NOT NULL,
        precio_total REAL NOT NULL,
        fecha TEXT,
        FOREIGN KEY (cliente_id) REFERENCES clientes(id)
    )""")
    conexion.commit()
    conexion.close()

crear_tablas()

# --- APLICACIÓN PRINCIPAL ---
class AplicacionCarpinteria:
    def __init__(self, root):
        self.root = root
        self.root.title("CARPINTERÍA 4 HERMANOS - Sistema con WhatsApp")
        self.root.geometry("1000x720")
        
        self.id_cliente_editando = None
        self.id_material_editando = None
        self.id_pedido_editando = None

        self.aplicar_estilos()

        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill="both", expand=True)

        lbl_titulo = ttk.Label(
            main_frame, 
            text="🪵 CARPINTERÍA 4 HERMANOS 🪵\nSistema de Control y Gestión Operativa", 
            font=("Segoe UI", 16, "bold"),
            justify="center"
        )
        lbl_titulo.pack(pady=(5, 15))

        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill="both", expand=True)

        self.tab_clientes = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_clientes, text="  👥 Clientes  ")

        self.tab_materiales = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_materiales, text="  🛠️ Inventario  ")

        self.tab_pedidos = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_pedidos, text="  📦 Pedidos  ")

        self.tab_reportes = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_reportes, text="  📊 Reportes  ")

        self.crear_interfaz_clientes()
        self.crear_interfaz_materiales()
        self.crear_interfaz_pedidos()
        self.crear_interfaz_reportes()

        self.cargar_datos_clientes()
        self.cargar_datos_materiales()
        self.cargar_datos_pedidos()
        self.actualizar_reportes()

    def aplicar_estilos(self):
        style = ttk.Style()
        style.theme_use('clam')

        BG_WOOD = "#2c1d11"
        CARD_BG = "#3d2b1f"
        ACCENT_WOOD = "#c68b59"
        ACCENT_HOVER = "#d79b6a"
        TAB_INACTIVE = "#4a3525"
        TEXT_LIGHT = "#f5ebd8"
        TABLE_BG = "#23160c"
        DANGER_RED = "#b84a39"

        self.root.configure(bg=BG_WOOD)

        style.configure(".", background=BG_WOOD, foreground=TEXT_LIGHT, font=("Segoe UI", 10))
        style.configure("TNotebook", background=BG_WOOD, borderwidth=0)
        style.configure("TNotebook.Tab", background=TAB_INACTIVE, foreground=TEXT_LIGHT, padding=[18, 9], font=("Segoe UI", 10, "bold"), borderwidth=0)
        style.map("TNotebook.Tab", background=[("selected", ACCENT_WOOD), ("active", "#5c4331")], foreground=[("selected", "#1a0f07"), ("active", TEXT_LIGHT)])
        style.configure("TFrame", background=BG_WOOD)
        style.configure("TLabelframe", background=CARD_BG, borderwidth=1, relief="solid")
        style.configure("TLabelframe.Label", background=CARD_BG, foreground=ACCENT_WOOD, font=("Segoe UI", 11, "bold"))
        style.configure("TButton", background=ACCENT_WOOD, foreground="#1a0f07", font=("Segoe UI", 10, "bold"), padding=8, borderwidth=0)
        style.map("TButton", background=[("active", ACCENT_HOVER)], foreground=[("active", "#000000")])
        style.configure("Danger.TButton", background=DANGER_RED, foreground=TEXT_LIGHT)
        style.map("Danger.TButton", background=[("active", "#d15b49")])
        style.configure("TEntry", fieldbackground="#543d2c", foreground="#ffffff", borderwidth=0, padding=5)
        style.configure("Treeview", background=TABLE_BG, fieldbackground=TABLE_BG, foreground=TEXT_LIGHT, rowheight=28, borderwidth=0)
        style.configure("Treeview.Heading", background=CARD_BG, foreground=ACCENT_WOOD, font=("Segoe UI", 10, "bold"), borderwidth=0)
        style.map("Treeview", background=[("selected", ACCENT_WOOD)], foreground=[("selected", "#1a0f07")])

    # ================= CLIENTES =================
    def crear_interfaz_clientes(self):
        frame_form = ttk.LabelFrame(self.tab_clientes, text=" Datos del Cliente ", padding=15)
        frame_form.pack(side="left", fill="y", padx=10, pady=10)

        ttk.Label(frame_form, text="Nombre completo:").pack(anchor="w", pady=(0, 2))
        self.entry_cli_nombre = ttk.Entry(frame_form, width=25)
        self.entry_cli_nombre.pack(pady=(0, 10))

        ttk.Label(frame_form, text="Teléfono (ej: 0981123456):").pack(anchor="w", pady=(0, 2))
        self.entry_cli_telefono = ttk.Entry(frame_form, width=25)
        self.entry_cli_telefono.pack(pady=(0, 10))

        ttk.Label(frame_form, text="Dirección:").pack(anchor="w", pady=(0, 2))
        self.entry_cli_direccion = ttk.Entry(frame_form, width=25)
        self.entry_cli_direccion.pack(pady=(0, 15))

        self.btn_guardar_cli = ttk.Button(frame_form, text="💾 Guardar / Actualizar", command=self.guardar_cliente_gui)
        self.btn_guardar_cli.pack(fill="x", pady=5)
        
        ttk.Button(frame_form, text="🧹 Cancelar / Limpiar", command=self.limpiar_form_cliente).pack(fill="x", pady=5)

        frame_tabla = ttk.LabelFrame(self.tab_clientes, text=" Clientes Registrados ", padding=10)
        frame_tabla.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.tabla_clientes = ttk.Treeview(frame_tabla, columns=("id", "nombre", "telefono", "direccion"), show="headings")
        self.tabla_clientes.heading("id", text="ID")
        self.tabla_clientes.heading("nombre", text="Nombre")
        self.tabla_clientes.heading("telefono", text="Teléfono")
        self.tabla_clientes.heading("direccion", text="Dirección")

        self.tabla_clientes.column("id", width=40, anchor="center")
        self.tabla_clientes.column("nombre", width=140)
        self.tabla_clientes.column("telefono", width=100)
        self.tabla_clientes.column("direccion", width=160)
        self.tabla_clientes.pack(fill="both", expand=True, pady=(0, 10))

        frame_btn_cli = ttk.Frame(frame_tabla)
        frame_btn_cli.pack(fill="x")
        ttk.Button(frame_btn_cli, text="✏️ Editar Seleccionado", command=self.cargar_cliente_para_editar).pack(side="left", padx=5)
        ttk.Button(frame_btn_cli, text="🗑️ Eliminar Seleccionado", style="Danger.TButton", command=self.eliminar_cliente_gui).pack(side="left", padx=5)

    def cargar_datos_clientes(self):
        for item in self.tabla_clientes.get_children():
            self.tabla_clientes.delete(item)
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM clientes")
        for c in cursor.fetchall():
            self.tabla_clientes.insert("", "end", values=c)
        conexion.close()

    def guardar_cliente_gui(self):
        nombre = self.entry_cli_nombre.get().strip()
        telefono = self.entry_cli_telefono.get().strip()
        direccion = self.entry_cli_direccion.get().strip()

        if not (nombre and telefono and direccion):
            messagebox.showwarning("Atención", "Todos los campos son obligatorios.")
            return

        conexion = conectar()
        cursor = conexion.cursor()

        if self.id_cliente_editando is None:
            cursor.execute("INSERT INTO clientes (nombre, telefono, direccion) VALUES (?, ?, ?)", (nombre, telefono, direccion))
            messagebox.showinfo("Éxito", f"Cliente '{nombre}' guardado con éxito.")
        else:
            cursor.execute("UPDATE clientes SET nombre=?, telefono=?, direccion=? WHERE id=?", (nombre, telefono, direccion, self.id_cliente_editando))
            messagebox.showinfo("Éxito", f"Cliente #{self.id_cliente_editando} actualizado con éxito.")

        conexion.commit()
        conexion.close()

        self.limpiar_form_cliente()
        self.cargar_datos_clientes()
        self.actualizar_reportes()

    def cargar_cliente_para_editar(self):
        seleccion = self.tabla_clientes.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona un cliente de la tabla para editar.")
            return
        
        item = self.tabla_clientes.item(seleccion)
        c_id, c_nombre, c_telefono, c_direccion = item["values"]

        self.id_cliente_editando = c_id
        self.entry_cli_nombre.delete(0, tk.END)
        self.entry_cli_nombre.insert(0, c_nombre)
        self.entry_cli_telefono.delete(0, tk.END)
        self.entry_cli_telefono.insert(0, c_telefono)
        self.entry_cli_direccion.delete(0, tk.END)
        self.entry_cli_direccion.insert(0, c_direccion)

    def limpiar_form_cliente(self):
        self.id_cliente_editando = None
        self.entry_cli_nombre.delete(0, tk.END)
        self.entry_cli_telefono.delete(0, tk.END)
        self.entry_cli_direccion.delete(0, tk.END)

    def eliminar_cliente_gui(self):
        seleccion = self.tabla_clientes.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona un cliente de la tabla.")
            return
        item = self.tabla_clientes.item(seleccion)
        cliente_id, nombre = item["values"][0], item["values"][1]
        if messagebox.askyesno("Confirmar", f"¿Deseas eliminar a '{nombre}'?"):
            conexion = conectar()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
            conexion.commit()
            conexion.close()
            self.cargar_datos_clientes()
            self.actualizar_reportes()

    # ================= MATERIALES =================
    def crear_interfaz_materiales(self):
        frame_form = ttk.LabelFrame(self.tab_materiales, text=" Datos del Insumo ", padding=15)
        frame_form.pack(side="left", fill="y", padx=10, pady=10)

        ttk.Label(frame_form, text="Nombre Material:").pack(anchor="w", pady=(0, 2))
        self.entry_mat_nombre = ttk.Entry(frame_form, width=25)
        self.entry_mat_nombre.pack(pady=(0, 10))

        ttk.Label(frame_form, text="Stock:").pack(anchor="w", pady=(0, 2))
        self.entry_mat_stock = ttk.Entry(frame_form, width=25)
        self.entry_mat_stock.pack(pady=(0, 10))

        ttk.Label(frame_form, text="Precio unitario ($):").pack(anchor="w", pady=(0, 2))
        self.entry_mat_precio = ttk.Entry(frame_form, width=25)
        self.entry_mat_precio.pack(pady=(0, 15))

        ttk.Button(frame_form, text="💾 Guardar / Actualizar", command=self.guardar_material_gui).pack(fill="x", pady=5)
        ttk.Button(frame_form, text="🧹 Cancelar / Limpiar", command=self.limpiar_form_material).pack(fill="x", pady=5)

        frame_tabla = ttk.LabelFrame(self.tab_materiales, text=" Inventario Actual ", padding=10)
        frame_tabla.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.tabla_mat = ttk.Treeview(frame_tabla, columns=("id", "nombre", "stock", "precio", "alerta"), show="headings")
        self.tabla_mat.heading("id", text="ID")
        self.tabla_mat.heading("nombre", text="Material")
        self.tabla_mat.heading("stock", text="Stock")
        self.tabla_mat.heading("precio", text="Precio Unit.")
        self.tabla_mat.heading("alerta", text="Estado")

        self.tabla_mat.column("id", width=30, anchor="center")
        self.tabla_mat.column("nombre", width=150)
        self.tabla_mat.column("stock", width=60, anchor="center")
        self.tabla_mat.column("precio", width=90, anchor="e")
        self.tabla_mat.column("alerta", width=100, anchor="center")
        self.tabla_mat.pack(fill="both", expand=True, pady=(0, 10))

        ttk.Button(frame_tabla, text="✏️ Editar Material Seleccionado", command=self.cargar_material_para_editar).pack(anchor="w")

    def cargar_datos_materiales(self):
        for item in self.tabla_mat.get_children():
            self.tabla_mat.delete(item)
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM materiales")
        for m in cursor.fetchall():
            alerta = "⚠️ Recomprar" if m[2] <= 5 else "✅ Normal"
            self.tabla_mat.insert("", "end", values=(m[0], m[1], m[2], f"${m[3]:.2f}", alerta))
        conexion.close()

    def guardar_material_gui(self):
        nombre = self.entry_mat_nombre.get().strip()
        try:
            stock = int(self.entry_mat_stock.get().strip())
            precio = float(self.entry_mat_precio.get().strip())

            if nombre and stock >= 0 and precio >= 0:
                conexion = conectar()
                cursor = conexion.cursor()
                if self.id_material_editando is None:
                    cursor.execute("INSERT INTO materiales (nombre, stock, precio_unitario) VALUES (?, ?, ?)", (nombre, stock, precio))
                    messagebox.showinfo("Éxito", f"Material '{nombre}' agregado.")
                else:
                    cursor.execute("UPDATE materiales SET nombre=?, stock=?, precio_unitario=? WHERE id=?", (nombre, stock, precio, self.id_material_editando))
                    messagebox.showinfo("Éxito", f"Material #{self.id_material_editando} actualizado.")
                
                conexion.commit()
                conexion.close()
                self.limpiar_form_material()
                self.cargar_datos_materiales()
                self.actualizar_reportes()
            else:
                messagebox.showwarning("Atención", "Ingrese valores numéricos válidos.")
        except ValueError:
            messagebox.showerror("Error", "Stock debe ser entero y Precio decimal.")

    def cargar_material_para_editar(self):
        seleccion = self.tabla_mat.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona un material de la tabla para editar.")
            return

        item = self.tabla_mat.item(seleccion)
        m_id, m_nombre, m_stock, m_precio, _ = item["values"]

        self.id_material_editando = m_id
        self.entry_mat_nombre.delete(0, tk.END)
        self.entry_mat_nombre.insert(0, m_nombre)
        self.entry_mat_stock.delete(0, tk.END)
        self.entry_mat_stock.insert(0, m_stock)
        self.entry_mat_precio.delete(0, tk.END)
        self.entry_mat_precio.insert(0, str(m_precio).replace("$", ""))

    def limpiar_form_material(self):
        self.id_material_editando = None
        self.entry_mat_nombre.delete(0, tk.END)
        self.entry_mat_stock.delete(0, tk.END)
        self.entry_mat_precio.delete(0, tk.END)

    # ================= PEDIDOS =================
    def crear_interfaz_pedidos(self):
        frame_form = ttk.LabelFrame(self.tab_pedidos, text=" Datos del Pedido ", padding=15)
        frame_form.pack(side="left", fill="y", padx=10, pady=10)

        ttk.Label(frame_form, text="ID Cliente:").pack(anchor="w", pady=(0, 2))
        self.entry_ped_cliente = ttk.Entry(frame_form, width=25)
        self.entry_ped_cliente.pack(pady=(0, 10))

        ttk.Label(frame_form, text="Descripción del Trabajo:").pack(anchor="w", pady=(0, 2))
        self.entry_ped_desc = ttk.Entry(frame_form, width=25)
        self.entry_ped_desc.pack(pady=(0, 10))

        ttk.Label(frame_form, text="Precio Total ($):").pack(anchor="w", pady=(0, 2))
        self.entry_ped_precio = ttk.Entry(frame_form, width=25)
        self.entry_ped_precio.pack(pady=(0, 15))

        ttk.Button(frame_form, text="💾 Guardar / Actualizar", command=self.guardar_pedido_gui).pack(fill="x", pady=5)
        ttk.Button(frame_form, text="🧹 Cancelar / Limpiar", command=self.limpiar_form_pedido).pack(fill="x", pady=5)

        frame_tabla = ttk.LabelFrame(self.tab_pedidos, text=" Gestionar Pedidos Registrados ", padding=10)
        frame_tabla.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.tabla_pedidos = ttk.Treeview(frame_tabla, columns=("id", "cliente", "desc", "estado", "precio", "fecha"), show="headings")
        self.tabla_pedidos.heading("id", text="ID")
        self.tabla_pedidos.heading("cliente", text="Cliente")
        self.tabla_pedidos.heading("desc", text="Trabajo")
        self.tabla_pedidos.heading("estado", text="Estado")
        self.tabla_pedidos.heading("precio", text="Total")
        self.tabla_pedidos.heading("fecha", text="Fecha")

        self.tabla_pedidos.column("id", width=30, anchor="center")
        self.tabla_pedidos.column("cliente", width=120)
        self.tabla_pedidos.column("desc", width=150)
        self.tabla_pedidos.column("estado", width=90, anchor="center")
        self.tabla_pedidos.column("precio", width=70, anchor="e")
        self.tabla_pedidos.column("fecha", width=80, anchor="center")

        self.tabla_pedidos.pack(fill="both", expand=True, pady=(0, 10))

        frame_acciones = ttk.Frame(frame_tabla)
        frame_acciones.pack(fill="x")
        ttk.Button(frame_acciones, text="✏️ Editar", command=self.cargar_pedido_para_editar).pack(side="left", padx=3)
        ttk.Button(frame_acciones, text="🔄 Estado", command=self.cambiar_estado_pedido).pack(side="left", padx=3)
        ttk.Button(frame_acciones, text="🧾 Recibo (.txt)", command=self.generar_recibo_pedido).pack(side="left", padx=3)
        ttk.Button(frame_acciones, text="💬 Enviar WhatsApp", command=self.enviar_recibo_whatsapp).pack(side="left", padx=3)

    def cargar_datos_pedidos(self):
        for item in self.tabla_pedidos.get_children():
            self.tabla_pedidos.delete(item)
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("""
        SELECT p.id, c.nombre, p.descripcion, p.estado, p.precio_total, p.fecha 
        FROM pedidos p
        JOIN clientes c ON p.cliente_id = c.id
        """)
        for p in cursor.fetchall():
            fecha_str = p[5] if p[5] else "Sin fecha"
            self.tabla_pedidos.insert("", "end", values=(p[0], p[1], p[2], p[3], f"${p[4]:.2f}", fecha_str))
        conexion.close()

    def guardar_pedido_gui(self):
        try:
            cliente_id = int(self.entry_ped_cliente.get().strip())
            desc = self.entry_ped_desc.get().strip()
            precio = float(self.entry_ped_precio.get().strip())
            fecha_hoy = datetime.now().strftime("%Y-%m-%d")

            if desc and precio > 0:
                conexion = conectar()
                cursor = conexion.cursor()

                if self.id_pedido_editando is None:
                    cursor.execute("INSERT INTO pedidos (cliente_id, descripcion, estado, precio_total, fecha) VALUES (?, ?, 'Pendiente', ?, ?)", (cliente_id, desc, precio, fecha_hoy))
                    messagebox.showinfo("Éxito", "Pedido creado con éxito.")
                else:
                    cursor.execute("UPDATE pedidos SET cliente_id=?, descripcion=?, precio_total=? WHERE id=?", (cliente_id, desc, precio, self.id_pedido_editando))
                    messagebox.showinfo("Éxito", f"Pedido #{self.id_pedido_editando} actualizado con éxito.")

                conexion.commit()
                conexion.close()
                self.limpiar_form_pedido()
                self.cargar_datos_pedidos()
                self.actualizar_reportes()
            else:
                messagebox.showwarning("Atención", "Complete la descripción y un precio válido.")
        except ValueError:
            messagebox.showerror("Error", "ID de cliente debe ser entero y Precio un decimal.")

    def cargar_pedido_para_editar(self):
        seleccion = self.tabla_pedidos.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona un pedido de la tabla para editar.")
            return

        item = self.tabla_pedidos.item(seleccion)
        p_id, _, p_desc, _, p_precio, _ = item["values"]

        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT cliente_id FROM pedidos WHERE id = ?", (p_id,))
        c_id = cursor.fetchone()[0]
        conexion.close()

        self.id_pedido_editando = p_id
        self.entry_ped_cliente.delete(0, tk.END)
        self.entry_ped_cliente.insert(0, str(c_id))
        self.entry_ped_desc.delete(0, tk.END)
        self.entry_ped_desc.insert(0, p_desc)
        self.entry_ped_precio.delete(0, tk.END)
        self.entry_ped_precio.insert(0, str(p_precio).replace("$", ""))

    def limpiar_form_pedido(self):
        self.id_pedido_editando = None
        self.entry_ped_cliente.delete(0, tk.END)
        self.entry_ped_desc.delete(0, tk.END)
        self.entry_ped_precio.delete(0, tk.END)

    def cambiar_estado_pedido(self):
        seleccion = self.tabla_pedidos.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona un pedido de la tabla.")
            return

        item = self.tabla_pedidos.item(seleccion)
        pedido_id = item["values"][0]
        estado_actual = item["values"][3]

        nuevos_estados = {"Pendiente": "En Proceso 🛠️", "En Proceso 🛠️": "Completado ✅", "Completado ✅": "Pendiente"}
        nuevo_estado = nuevos_estados.get(estado_actual, "Pendiente")

        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("UPDATE pedidos SET estado = ? WHERE id = ?", (nuevo_estado, pedido_id))
        conexion.commit()
        conexion.close()

        self.cargar_datos_pedidos()

    def generar_recibo_pedido(self):
        seleccion = self.tabla_pedidos.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona un pedido de la tabla.")
            return

        item = self.tabla_pedidos.item(seleccion)
        pedido_id, cliente, desc, estado, precio, fecha = item["values"]

        nombre_archivo = f"Recibo_Pedido_{pedido_id}.txt"
        contenido = f"""
==================================================
           CARPINTERÍA 4 HERMANOS
        COMPROBANTE DE PEDIDO Y PRESUPUESTO
==================================================
Fecha de Emisión: {fecha}
Nº de Pedido: #{pedido_id}
Cliente: {cliente}
--------------------------------------------------
Descripción del Mueble / Trabajo:
 -> {desc}

Estado Actual del Trabajo: {estado}
--------------------------------------------------
TOTAL COMPROMETIDO: {precio}
==================================================
 ¡Gracias por confiar en Carpintería 4 Hermanos!
==================================================
        """
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write(contenido)

        messagebox.showinfo("Recibo Creado", f"Se ha generado el archivo '{nombre_archivo}' con éxito.")

    # --- NUEVA FUNCIÓN PARA ENVIAR POR WHATSAPP ---
    def enviar_recibo_whatsapp(self):
        seleccion = self.tabla_pedidos.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona un pedido de la tabla para enviar.")
            return

        item = self.tabla_pedidos.item(seleccion)
        pedido_id, cliente_nombre, desc, estado, precio, fecha = item["values"]

        # Obtener el número de teléfono del cliente desde la base de datos
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT c.telefono 
            FROM pedidos p 
            JOIN clientes c ON p.cliente_id = c.id 
            WHERE p.id = ?
        """, (pedido_id,))
        resultado = cursor.fetchone()
        conexion.close()

        if not resultado or not resultado[0]:
            messagebox.showerror("Error", "No se encontró un número de teléfono registrado para este cliente.")
            return

        telefono = str(resultado[0]).strip()

        # Limpiar el teléfono para dejar solo números (elimina espacios, guiones o signos +)
        telefono_limpio = "".join(filter(str.isdigit, telefono))

        # Si el número no tiene prefijo de país (ej. Paraguay 595), se lo agrega si empieza por 09
        if telefono_limpio.startswith("0"):
            telefono_limpio = "595" + telefono_limpio[1:]

        # Crear el texto del mensaje para WhatsApp
        mensaje = (
            f"🛠️ *CARPINTERÍA 4 HERMANOS*\n"
            f"📋 *COMPROBANTE DE PEDIDO #{pedido_id}*\n\n"
            f"👤 *Cliente:* {cliente_nombre}\n"
            f"📅 *Fecha:* {fecha}\n"
            f"🪵 *Trabajo:* {desc}\n"
            f"📌 *Estado:* {estado}\n"
            f"💰 *Total:* {precio}\n\n"
            f"¡Muchas gracias por confiar en nosotros! 🙌"
        )

        # Formatear el mensaje para URL
        mensaje_encoded = urllib.parse.quote(mensaje)
        url_whatsapp = f"https://api.whatsapp.com/send?phone={telefono_limpio}&text={mensaje_encoded}"

        # Abrir en el navegador predeterminado
        webbrowser.open(url_whatsapp)

    # ================= REPORTES =================
    def crear_interfaz_reportes(self):
        frame_rep = ttk.LabelFrame(self.tab_reportes, text=" Métrica General del Negocio ", padding=30)
        frame_rep.pack(fill="both", expand=True, padx=20, pady=20)

        self.lbl_rep_clientes = ttk.Label(frame_rep, text="👥 Clientes Registrados: 0", font=("Segoe UI", 12))
        self.lbl_rep_clientes.pack(anchor="w", pady=10)

        self.lbl_rep_pedidos = ttk.Label(frame_rep, text="📦 Pedidos Realizados: 0", font=("Segoe UI", 12))
        self.lbl_rep_pedidos.pack(anchor="w", pady=10)

        self.lbl_rep_materiales = ttk.Label(frame_rep, text="🛠️ Tipos de Insumos: 0", font=("Segoe UI", 12))
        self.lbl_rep_materiales.pack(anchor="w", pady=10)

        self.lbl_rep_ingresos = ttk.Label(frame_rep, text="💰 Ingresos Totales: $0.00", font=("Segoe UI", 16, "bold"), foreground="#ffd166")
        self.lbl_rep_ingresos.pack(anchor="w", pady=20)

        ttk.Button(frame_rep, text="🔄 Actualizar Reporte", command=self.actualizar_reportes).pack(anchor="w", pady=10)

    def actualizar_reportes(self):
        conexion = conectar()
        cursor = conexion.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM clientes")
        cli_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM pedidos")
        ped_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM materiales")
        mat_count = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(precio_total) FROM pedidos")
        total_ingresos = cursor.fetchone()[0] or 0.0

        conexion.close()

        self.lbl_rep_clientes.config(text=f"👥 Clientes Registrados: {cli_count}")
        self.lbl_rep_pedidos.config(text=f"📦 Pedidos Realizados: {ped_count}")
        self.lbl_rep_materiales.config(text=f"🛠️ Tipos de Insumos: {mat_count}")
        self.lbl_rep_ingresos.config(text=f"💰 Ingresos Totales: ${total_ingresos:.2f}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionCarpinteria(root)
    root.mainloop()