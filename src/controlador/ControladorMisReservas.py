                                                                  

class ControladorMisReservas:
    def __init__(self, ref_modelo, ref_vista, ref_vista_origen, correo_estudiante, tipo_usuario):
        self._modelo  = ref_modelo
        self._vista   = ref_vista
        self._vista_origen = ref_vista_origen
        self._correo  = correo_estudiante
        self._tipo_usuario = tipo_usuario
                                                

    def actualizarReservas(self):
        if self._correo is None:
            reservas = self._modelo.obtenerTodasReservas()
        else:
            reservas = self._modelo.actualizarReservasEstudiante(self._correo)
        self._vista.mostrarReservas(reservas)

    def buscarReservas(self, titulo, tema):
        if self._correo is None:
            self.actualizarReservas()
        else:
            reservas = self._modelo.buscarReservasEstudiante(self._correo, titulo, tema)
            self._vista.mostrarReservas(reservas)

    def finalizarReservaCaducada(self, isbn):
        return self._modelo.cancelarReservaCaducada(isbn)

    def registroAtras(self):
        self._vista.close()
        self._vista_origen.showMaximized()
        return