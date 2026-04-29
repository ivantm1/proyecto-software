class CatalogoControlador:
    """
    Controlador para la vista Catalogo.
    Soporta los dos roles: Estudiante (reservar) y Bibliotecario
    (alta, baja, ver reservados).

    Recibe un LogicaExtension como modelo para acceder a los DAOs
    de Libro y Reserva.
    """

    def __init__(self, ref_modelo, ref_vista_catalogo, correo_usuario=None, tipo_usuario=None):
        self._modelo = ref_modelo
        self._vista_catalogo = ref_vista_catalogo
        self._correo_usuario = correo_usuario
        self._tipo_usuario = tipo_usuario

    # ------------------------------------------------------------------
    # Catálogo y búsqueda
    # ------------------------------------------------------------------

    def cargarCatalogo(self):
        libros = self._modelo.obtenerCatalogo()
        self._vista_catalogo.cargar_lista_libros(libros)

    def buscarPorTitulo(self, titulo):
        libros = self._modelo.buscarPorTitulo(titulo)
        self._vista_catalogo.mostrarLibros(libros)

    def buscarPorTema(self, tema):
        libros = self._modelo.buscarPorTema(tema)
        self._vista_catalogo.mostrarLibros(libros)
    
    def buscarLibro(self, titulo, tema):
        libros = self._modelo.buscarLibro(titulo, tema)
        if self._tipo_usuario == "estudiante":
            self._vista_catalogo.cargar_lista_libros_estudiante(libros)
        else:
            self._vista_catalogo.cargar_lista_libros_bibliotecario(libros)

    # ------------------------------------------------------------------
    # Acciones Estudiante
    # ------------------------------------------------------------------

    def reservarLibro(self, isbn):
        if not self._correo_usuario:
            self._vista_catalogo.lanzarAviso("No hay usuario identificado.")
            return

        if self._modelo.tieneSancionActiva(self._correo_usuario):
            self._vista_catalogo.lanzarAviso(
                "Tienes una sanción activa y no puedes realizar reservas."
            )
            return

        exito = self._modelo.crearReserva(isbn, self._correo_usuario)
        if exito:
            self._vista_catalogo.lanzarAviso("Reserva realizada con éxito.")
            self.cargarCatalogo()
        else:
            self._vista_catalogo.lanzarAviso(
                "No se pudo reservar el libro. "
                "Puede que ya tenga una reserva activa."
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
        self._vista_catalogo.lanzarAviso(
            "La ventana de Alta de libro aún no está implementada."
        )

    def verReservados(self):
        libros = self._modelo.obtenerReservados()
        self._vista_catalogo.mostrarLibros(libros)
