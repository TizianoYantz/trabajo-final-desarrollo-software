from datetime import datetime

class Movimiento:

    def __init__(self, descripcion):
        self._descripcion = descripcion
        self._fecha = datetime.now()

    def obtener_descripcion(self):
        return self._descripcion

    def obtener_fecha(self):
        return self._fecha