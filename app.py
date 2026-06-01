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

    productos = inventario.listar_productos()

    return render_template(
        "inventario.html",
        productos=productos
    )

@app.route("/agregar-producto", methods=["POST"])
def agregar_producto_html():

    nombre = request.form["nombre"]
    cantidad = int(request.form["cantidad"])
    stock_minimo = int(request.form["stock_minimo"])

    inventario.agregar_producto(
        nombre,
        cantidad,
        stock_minimo
    )

    return redirect("/inventario")


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

    inventario.vender_producto(
        id_producto,
        cantidad
    )

    return redirect("/ventas")

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
        data.get("stock_minimo", 5)
    )

    return jsonify({
        "id": producto.obtener_id(),
        "nombre": producto.obtener_nombre(),
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
# STOCK BAJO
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
# PRODUCTOS AGOTADOS
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
# API VENTAS
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