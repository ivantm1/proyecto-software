class PrestamoVO:
    def __init__(self, isbn_libro, correo_estudiante, fecha_prestamo, fecha_devolucion, estado='Activo'):
        self._isbn_libro        = isbn_libro
        self._correo_estudiante = correo_estudiante
        self._fecha_prestamo    = fecha_prestamo
        self._fecha_devolucion  = fecha_devolucion
        self._estado            = estado
                                                          
        self._titulo      = ''
        self._autor       = ''
        self._nombre_tema = ''
        self._descripcion = ''

    @property
    def isbn_libro(self):        return self._isbn_libro
    @property
    def correo_estudiante(self): return self._correo_estudiante
    @property
    def fecha_prestamo(self):    return self._fecha_prestamo
    @property
    def fecha_devolucion(self):  return self._fecha_devolucion
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