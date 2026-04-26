class MisPrestamosControlador:
    """
    Controlador para la vista MisPrestamos (rol Estudiante).
    Gestiona la consulta y prórroga de préstamos propios.
    """

    def __init__(self, ref_modelo, ref_vista, correo_estudiante):
        self._modelo = ref_modelo
        self._vista = ref_vista
        self._correo = correo_estudiante

    def actualizarPrestamos(self):
        prestamos = self._modelo.obtenerPrestamosEstudiante(self._correo)
        self._vista.mostrarPrestamos(prestamos)

    def prorrogarPrestamo(self, isbn):
        exito = self._modelo.prorrogarPrestamo(isbn)
        if exito:
            self._vista.lanzarAviso("Prórroga de 7 días aplicada correctamente.")
            self.actualizarPrestamos()
        else:
            self._vista.lanzarAviso(
                "No se pudo prorrogar. "
                "El libro puede tener una reserva activa o ya fue prorrogado."
            )
