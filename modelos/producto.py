
class Producto:
    def __init__(self, id_producto, nombre, cantidad, stock_minimo=5):
        self._id = id_producto
        self._nombre = nombre
        self._cantidad = cantidad
        self._stock_minimo = stock_minimo

    # Getters
    def obtener_id(self):
        return self._id

    def obtener_nombre(self):
        return self._nombre

    def obtener_cantidad(self):
        return self._cantidad

    def obtener_stock_minimo(self):
        return self._stock_minimo

    # Setters
    def modificar_nombre(self, nuevo_nombre):
        self._nombre = nuevo_nombre

    def modificar_cantidad(self, nueva_cantidad):
        if nueva_cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa")

        self._cantidad = nueva_cantidad

    def modificar_stock_minimo(self, nuevo_stock):
        if nuevo_stock >= 0:
            self._stock_minimo = nuevo_stock

    # Métodos de negocio
    def reponer_stock(self, cantidad):
        if cantidad > 0:
            self._cantidad += cantidad

    def descontar_stock(self, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero")

        if cantidad > self._cantidad:
            raise ValueError("Stock insuficiente")

        self._cantidad -= cantidad

    def tiene_stock_bajo(self):
        return self._cantidad <= self._stock_minimo

    def esta_agotado(self):
        return self._cantidad == 0

    def __str__(self):
        return f"[{self._id}] {self._nombre} - Stock: {self._cantidad}"