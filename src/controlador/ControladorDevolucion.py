class ControladorDevolucion:
    def __init__(self, ref_modelo, ref_vista_devolucion, ref_vista_bibliotecario):
        self._modelo      = ref_modelo
        self._vista       = ref_vista_devolucion
        self._vista_anterior = ref_vista_bibliotecario

    def registrarDevolucion(self, isbn, estado_libro):
        if not isbn:
            self._vista.lanzarAviso("Por favor, introduce un ISBN válido.")
            return

        prestamo = self._modelo.buscarPrestamoActivoPorISBN(isbn)
        if prestamo is None:
            self._vista.lanzarAviso("No se encontró ningún préstamo activo con ese ISBN.")
            return

        exito = self._modelo.registrarDevolucion(isbn)
        if not exito:
            self._vista.lanzarAviso("Error al registrar la devolución. Inténtalo de nuevo.")
            return

        semanas_retraso = self._modelo.calcularSemanasRetraso(prestamo.fecha_devolucion)

        mensajes = []
        if semanas_retraso > 0:
            self._modelo.aplicarSancionRetraso(prestamo.correo_estudiante, semanas_retraso)
            mensajes.append(f"Devolución registrada con {semanas_retraso} semana(s) de retraso.")
            mensajes.append("Se ha aplicado una sanción por retraso al estudiante.")

        if estado_libro in ["Dañado", "Roto"]:
            mensajes.append(f"El libro está {estado_libro.lower()}: no se aplica sanción automática.")
            
        if not mensajes:
            mensaje = "Devolución registrada correctamente."
        else:
            mensaje = "\n".join(mensajes)

        self._vista.mostrarResultado(mensaje)
        self._vista.lanzarAviso(mensaje)
        self._vista.limpiarFormulario()

    def volver(self):
        self._vista.limpiarFormulario()
        self._vista.close()
        self._vista_anterior.showMaximized()