from src.modelo.logica.LoggerSingleton import Logger

class ControladorAnadirLibro:
    def __init__(self, ref_modelo, ref_vista_anadir, ref_vista_bibliotecario, correo_actor=""):
        self._modelo              = ref_modelo
        self._vista               = ref_vista_anadir
        self._vista_bibliotecario = ref_vista_bibliotecario
        self._correo_actor        = correo_actor

    def anadirLibro(self, titulo, isbn, autor, tema, descripcion):
        valido, mensaje = self._modelo.validarAltaLibro(titulo, isbn, autor, tema, descripcion)
        if not valido:
            self._vista.lanzarAviso(mensaje)
            return

        libro = self._modelo.crearLibroVO(titulo, isbn, autor, tema, descripcion)
        exito = self._modelo.altaLibro(libro)
        
        if exito:
            Logger().alta_libro(isbn, titulo, actor=self._correo_actor)
            self._vista.mostrarResultado(f"Libro '{titulo}' añadido correctamente.")
            self._vista.lanzarAviso(f"Libro '{titulo}' añadido correctamente.")
            self._vista.limpiarFormulario()
        else:
            Logger().alta_libro_error(isbn, titulo)
            self._vista.lanzarAviso("Error al añadir el libro. Comprueba los datos e inténtalo de nuevo.")

    def volver(self):
        self._vista.limpiarFormulario()
        self._vista.close()
        self._vista_bibliotecario.showMaximized()