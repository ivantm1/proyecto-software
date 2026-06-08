from src.vista.VistaSeleccionPrestamo import VistaSeleccionPrestamo

class ControladorMisPrestamos:
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
        self._detalle.mostrarPrestamo(prestamo, self._tipo_usuario)
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

    def terminarPrestamo(self, isbn):
        prestamo = self._modelo.buscarPrestamoActivoPorISBN(isbn)
        if prestamo is None:
            self._detalle.lanzarAviso("Este préstamo ya ha sido devuelto.")
            return

        exito = self._modelo.registrarDevolucion(isbn)
        if not exito:
            self._detalle.lanzarAviso("Este préstamo ya ha sido devuelto.")
            return

        semanas_retraso = self._modelo.calcularSemanasRetraso(prestamo.fecha_devolucion)
        if semanas_retraso > 0:
            self._modelo.aplicarSancionRetraso(prestamo.correo_estudiante, semanas_retraso)
            self._detalle.lanzarAviso(f"Préstamo terminado con {semanas_retraso} semana(s) de retraso. Se ha aplicado una sanción.")
        else:
            self._detalle.lanzarAviso("Préstamo terminado correctamente.")

        reserva = self._modelo.obtenerReservaPorLibro(isbn)
        if reserva:
            self._modelo.marcarReservaEspera(isbn)
            self._detalle.lanzarAviso(
                f"El libro devuelto tiene una reserva activa del alumno {reserva.correo_estudiante}.\n"
                "La reserva ha pasado a estado 'Espera'. El alumno tiene 7 días para recoger el libro.\n"
                "Si no lo recoge en ese plazo, la reserva se cancelará automáticamente."
            )

        self.actualizarPrestamos()
        self._detalle.close()

    def registroAtras(self):
        self._vista.close()
        if self._tipo_usuario == "Bibliotecario":
            resumen = self._modelo.obtenerResumenEstudiante(self._correo)
            if resumen:
                estudiante, num_prestamos, num_reservas, num_sanciones = resumen
                self._vista_estudiante.cargar_datos(estudiante, num_prestamos, num_reservas, num_sanciones)
        self._vista_estudiante.showMaximized()