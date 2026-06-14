from flask import Flask, request, jsonify, render_template, redirect
from modelos.inventario import Inventario

app = Flask(__name__)

# Instancia única del inventario
inventario = Inventario()


# ==================================
# PÁGINAS HTML
# ==================================

@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/inventario")
def pagina_inventario():

    nombre_busqueda = request.args.get("buscar")

    # PRODUCTOS NORMALES
    if nombre_busqueda:

        productos = []

        for producto in inventario.listar_productos():

            if nombre_busqueda.lower() in producto.obtener_nombre().lower():
                productos.append(producto)

    else:
        productos = inventario.listar_productos()

    # ⚠ PRODUCTOS CON POCO STOCK (NUEVO)
    productos_poco_stock = []

    for producto in inventario.listar_productos():

        if producto.obtener_cantidad() < producto.obtener_stock_minimo():
            productos_poco_stock.append(producto)

    movimientos = inventario.obtener_movimientos()
    
    return render_template(
        "inventario.html",
        productos=productos,
        productos_poco_stock=productos_poco_stock,
        valor_total=inventario.obtener_valor_total_inventario(),
        movimientos=movimientos


    )


@app.route("/agregar-producto", methods=["POST"])
def agregar_producto_html():

    nombre = request.form["nombre"]
    cantidad = int(request.form["cantidad"])
    categoria = request.form["categoria"]
    precio_unitario = float(request.form["precio_unitario"])
    stock_minimo = int(request.form["stock_minimo"])

    inventario.agregar_producto(
        nombre,
        cantidad,
        categoria,
        precio_unitario,
        stock_minimo
    )

    return redirect("/inventario")


@app.route("/guardar-producto/<int:id_producto>", methods=["POST"])
def guardar_producto(id_producto):

    nombre = request.form["nombre"]
    categoria = request.form["categoria"]
    precio_unitario = float(request.form["precio_unitario"])
    cantidad = int(request.form["cantidad"])

    inventario.actualizar_producto(
        id_producto,
        nuevo_nombre=nombre,
        nueva_categoria=categoria,
        nuevo_precio_unitario=precio_unitario,
        nueva_cantidad=cantidad
    )

    return redirect("/inventario")


@app.route("/eliminar_producto/<int:id_producto>", methods=["POST"])
def eliminar_producto_html(id_producto):

    inventario.eliminar_producto(id_producto)

    return redirect("/inventario")


# ==================================
# VENTAS (HTML)
# ==================================

@app.route("/ventas")
def pagina_ventas():

    ventas = inventario.obtener_ventas()

    return render_template(
        "ventas.html",
        ventas=ventas
    )


@app.route("/registrar-venta", methods=["POST"])
def registrar_venta_html():

    id_producto = int(request.form["id_producto"])
    cantidad = int(request.form["cantidad"])

    try:
        inventario.vender_producto(
            id_producto,
            cantidad
        )

        return redirect("/ventas")

    except ValueError as e:

        ventas = inventario.obtener_ventas()

        return render_template(
            "ventas.html",
            ventas=ventas,
            error=str(e)
        )


# ==================================
# API PRODUCTOS
# ==================================

@app.route("/productos", methods=["GET"])
def obtener_productos():

    resultado = []

    for p in inventario.listar_productos():
        resultado.append({
            "id": p.obtener_id(),
            "nombre": p.obtener_nombre(),
            "categoria": p.obtener_categoria(),
            "precio_unitario": p.obtener_precio_unitario(),
            "cantidad": p.obtener_cantidad(),
            "stock_minimo": p.obtener_stock_minimo()
        })

    return jsonify(resultado)


@app.route("/productos", methods=["POST"])
def agregar_producto():

    data = request.json

    producto = inventario.agregar_producto(
        data["nombre"],
        data["cantidad"],
        data["categoria"],
        data["precio_unitario"],
        data.get("stock_minimo", 5)
    )

    return jsonify({
        "id": producto.obtener_id(),
        "nombre": producto.obtener_nombre(),
        "categoria": producto.obtener_categoria(),
        "precio_unitario": producto.obtener_precio_unitario(),
        "cantidad": producto.obtener_cantidad(),
        "stock_minimo": producto.obtener_stock_minimo()
    })


@app.route("/productos/<int:id_producto>", methods=["PUT"])
def actualizar_producto(id_producto):

    data = request.json

    exito = inventario.actualizar_producto(
        id_producto,
        nuevo_nombre=data.get("nombre"),
        nueva_cantidad=data.get("cantidad"),
        nueva_categoria=data.get("categoria"),
        nuevo_precio_unitario=data.get("precio_unitario"),
        nuevo_stock_minimo=data.get("stock_minimo")
    )

    if not exito:
        return jsonify({"error": "Producto no encontrado"}), 404

    return jsonify({"mensaje": "Producto actualizado"})


@app.route("/productos/<int:id_producto>", methods=["DELETE"])
def eliminar_producto(id_producto):

    exito = inventario.eliminar_producto(id_producto)

    if not exito:
        return jsonify({"error": "Producto no encontrado"}), 404

    return jsonify({"mensaje": "Producto eliminado"})


# ==================================
# REPONER STOCK
# ==================================

@app.route("/productos/<int:id_producto>/reponer", methods=["POST"])
def reponer_stock(id_producto):

    data = request.json

    exito = inventario.reponer_producto(
        id_producto,
        data["cantidad"]
    )

    if not exito:
        return jsonify({"error": "Producto no encontrado"}), 404

    return jsonify({"mensaje": "Stock repuesto correctamente"})


# ==================================
# STOCK BAJO (API)
# ==================================

@app.route("/stock-bajo", methods=["GET"])
def stock_bajo():

    resultado = []

    for p in inventario.productos_con_stock_bajo():
        resultado.append({
            "id": p.obtener_id(),
            "nombre": p.obtener_nombre(),
            "cantidad": p.obtener_cantidad(),
            "stock_minimo": p.obtener_stock_minimo()
        })

    return jsonify(resultado)


# ==================================
# PRODUCTOS AGOTADOS (API)
# ==================================

@app.route("/agotados", methods=["GET"])
def agotados():

    resultado = []

    for p in inventario.productos_agotados():
        resultado.append({
            "id": p.obtener_id(),
            "nombre": p.obtener_nombre()
        })

    return jsonify(resultado)


# ==================================
# VENTAS API
# ==================================

@app.route("/ventas/registrar", methods=["POST"])
def registrar_venta():

    data = request.json

    try:
        inventario.vender_producto(
            data["id_producto"],
            data["cantidad"]
        )

        return jsonify({
            "mensaje": "Venta registrada correctamente"
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400


@app.route("/ventas/historial", methods=["GET"])
def historial_ventas():

    resultado = []

    for venta in inventario.obtener_ventas():
        resultado.append({
            "producto": venta.obtener_producto().obtener_nombre(),
            "cantidad": venta.obtener_cantidad(),
            "fecha": venta.obtener_fecha().strftime("%d/%m/%Y %H:%M")
        })

    return jsonify(resultado)


# ==================================
# EJECUTAR APP
# ==================================

if __name__ == "__main__":
    app.run(debug=True)