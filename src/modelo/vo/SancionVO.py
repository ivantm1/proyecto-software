class SancionVO:
    def __init__(self, correo_estudiante, tipo, duracion_sancion, fecha_inicio, estado=None, fecha_fin=None):
        self._correo_estudiante = correo_estudiante
        self._tipo = tipo                     # "retraso" | "danio"
        self._duracion_sancion = duracion_sancion
        self._fecha_inicio = fecha_inicio
        self._estado = estado
        if fecha_fin is None and duracion_sancion is not None:
            from datetime import timedelta, date
            if isinstance(fecha_inicio, str):
                fecha_inicio = date.fromisoformat(fecha_inicio)
            self._fecha_fin = fecha_inicio + timedelta(days=duracion_sancion)
        else:
            self._fecha_fin = fecha_fin

    @property
    def correo_estudiante(self): return self._correo_estudiante
    @property
    def tipo(self): return self._tipo
    @property
    def duracion_sancion(self): return self._duracion_sancion
    @property
    def fecha_inicio(self): return self._fecha_inicio
    @property
    def estado(self): return self._estado
    @property
    def fecha_fin(self): return self._fecha_fin
