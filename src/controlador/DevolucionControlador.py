import datetime

class DevolucionControlador:
    def __init__(self, ref_modelo, ref_vista_devolucion, ref_vista_bibliotecario):
        self._modelo      = ref_modelo
        self._vista       = ref_vista_devolucion
        self._vista_anterior = ref_vista_bibliotecario

    def registrarDevolucion(self, isbn, estado_libro):
        # 1. Buscar el préstamo activo por ISBN
        prestamo = self._modelo.buscarPrestamoActivoPorISBN(isbn)
        if prestamo is None:
            self._vista.lanzarAviso("No se encontró ningún préstamo activo con ese ISBN.")
            return

        # 2. Calcular si hay retraso
        semanas_retraso = self._calcularSemanasRetraso(prestamo.fecha_devolucion)

        # 3. Registrar la devolución en BD (marca estado='Devuelto' y libro='Disponible')
        exito = self._modelo.registrarDevolucion(isbn)
        if not exito:
            self._vista.lanzarAviso("Error al registrar la devolución. Inténtalo de nuevo.")
            return

        mensajes = []
        # 4. Aplicar sanción si hay retraso
        if semanas_retraso > 0:
            self._modelo.aplicarSancionRetraso(prestamo.correo_estudiante, semanas_retraso)
            mensajes.append(f"Devolución registrada con {semanas_retraso} semana(s) de retraso.")
            mensajes.append("Se ha aplicado una sanción por retraso al estudiante.")

        if estado_libro in ["Dañado", "Roto"]:
            self._modelo.aplicarSancionDanio(prestamo.correo_estudiante, estado_libro)
            mensajes.append(f"El libro está {estado_libro.lower()}: se ha aplicado una sanción por daño al estudiante.")
            
        if not mensajes:
            mensaje = "Devolución registrada correctamente."
        else:
            mensaje = "\n".join(mensajes)

        self._vista.mostrarResultado(mensaje)
        self._vista.lanzarAviso(mensaje)
        self._vista.limpiarFormulario()

    def _calcularSemanasRetraso(self, fecha_devolucion):
        """Devuelve las semanas completas de retraso (0 si no hay retraso)."""
        if fecha_devolucion is None:
            return 0
        hoy = datetime.date.today()
        # fecha_devolucion puede llegar como string 'YYYY-MM-DD' o como date
        if isinstance(fecha_devolucion, str):
            fecha_devolucion = datetime.date.fromisoformat(fecha_devolucion[:10])
        if hoy <= fecha_devolucion:
            return 0
        dias_retraso = (hoy - fecha_devolucion).days
        return max(1, dias_retraso // 7)

    def volver(self):
        self._vista.limpiarFormulario()
        self._vista.close()
        self._vista_anterior.showMaximized()