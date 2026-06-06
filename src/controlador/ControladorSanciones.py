from src.modelo.logica.LoggerSingleton import Logger

class ControladorSanciones:
    def __init__(self, ref_modelo, ref_vista, ref_vista_gestion=None):
        self._modelo = ref_modelo
        self._vista = ref_vista
        self._vista_gestion = ref_vista_gestion
        self._estudiante_actual = None

    def cargarSanciones(self, correo_estudiante):
        sanciones = self._modelo.obtenerSancionesEstudiante(correo_estudiante)
        self._vista.mostrarSanciones(sanciones)

    def aplicarSancion(self, correo_estudiante, motivo, dias):
        resultado = self._modelo.aplicarSancionManual(correo_estudiante, motivo, dias)

        if resultado:
            Logger().sancion_aplicada(correo_estudiante, "manual", f"motivo={motivo} dias={dias}")
            self._vista.lanzarAviso(
                f"Se ha aplicado una sanción por {motivo.lower()}"
            )
            self.cargarSanciones(correo_estudiante)
        else:
            self._vista.lanzarAviso("Error al aplicar la sanción.")
        return resultado

    def eliminarSancion(self, correo_estudiante, tipo, fecha_inicio, duracion):
        resultado = self._modelo.eliminarSancion(correo_estudiante, tipo, fecha_inicio, duracion)
        if resultado:
            Logger().sancion_eliminada(correo_estudiante, tipo)
            self._vista.lanzarAviso("Sanción eliminada correctamente.")
            self.cargarSanciones(correo_estudiante)
        else:
            self._vista.lanzarAviso("No se pudo eliminar la sanción seleccionada.")
        return resultado

    def volverASanciones(self):
        if self._vista:
            self._vista.close()

        if self._vista_gestion:
            controlador_gestion = getattr(self._vista_gestion, 'controlador', None)
            if controlador_gestion and hasattr(controlador_gestion, 'volverASanciones'):
                controlador_gestion.volverASanciones()
                return

            self._vista_gestion.showMaximized()
