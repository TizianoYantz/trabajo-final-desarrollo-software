class Producto:
    def __init__(
        self,
        id_producto,
        nombre,
        cantidad,
        categoria,
        precio_unitario,
        stock_minimo=5
    ):
        self._id = id_producto
        self._nombre = nombre
        self._cantidad = cantidad
        self._categoria = categoria
        self._precio_unitario = precio_unitario
        self._stock_minimo = stock_minimo

    # Getters
    def obtener_id(self):
        return self._id

    def obtener_nombre(self):
        return self._nombre

    def obtener_cantidad(self):
        return self._cantidad

    def obtener_categoria(self):
        return self._categoria

    def obtener_precio_unitario(self):
        return self._precio_unitario

    def obtener_stock_minimo(self):
        return self._stock_minimo

    # Setters
    def modificar_nombre(self, nuevo_nombre):
        self._nombre = nuevo_nombre

    def modificar_cantidad(self, nueva_cantidad):
        if nueva_cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa")

        self._cantidad = nueva_cantidad

    def modificar_categoria(self, nueva_categoria):
        self._categoria = nueva_categoria

    def modificar_precio_unitario(self, nuevo_precio):
        if nuevo_precio < 0:
            raise ValueError("El precio no puede ser negativo")

        self._precio_unitario = nuevo_precio

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
        return (
            f"[{self._id}] "
            f"{self._nombre} "
            f"({self._categoria}) "
            f"- Stock: {self._cantidad} "
            f"- Precio: ${self._precio_unitario}"
        )
    def obtener_valor_total(self):
        return self._cantidad * self._precio_unitario
