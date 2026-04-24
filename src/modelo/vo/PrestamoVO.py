class PrestamoVO:
    def __init__(self, isbn_libro, correo_estudiante, fecha_prestamo, fecha_devolucion):
        self._isbn_libro = isbn_libro
        self._correo_estudiante = correo_estudiante
        self._fecha_prestamo = fecha_prestamo
        self._fecha_devolucion = fecha_devolucion

    @property
    def isbn_libro(self): return self._isbn_libro
    @property
    def correo_estudiante(self): return self._correo_estudiante
    @property
    def fecha_prestamo(self): return self._fecha_prestamo
    @property
    def fecha_devolucion(self): return self._fecha_devolucion
    @fecha_devolucion.setter
    def fecha_devolucion(self, nueva_fecha): self._fecha_devolucion = nueva_fecha
