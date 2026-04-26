class DevolucionControlador:
    def __init__(self, ref_modelo, ref_vista):
        self._modelo = ref_modelo
        self._vista = ref_vista

    def registrarDevolucion(self, isbn):
        prestamo = self._modelo.buscarPorISBN(isbn)
        if prestamo is None:
            self._vista.lanzarAviso("No se encontró ningún libro con ese ISBN.")
            return

        exito = self._modelo.registrarDevolucion(isbn)
        if not exito:
            self._vista.lanzarAviso("Error al registrar la devolución.")
            return

        mensaje = "Devolución registrada correctamente."
        self._vista.lanzarAviso(mensaje)
        self._vista.mostrarResultado(mensaje)
