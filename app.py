from flask import Flask, request, jsonify, render_template
from inventario import Inventario

# Crear app primero
app = Flask(__name__)

# Instancia del inventario
inventario = Inventario()

# =========================
# RUTA PRINCIPAL (HTML)
# =========================
@app.route("/")
def inicio():
    return render_template("index.html")


# =========================
# GET → obtener productos
# =========================
@app.route("/productos", methods=["GET"])
def obtener_productos():
    productos = inventario.listar_productos()

    resultado = []
    for p in productos:
        resultado.append({
            "id": p.obtener_id(),
            "nombre": p.obtener_nombre(),
            "cantidad": p.obtener_cantidad()
        })

    return jsonify(resultado)


# =========================
# POST → agregar producto
# =========================
@app.route("/productos", methods=["POST"])
def agregar_producto():
    data = request.json

    producto = inventario.agregar_producto(
        data["nombre"],
        data["cantidad"]
    )

    return jsonify({
        "id": producto.obtener_id(),
        "nombre": producto.obtener_nombre(),
        "cantidad": producto.obtener_cantidad()
    })


# =========================
# PUT → actualizar producto
# =========================
@app.route("/productos/<int:id_producto>", methods=["PUT"])
def actualizar_producto(id_producto):
    data = request.json

    exito = inventario.actualizar_producto(
        id_producto,
        nuevo_nombre=data.get("nombre"),
        nueva_cantidad=data.get("cantidad")
    )

    if not exito:
        return jsonify({"error": "Producto no encontrado"}), 404

    return jsonify({"mensaje": "Producto actualizado"})


# =========================
# DELETE → eliminar producto
# =========================
@app.route("/productos/<int:id_producto>", methods=["DELETE"])
def eliminar_producto(id_producto):
    exito = inventario.eliminar_producto(id_producto)

    if not exito:
        return jsonify({"error": "Producto no encontrado"}), 404

    return jsonify({"mensaje": "Producto eliminado"})


# =========================
# EJECUTAR
# =========================
if __name__ == "__main__":
    app.run(debug=True)