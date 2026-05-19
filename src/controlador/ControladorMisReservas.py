                                                                  

class ControladorMisReservas:
    def __init__(self, ref_modelo, ref_vista, ref_vista_estudiante, ref_vista_bibliotecario, correo_estudiante, tipo_usuario):
        self._modelo  = ref_modelo
        self._vista   = ref_vista
        self._vista_estudiante = ref_vista_estudiante
        self._vista_bibliotecario = ref_vista_bibliotecario
        self._correo  = correo_estudiante
        self._tipo_usuario = tipo_usuario
                                                

    def actualizarReservas(self):
        reservas = self._modelo.obtenerReservasEstudiante(self._correo)
        for reserva in reservas:
            if self._modelo.reservaExpirada(reserva.isbn_libro):
                self._modelo.liberarReservaExpirada(reserva.isbn_libro)
        reservas = self._modelo.obtenerReservasEstudiante(self._correo)
        self._vista.mostrarReservas(reservas)

    def buscarReservas(self, titulo, tema):
        reservas = self._modelo.buscarReservasEstudiante(self._correo, titulo, tema)
        self._vista.mostrarReservas(reservas)

    def abrirDetalleReserva(self, fila):
        reserva = self._vista.obtenerReservaPorFila(fila)
        if reserva is None:
            return
        self._detalle.controlador = self
        self._detalle.mostrarReserva(reserva)
        self._detalle.show()

    def registroAtras(self):
        self._vista.close()
        self._vista_estudiante.showMaximized()