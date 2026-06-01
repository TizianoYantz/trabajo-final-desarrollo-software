from datetime import datetime


class Venta:
    def __init__(self, producto, cantidad):
        self._producto = producto
        self._cantidad = cantidad
        self._fecha = datetime.now()

    def obtener_producto(self):
        return self._producto

    def obtener_cantidad(self):
        return self._cantidad

    def obtener_fecha(self):
        return self._fecha

    def __str__(self):
        return (
            f"Venta - Producto: {self._producto.obtener_nombre()} "
            f"| Cantidad: {self._cantidad} "
            f"| Fecha: {self._fecha.strftime('%d/%m/%Y %H:%M')}"
        )