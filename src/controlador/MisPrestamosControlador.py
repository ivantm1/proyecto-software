from src.vista.VistaSeleccionPrestamo import VistaSeleccionPrestamo

class MisPrestamosControlador:
    def __init__(self, ref_modelo, ref_vista, ref_vista_estudiante, ref_vista_bibliotecario, correo_estudiante, tipo_usuario):
        self._modelo  = ref_modelo
        self._vista   = ref_vista
        self._vista_estudiante = ref_vista_estudiante
        self._vista_bibliotecario = ref_vista_bibliotecario
        self._correo  = correo_estudiante
        self._tipo_usuario = tipo_usuario
        self._detalle = VistaSeleccionPrestamo()

    def actualizarPrestamos(self):
        prestamos = self._modelo.obtenerPrestamosEstudiante(self._correo)
        self._vista.mostrarPrestamos(prestamos)

    def buscarPrestamos(self, titulo, tema):
        prestamos = self._modelo.buscarPrestamosEstudiante(self._correo, titulo, tema)
        self._vista.mostrarPrestamos(prestamos)

    def abrirDetallePrestamo(self, fila):
        prestamo = self._vista.obtenerPrestamoPorFila(fila)
        if prestamo is None:
            return
        self._detalle.controlador = self
        self._detalle.mostrarPrestamo(prestamo)
        self._detalle.show()

    def prorrogarPrestamo(self, isbn):
        exito = self._modelo.prorrogarPrestamo(isbn)
        if exito:
            self._detalle.lanzarAviso("Prórroga de 7 días aplicada correctamente.")
            self.actualizarPrestamos()
            self._detalle.close()
        else:
            self._detalle.lanzarAviso(
                "No se pudo prorrogar. "
                "El libro puede tener una reserva activa o ya fue prorrogado."
            )

    def registroAtras(self):
        self._vista.close()
        self._vista_estudiante.showMaximized()