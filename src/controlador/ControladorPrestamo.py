class ControladorPrestamo:
    def __init__(self, ref_vista):
        self._vista = ref_vista

    def registrarPrestamo(self, id_usuario, isbn, ref_modelo):
        if not id_usuario or not isbn:
            self._vista.lanzarAviso("Por favor, introduce el ID de usuario y el ISBN.")
            return

        try:
            id_usuario = int(id_usuario)
        except ValueError:
            self._vista.lanzarAviso("El ID de usuario debe ser un número.")
            return

        valido, mensaje = ref_modelo.validarPrestamo(isbn, str(id_usuario))
        if not valido:
            self._vista.lanzarAviso(mensaje)
            return

        resultado = ref_modelo.registrarPrestamo(isbn, str(id_usuario))
        if resultado:
            self._vista.lanzarAviso(f"Préstamo registrado con éxito. Fecha de devolución: {resultado.fecha_devolucion}")
            self.cargarPrestamosUsuario(str(id_usuario), ref_modelo)
        else:
            self._vista.lanzarAviso("Error al registrar el préstamo.")

    def devolverPrestamo(self, id_prestamo, isbn, ref_modelo):
        if not id_prestamo:
            self._vista.lanzarAviso("ID de préstamo inválido.")
            return

        try:
            id_prestamo = int(id_prestamo)
        except ValueError:
            self._vista.lanzarAviso("ID de préstamo inválido.")
            return

        prestamo = ref_modelo.buscarPrestamoActivoPorISBN(isbn)
        if prestamo is None:
            self._vista.lanzarAviso("No se encontró el préstamo.")
            return

        exito = ref_modelo.registrarDevolucion(isbn)
        if not exito:
            self._vista.lanzarAviso("Error al registrar la devolución.")
            return

        semanas_retraso = ref_modelo.calcularSemanasRetraso(prestamo.fecha_devolucion)
        if semanas_retraso > 0:
            ref_modelo.aplicarSancionRetraso(prestamo.correo_estudiante, semanas_retraso)
            self._vista.lanzarAviso(
                f"Devolución registrada con retraso. Se ha aplicado una sanción."
            )
        else:
            self._vista.lanzarAviso("Devolución registrada correctamente.")

        self.cargarPrestamosUsuario(str(prestamo.correo_estudiante), ref_modelo)

    def cargarPrestamosUsuario(self, id_usuario, ref_modelo):
        try:
            int(id_usuario)
        except ValueError:
            self._vista.lanzarAviso("El ID de usuario debe ser un número.")
            return

        prestamos = ref_modelo.obtenerPrestamosEstudiante(id_usuario)
        self._vista.mostrarPrestamos(prestamos)
