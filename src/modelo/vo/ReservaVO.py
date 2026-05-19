class ReservaVO:
    def __init__(self, isbn_libro, correo_estudiante, fecha_reserva, estado='Pendiente'):
        self._isbn_libro = isbn_libro
        self._correo_estudiante = correo_estudiante
        self._fecha_reserva = fecha_reserva
        self._estado = estado
                                                          
        self._titulo      = ''
        self._autor       = ''
        self._nombre_tema = ''
        self._descripcion = ''

    @property
    def isbn_libro(self): return self._isbn_libro
    @property
    def correo_estudiante(self): return self._correo_estudiante
    @property
    def fecha_reserva(self): return self._fecha_reserva
    @property
    def estado(self):            return self._estado
    @property
    def titulo(self):            return self._titulo
    @property
    def autor(self):             return self._autor
    @property
    def nombre_tema(self):       return self._nombre_tema
    @property
    def descripcion(self):       return self._descripcion