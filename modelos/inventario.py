from modelos.producto import Producto
from modelos.venta import Venta


class Inventario:
    def __init__(self):
        self._productos = []
        self._ventas = []
        self._proximo_id = 1
        self._movimientos = []

    def agregar_producto(
        self,
        nombre,
        cantidad,
        categoria,
        precio_unitario,
        stock_minimo=5
    ):

        producto_existente = self.buscar_por_nombre(nombre)

        if producto_existente:
            producto_existente.reponer_stock(cantidad)

            self.registrar_movimiento(
                f"Stock agregado: {nombre} (+{cantidad})"
            )

            return producto_existente

        producto = Producto(
            self._proximo_id,
            nombre,
            cantidad,
            categoria,
            precio_unitario,
            stock_minimo
        )

        self._productos.append(producto)

        self.registrar_movimiento(
            f"Producto agregado: {nombre} (+{cantidad})"
        )

        self._proximo_id += 1

        return producto

    def eliminar_producto(self, id_producto):
        producto = self.buscar_producto(id_producto)

        if producto:

            self.registrar_movimiento(
                f"Producto eliminado: {producto.obtener_nombre()}"
            )

            self._productos.remove(producto)
            return True

        return False

    def buscar_producto(self, id_producto):
        for producto in self._productos:
            if producto.obtener_id() == id_producto:
                return producto

        return None

    def buscar_por_nombre(self, nombre):
        for producto in self._productos:
            if producto.obtener_nombre().lower() == nombre.lower():
                return producto

        return None

    def listar_productos(self):
        return self._productos

    def actualizar_producto(
        self,
        id_producto,
        nuevo_nombre=None,
        nueva_cantidad=None,
        nueva_categoria=None,
        nuevo_precio_unitario=None,
        nuevo_stock_minimo=None
    ):
        producto = self.buscar_producto(id_producto)

        if producto is None:
            return False

        if nuevo_nombre is not None:
            producto.modificar_nombre(nuevo_nombre)

        if nueva_cantidad is not None:
            producto.modificar_cantidad(nueva_cantidad)

        if nueva_categoria is not None:
            producto.modificar_categoria(nueva_categoria)

        if nuevo_precio_unitario is not None:
            producto.modificar_precio_unitario(
                nuevo_precio_unitario
            )

        if nuevo_stock_minimo is not None:
            producto.modificar_stock_minimo(
                nuevo_stock_minimo
            )

        self.registrar_movimiento(
            f"Producto actualizado: {producto.obtener_nombre()}"
        )

        return True

    def reponer_producto(self, id_producto, cantidad):
        producto = self.buscar_producto(id_producto)

        if producto:
            producto.reponer_stock(cantidad)

            self.registrar_movimiento(
                f"Stock repuesto: {producto.obtener_nombre()} (+{cantidad})"
            )

            return True

        return False

    def vender_producto(self, id_producto, cantidad):
        producto = self.buscar_producto(id_producto)

        if producto is None:
            return False

        producto.descontar_stock(cantidad)

        self.registrar_movimiento(
            f"Venta registrada: {producto.obtener_nombre()} (-{cantidad})"
        )

        venta = Venta(producto, cantidad)
        self._ventas.append(venta)

        return True

    def obtener_ventas(self):
        return self._ventas

    def productos_agotados(self):
        return [
            producto
            for producto in self._productos
            if producto.esta_agotado()
        ]

    def productos_con_stock_bajo(self):
        return [
            producto
            for producto in self._productos
            if producto.tiene_stock_bajo()
        ]

    def obtener_valor_total_inventario(self):
        total = 0

        for producto in self._productos:
            total += producto.obtener_valor_total()

        return total

    def registrar_movimiento(self, descripcion):
        from modelos.movimiento import Movimiento

        movimiento = Movimiento(descripcion)

        self._movimientos.append(movimiento)

    def obtener_movimientos(self):
        return self._movimientos