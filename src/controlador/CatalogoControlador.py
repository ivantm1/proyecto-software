from src.vista.VistaSeleccionLibro import VistaSeleccionLibro

class CatalogoControlador:
    def __init__(self, ref_modelo, ref_vista_catalogo, correo_usuario=None, tipo_usuario=None):
        self._modelo          = ref_modelo
        self._vista_catalogo  = ref_vista_catalogo
        self._correo_usuario  = correo_usuario
        self._tipo_usuario    = tipo_usuario
        self._detalle         = VistaSeleccionLibro()

    # ------------------------------------------------------------------
    # Catálogo y búsqueda
    # ------------------------------------------------------------------

    def cargarCatalogo(self):
        libros = self._modelo.obtenerCatalogo()
        if self._tipo_usuario == "Estudiante":
            self._vista_catalogo.cargar_lista_libros_estudiante(libros)
        else:
            self._vista_catalogo.cargar_lista_libros_bibliotecario(libros)

    def buscarLibro(self, titulo, tema):
        libros = self._modelo.buscarLibro(titulo, tema)
        if self._tipo_usuario == "Estudiante":
            self._vista_catalogo.cargar_lista_libros_estudiante(libros)
        else:
            self._vista_catalogo.cargar_lista_libros_bibliotecario(libros)

    # ------------------------------------------------------------------
    # Detalle del libro (doble clic)
    # ------------------------------------------------------------------

    def abrirDetalleLibro(self, fila):
        libro = self._vista_catalogo.obtenerLibroPorFila(fila)
        if libro is None:
            return
        self._detalle.controlador = self
        self._detalle.mostrarLibro(libro)
        self._detalle.show()

    # ------------------------------------------------------------------
    # Acciones Estudiante
    # ------------------------------------------------------------------

    def reservarLibro(self, isbn):
        if not self._correo_usuario:
            self._detalle.lanzarAviso("No hay usuario identificado.")
            return

        if self._modelo.tieneSancionActiva(self._correo_usuario):
            self._detalle.lanzarAviso("Tienes una sanción activa y no puedes realizar reservas.")
            return

        exito = self._modelo.crearReserva(isbn, self._correo_usuario)
        if exito:
            self._detalle.lanzarAviso("Reserva realizada con éxito.")
            self._detalle.close()
            self.cargarCatalogo()
        else:
            self._detalle.lanzarAviso(
                "No se pudo reservar el libro. "
                "Puede que ya tengas una reserva activa."
            )

    # ------------------------------------------------------------------
    # Acciones Bibliotecario
    # ------------------------------------------------------------------

    def bajaLibro(self, isbn):
        exito = self._modelo.bajaLibro(isbn)
        if exito:
            self._vista_catalogo.lanzarAviso("Libro retirado del catálogo.")
            self.cargarCatalogo()
        else:
            self._vista_catalogo.lanzarAviso(
                "No se pudo retirar el libro. "
                "Comprueba que no tenga préstamos o reservas activas."
            )

    def ventanaAltaLibro(self):
        self._vista_catalogo.lanzarAviso("La ventana de Alta de libro aún no está implementada.")

    def verReservados(self):
        libros = self._modelo.obtenerReservados()
        self._vista_catalogo.cargar_lista_libros_bibliotecario(libros)