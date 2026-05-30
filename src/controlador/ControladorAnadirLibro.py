class ControladorAnadirLibro:
    def __init__(self, ref_modelo, ref_vista_anadir, ref_vista_bibliotecario):
        self._modelo             = ref_modelo
        self._vista              = ref_vista_anadir
        self._vista_bibliotecario = ref_vista_bibliotecario

    def anadirLibro(self, titulo, isbn, autor, tema, descripcion):
        valido, mensaje = self._modelo.validarAltaLibro(titulo, isbn, autor, tema, descripcion)
        if not valido:
            self._vista.lanzarAviso(mensaje)
            return

        libro = self._modelo.crearLibroVO(titulo, isbn, autor, tema, descripcion)
        exito = self._modelo.altaLibro(libro)
        
        if exito:
            self._vista.mostrarResultado(f"Libro '{titulo}' añadido correctamente.")
            self._vista.lanzarAviso(f"Libro '{titulo}' añadido correctamente.")
            self._vista.limpiarFormulario()
        else:
            self._vista.lanzarAviso("Error al añadir el libro. Comprueba los datos e inténtalo de nuevo.")

    def volver(self):
        self._vista.limpiarFormulario()
        self._vista.close()
        self._vista_bibliotecario.showMaximized()