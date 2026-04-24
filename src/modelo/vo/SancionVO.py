class SancionVO:
    def __init__(self, correo_estudiante, tipo, semanas_sancion, fecha_inicio):
        self._correo_estudiante = correo_estudiante
        self._tipo = tipo                     # "retraso" | "danio"
        self._semanas_sancion = semanas_sancion
        self._fecha_inicio = fecha_inicio

    @property
    def correo_estudiante(self): return self._correo_estudiante
    @property
    def tipo(self): return self._tipo
    @property
    def semanas_sancion(self): return self._semanas_sancion
    @property
    def fecha_inicio(self): return self._fecha_inicio
