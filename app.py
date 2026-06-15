import sqlite3
from flask import Flask, request, jsonify, render_template, redirect, session
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
import re

app = Flask(__name__)

app.secret_key = "gestion_inventario_2026"

# ==========================
# CONEXIÓN DB
# ==========================
def conectar_db():
    conn = sqlite3.connect("inventario.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        usuario = request.form["usuario"]
        password = request.form["password"]

        conn = conectar_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM usuarios
            WHERE usuario = ?
        """, (usuario,))

        usuario_db = cursor.fetchone()

        conn.close()

        if usuario_db and check_password_hash(
            usuario_db["password"],
            password
        ):
            session["usuario"] = usuario
            return redirect("/")

        return render_template(
            "login.html",
            error="Usuario o contraseña incorrectos"
        )

    return render_template("login.html")

@app.route("/registro", methods=["GET", "POST"])
def registro():

    if request.method == "POST":

        usuario = request.form["usuario"]
        password = request.form["password"]
        confirmar = request.form["confirmar_password"]

        # VALIDAR CONTRASEÑAS IGUALES
        if password != confirmar:

            return render_template(
                "registro.html",
                error="Las contraseñas no coinciden"
            )

        # VALIDAR SEGURIDAD
        if len(password) < 8:

            return render_template(
                "registro.html",
                error="La contraseña debe tener al menos 8 caracteres"
            )

        if not re.search(r"[A-Z]", password):

            return render_template(
                "registro.html",
                error="Debe contener al menos una mayúscula"
            )

        if not re.search(r"[a-z]", password):

            return render_template(
                "registro.html",
                error="Debe contener al menos una minúscula"
            )

        if not re.search(r"\d", password):

            return render_template(
                "registro.html",
                error="Debe contener al menos un número"
            )

        if not re.search(
            r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?]",
            password
        ):

            return render_template(
                "registro.html",
                error="Debe contener al menos un carácter especial"
            )

        conn = conectar_db()
        cursor = conn.cursor()

        # VERIFICAR SI EL USUARIO YA EXISTE
        cursor.execute("""
            SELECT * FROM usuarios
            WHERE usuario = ?
        """, (usuario,))

        existe = cursor.fetchone()

        if existe:

            conn.close()

            return render_template(
                "registro.html",
                error="Ese usuario ya existe"
            )

        # GENERAR HASH
        password_hash = generate_password_hash(password)

        # GUARDAR USUARIO
        cursor.execute("""
            INSERT INTO usuarios(usuario, password)
            VALUES (?, ?)
        """, (usuario, password_hash))

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("registro.html")

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")
# ==========================
# PÁGINA PRINCIPAL
# ==========================

@app.route("/")
def inicio():

    if "usuario" not in session:
        return redirect("/login")

    return render_template("index.html")

# ==========================
# INVENTARIO
# ==========================
@app.route("/inventario")
def pagina_inventario():

    # LOGIN REQUERIDO
    if "usuario" not in session:
        return redirect("/login")

    nombre_busqueda = request.args.get("buscar")

    conn = conectar_db()
    cursor = conn.cursor()

    no_resultados = False

    # PRODUCTOS
    if nombre_busqueda:
        cursor.execute("""
            SELECT * FROM productos
            WHERE LOWER(nombre) LIKE ?
        """, ('%' + nombre_busqueda.lower() + '%',))

        productos = cursor.fetchall()

        if len(productos) == 0:
            no_resultados = True

    else:
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()

    # STOCK BAJO
    cursor.execute("""
        SELECT * FROM productos
        WHERE cantidad < stock_minimo
    """)
    productos_poco_stock = cursor.fetchall()

    # VALOR TOTAL
    cursor.execute("""
        SELECT SUM(precio_unitario * cantidad) AS total
        FROM productos
    """)
    valor_total = cursor.fetchone()["total"] or 0

    # HISTORIAL MOVIMIENTOS (ÚLTIMOS 10)
    cursor.execute("""
        SELECT * FROM movimientos
        ORDER BY id DESC
        LIMIT 10
    """)
    movimientos = cursor.fetchall()

    # CATEGORÍAS ÚNICAS
    cursor.execute("""
        SELECT DISTINCT categoria
        FROM productos
        ORDER BY categoria
    """)
    categorias = cursor.fetchall()

    conn.close()

    return render_template(
        "inventario.html",
        productos=productos,
        productos_poco_stock=productos_poco_stock,
        valor_total=valor_total,
        movimientos=movimientos,
        categorias=categorias,
        no_resultados=no_resultados
    )
# ==========================
# AGREGAR PRODUCTO
# ==========================
@app.route("/agregar-producto", methods=["POST"])
def agregar_producto_html():
    
    if "usuario" not in session:
        return redirect("/login")    

    conn = conectar_db()
    cursor = conn.cursor()

    nombre = request.form.get("nombre")
    categoria = request.form.get("categoria")
    precio_unitario = float(request.form.get("precio_unitario"))
    cantidad = int(request.form.get("cantidad"))
    stock_minimo = int(request.form.get("stock_minimo"))

    # 🔍 BUSCAR SI YA EXISTE
    cursor.execute("""
        SELECT * FROM productos
        WHERE nombre = ?
        AND categoria = ?
        AND precio_unitario = ?
    """, (nombre, categoria, precio_unitario))

    producto_existente = cursor.fetchone()

    if producto_existente:
        # 🔼 SI EXISTE → SUMAR STOCK
        cursor.execute("""
            UPDATE productos
            SET cantidad = cantidad + ?
            WHERE id = ?
        """, (cantidad, producto_existente["id"]))

        cursor.execute("""
            INSERT INTO movimientos (descripcion)
            VALUES (?)
        """, (f"Se sumó stock a {nombre} (+{cantidad})",))

    else:
        # ➕ SI NO EXISTE → CREAR NUEVO
        cursor.execute("""
            INSERT INTO productos (nombre, categoria, precio_unitario, cantidad, stock_minimo)
            VALUES (?, ?, ?, ?, ?)
        """, (nombre, categoria, precio_unitario, cantidad, stock_minimo))

        cursor.execute("""
            INSERT INTO movimientos (descripcion)
            VALUES (?)
        """, (f"Se creó producto {nombre} (+{cantidad})",))

    conn.commit()
    conn.close()

    return redirect("/inventario")

@app.route("/agregar-stock", methods=["POST"])
def agregar_stock():

    if "usuario" not in session:
        return redirect("/login")

    conn = conectar_db()
    cursor = conn.cursor()

    producto_id = int(request.form["producto_id"])
    cantidad = int(request.form["cantidad"])

    cursor.execute("""
        UPDATE productos
        SET cantidad = cantidad + ?
        WHERE id = ?
    """, (cantidad, producto_id))

    cursor.execute("""
        SELECT nombre
        FROM productos
        WHERE id = ?
    """, (producto_id,))

    producto = cursor.fetchone()

    cursor.execute("""
        INSERT INTO movimientos (descripcion)
        VALUES (?)
    """, (f"Se repuso stock de {producto['nombre']} (+{cantidad})",))

    conn.commit()
    conn.close()

    return redirect("/inventario")
# ==========================
# EDITAR PRODUCTO
# ==========================
@app.route("/guardar-producto/<int:id_producto>", methods=["POST"])
def guardar_producto(id_producto):
    if "usuario" not in session:
        return redirect("/login")

    conn = conectar_db()
    cursor = conn.cursor()

    nombre = request.form["nombre"]

    cursor.execute("""
        UPDATE productos
        SET nombre=?, categoria=?, precio_unitario=?, cantidad=?
        WHERE id=?
    """, (
        nombre,
        request.form["categoria"],
        float(request.form["precio_unitario"]),
        int(request.form["cantidad"]),
        id_producto
    ))

    # MOVIMIENTO
    cursor.execute("""
        INSERT INTO movimientos (descripcion)
        VALUES (?)
    """, (f"Se editó producto {nombre}",))

    conn.commit()
    conn.close()

    return redirect("/inventario")


# ==========================
# ELIMINAR PRODUCTO
# ==========================
@app.route("/eliminar_producto/<int:id_producto>", methods=["POST"])
def eliminar_producto_html(id_producto):
    if "usuario" not in session:
        return redirect("/login")

    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))

    # MOVIMIENTO
    cursor.execute("""
        INSERT INTO movimientos (descripcion)
        VALUES (?)
    """, (f"Se eliminó producto ID {id_producto}",))

    conn.commit()
    conn.close()

    return redirect("/inventario")


# ==========================
# API PRODUCTOS
# ==========================
@app.route("/productos", methods=["GET"])
def obtener_productos():
    if "usuario" not in session:
        return redirect("/login")

    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()

    conn.close()

    return jsonify([{
        "id": p["id"],
        "nombre": p["nombre"],
        "categoria": p["categoria"],
        "precio_unitario": p["precio_unitario"],
        "cantidad": p["cantidad"],
        "stock_minimo": p["stock_minimo"]
    } for p in productos])


# ==========================
# STOCK BAJO
# ==========================
@app.route("/stock-bajo", methods=["GET"])
def stock_bajo():
    if "usuario" not in session:
        return redirect("/login")

    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM productos
        WHERE cantidad < stock_minimo
    """)

    productos = cursor.fetchall()
    conn.close()

    return jsonify([{
        "id": p["id"],
        "nombre": p["nombre"],
        "cantidad": p["cantidad"],
        "stock_minimo": p["stock_minimo"]
    } for p in productos])


# ==========================
# AGOTADOS
# ==========================
@app.route("/agotados", methods=["GET"])
def agotados():
    if "usuario" not in session:
        return redirect("/login")

    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM productos
        WHERE cantidad = 0
    """)

    productos = cursor.fetchall()
    conn.close()

    return jsonify([{
        "id": p["id"],
        "nombre": p["nombre"]
    } for p in productos])


# ==========================
# VENTAS
# ==========================
@app.route("/ventas")
def pagina_ventas():

    if "usuario" not in session:
        return redirect("/login")

    conn = conectar_db()
    cursor = conn.cursor()

    # HISTORIAL DE VENTAS
    cursor.execute("""
        SELECT v.id, p.nombre, v.cantidad, v.fecha
        FROM ventas v
        JOIN productos p ON p.id = v.producto_id
        ORDER BY v.id DESC
    """)
    ventas = cursor.fetchall()

    # PRODUCTOS DISPONIBLES PARA VENDER
    cursor.execute("""
        SELECT *
        FROM productos
        WHERE cantidad > 0
        ORDER BY nombre
    """)
    productos = cursor.fetchall()

    conn.close()

    return render_template(
        "ventas.html",
        ventas=ventas,
        productos=productos
    )


# ==========================
# REGISTRAR VENTA
# ==========================
@app.route("/ventas/registrar", methods=["POST"])
def registrar_venta():

    if "usuario" not in session:
        return redirect("/login")

    conn = conectar_db()
    cursor = conn.cursor()

    producto_id = int(request.form["id_producto"])
    cantidad = int(request.form["cantidad"])

    # BUSCAR PRODUCTO
    cursor.execute("""
        SELECT *
        FROM productos
        WHERE id = ?
    """, (producto_id,))

    producto = cursor.fetchone()

    if not producto:

        conn.close()

        return render_template(
            "ventas.html",
            error="Producto no encontrado"
        )

    # VALIDAR STOCK
    if producto["cantidad"] < cantidad:

        cursor.execute("""
            SELECT *
            FROM productos
            WHERE cantidad > 0
            ORDER BY nombre
        """)

        productos = cursor.fetchall()

        cursor.execute("""
            SELECT v.id, p.nombre, v.cantidad, v.fecha
            FROM ventas v
            JOIN productos p ON p.id = v.producto_id
            ORDER BY v.id DESC
        """)

        ventas = cursor.fetchall()

        conn.close()

        return render_template(
            "ventas.html",
            ventas=ventas,
            productos=productos,
            error="Stock insuficiente"
        )

    # DESCONTAR STOCK
    cursor.execute("""
        UPDATE productos
        SET cantidad = cantidad - ?
        WHERE id = ?
    """, (cantidad, producto_id))

    # GUARDAR VENTA
    cursor.execute("""
        INSERT INTO ventas (producto_id, cantidad)
        VALUES (?, ?)
    """, (producto_id, cantidad))

    # HISTORIAL
    cursor.execute("""
        INSERT INTO movimientos (descripcion)
        VALUES (?)
    """, (f"Venta realizada: {producto['nombre']} (-{cantidad})",))

    conn.commit()
    conn.close()

    return redirect("/ventas")

# ==========================
# RUN
# ==========================
if __name__ == "__main__":
    app.run(debug=True)