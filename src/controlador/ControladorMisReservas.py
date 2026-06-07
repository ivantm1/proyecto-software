                                                                  

class ControladorMisReservas:
    def __init__(self, ref_modelo, ref_vista, ref_vista_estudiante, ref_vista_bibliotecario, ref_vista_buscar_estudiante, correo_estudiante, tipo_usuario):
        self._modelo  = ref_modelo
        self._vista   = ref_vista
        self._vista_estudiante = ref_vista_estudiante
        self._vista_bibliotecario = ref_vista_bibliotecario
        self._vista_buscar_estudiante = ref_vista_buscar_estudiante
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

    def registroAtras(self):
        self._vista.close()
        if self._tipo_usuario == "Bibliotecario":
            self._vista_buscar_estudiante.showMaximized()
        else:
            self._vista_estudiante.showMaximized()