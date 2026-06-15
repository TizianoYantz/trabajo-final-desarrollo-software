import sqlite3
from flask import Flask, request, jsonify, render_template, redirect

app = Flask(__name__)

# ==========================
# CONEXIÓN DB
# ==========================
def conectar_db():
    conn = sqlite3.connect("inventario.db")
    conn.row_factory = sqlite3.Row
    return conn


# ==========================
# PÁGINA PRINCIPAL
# ==========================
@app.route("/")
def inicio():
    return render_template("index.html")


# ==========================
# INVENTARIO
# ==========================
@app.route("/inventario")
def pagina_inventario():

    nombre_busqueda = request.args.get("buscar")

    conn = conectar_db()
    cursor = conn.cursor()

    # PRODUCTOS
    if nombre_busqueda:
        cursor.execute("""
            SELECT * FROM productos
            WHERE LOWER(nombre) LIKE ?
        """, ('%' + nombre_busqueda.lower() + '%',))
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
        SELECT SUM(precio_unitario * cantidad) as total
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

    # 🆕 CATEGORÍAS ÚNICAS (SIN DUPLICADOS)
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
        categorias=categorias
    )
# ==========================
# AGREGAR PRODUCTO
# ==========================
@app.route("/agregar-producto", methods=["POST"])
def agregar_producto_html():

    conn = conectar_db()
    cursor = conn.cursor()

    nombre = request.form.get("nombre")
    cantidad = int(request.form.get("cantidad"))

    categoria = request.form.get("categoria")
    precio_unitario = float(request.form.get("precio_unitario"))
    stock_minimo = int(request.form.get("stock_minimo"))

    cursor.execute("""
        INSERT INTO productos (nombre, categoria, precio_unitario, cantidad, stock_minimo)
        VALUES (?, ?, ?, ?, ?)
    """, (
        nombre,
        categoria,
        precio_unitario,
        cantidad,
        stock_minimo
    ))

    # 🔥 MOVIMIENTO CON CANTIDAD
    cursor.execute("""
        INSERT INTO movimientos (descripcion)
        VALUES (?)
    """, (f"Se agregó producto {nombre} (+{cantidad})",))

    conn.commit()
    conn.close()

    return redirect("/inventario")
# ==========================
# EDITAR PRODUCTO
# ==========================
@app.route("/guardar-producto/<int:id_producto>", methods=["POST"])
def guardar_producto(id_producto):

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
# VENTAS (TEMPORAL)
# ==========================
@app.route("/ventas")
def pagina_ventas():

    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT v.id, p.nombre, v.cantidad, v.fecha
        FROM ventas v
        JOIN productos p ON p.id = v.producto_id
        ORDER BY v.id DESC
    """)

    ventas = cursor.fetchall()
    conn.close()

    return render_template("ventas.html", ventas=ventas)


@app.route("/ventas/registrar", methods=["POST"])
def registrar_venta():

    conn = conectar_db()
    cursor = conn.cursor()

    producto_id = int(request.form["id_producto"])
    cantidad = int(request.form["cantidad"])

    # 🔍 buscar producto
    cursor.execute("""
        SELECT * FROM productos WHERE id = ?
    """, (producto_id,))

    producto = cursor.fetchone()

    if not producto:
        conn.close()
        return jsonify({"error": "Producto no encontrado"}), 404

    # ❌ validar stock
    if producto["cantidad"] < cantidad:
        conn.close()
        return jsonify({"error": "Stock insuficiente"}), 400

    # 🔻 descontar stock
    cursor.execute("""
        UPDATE productos
        SET cantidad = cantidad - ?
        WHERE id = ?
    """, (cantidad, producto_id))

    # 🧾 guardar venta
    cursor.execute("""
        INSERT INTO ventas (producto_id, cantidad)
        VALUES (?, ?)
    """, (producto_id, cantidad))

    # 📜 movimiento historial
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