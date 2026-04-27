class Producto:
    def __init__(self, id, nombre, cantidad):
        self._id = id
        self._nombre = nombre
        self._cantidad = cantidad

    # Getters
    def obtener_id(self):
        return self._id

    def obtener_nombre(self):
        return self._nombre

    def obtener_cantidad(self):
        return self._cantidad

    # Setters
    def modificar_nombre(self, nuevo_nombre):
        self._nombre = nuevo_nombre

    def modificar_cantidad(self, nueva_cantidad):
        if nueva_cantidad >= 0:
            self._cantidad = nueva_cantidad
        else:
            raise ValueError("La cantidad no puede ser negativa")

    def __str__(self):
        return f"[{self._id}] {self._nombre} - Stock: {self._cantidad}"


class Inventario:
    def __init__(self):
        self._productos = []
        self._proximo_id = 1

    def agregar_producto(self, nombre, cantidad):
        producto = Producto(self._proximo_id, nombre, cantidad)
        self._productos.append(producto)
        self._proximo_id += 1
        return producto

    def eliminar_producto(self, id_producto):
        for producto in self._productos:
            if producto.obtener_id() == id_producto:
                self._productos.remove(producto)
                return True
        return False

    def buscar_producto(self, id_producto):
        for producto in self._productos:
            if producto.obtener_id() == id_producto:
                return producto
        return None

    def listar_productos(self):
        return self._productos
    
    def actualizar_producto(self, id_producto, nuevo_nombre=None, nueva_cantidad=None):
        producto = self.buscar_producto(id_producto)

        if producto is None:
            return False

        if nuevo_nombre is not None:
            producto.modificar_nombre(nuevo_nombre)

        if nueva_cantidad is not None:
            producto.modificar_cantidad(nueva_cantidad)

        return True

    