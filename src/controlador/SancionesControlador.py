class SancionesControlador:
    """
    Controlador para la vista Sanciones (rol Bibliotecario).
    Gestiona la consulta y aplicación de sanciones manuales.
    """

    def __init__(self, ref_modelo, ref_vista):
        self._modelo = ref_modelo
        self._vista = ref_vista

    def cargarSanciones(self, correo_estudiante):
        sanciones = self._modelo.obtenerSancionesEstudiante(correo_estudiante)
        self._vista.mostrarSanciones(sanciones)

    def aplicarSancionDanio(self, correo_estudiante, semanas):
        resultado = self._modelo.aplicarSancionDanio(correo_estudiante, semanas)
        if resultado:
            self._vista.lanzarAviso(
                f"Sanción de {semanas} semana(s) aplicada correctamente."
            )
            self.cargarSanciones(correo_estudiante)
        else:
            self._vista.lanzarAviso("Error al aplicar la sanción.")
