class ReservaVO:
    def __init__(self, isbn_libro, correo_estudiante, fecha_reserva):
        self._isbn_libro = isbn_libro
        self._correo_estudiante = correo_estudiante
        self._fecha_reserva = fecha_reserva

    @property
    def isbn_libro(self): return self._isbn_libro
    @property
    def correo_estudiante(self): return self._correo_estudiante
    @property
    def fecha_reserva(self): return self._fecha_reserva
