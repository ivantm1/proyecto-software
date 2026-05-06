from src.vista.VistaLibroDisponible import VistaLibroDisponible
from src.vista.VistaLibroPrestado import VistaLibroPrestado

class CatalogoControlador:
    def __init__(self, ref_modelo, ref_vista_catalogo, ref_vista_estudiante, ref_vista_bibliotecario, correo_usuario=None, tipo_usuario=None):
        self._modelo          = ref_modelo
        self._vista_catalogo  = ref_vista_catalogo
        self._vista_estudiante = ref_vista_estudiante
        self._vista_bibliotecario = ref_vista_bibliotecario
        self._correo_usuario  = correo_usuario
        self._tipo_usuario    = tipo_usuario
        self._libroDisponible         = VistaLibroDisponible()
        self._libroPrestado        = VistaLibroPrestado()

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

    def abrirDetalleLibroDisponible(self, fila):
        libro = self._vista_catalogo.obtenerLibroPorFila(fila)
        if libro is None:
            return
        self._libroDisponible.controlador = self
        self._libroDisponible.mostrarLibro(libro)
        self._libroDisponible.show()

    def abrirDetalleLibroPrestado(self, fila):
        libro = self._vista_catalogo.obtenerLibroPorFila(fila)
        if libro is None:
            return
        self._libroPrestado.controlador = self
        self._libroPrestado.mostrarLibro(libro)
        self._libroPrestado.show()


    def reservarLibro(self, isbn):
        if not self._correo_usuario:
            self._libroPrestado.lanzarAviso("No hay usuario identificado.")
            return

        if self._modelo.tieneSancionActiva(self._correo_usuario):
            self._libroPrestado.lanzarAviso("Tienes una sanción activa y no puedes realizar reservas.")
            return

        if self._modelo.tienePrestamoActivo(isbn, self._correo_usuario):
            self._libroPrestado.lanzarAviso("No puedes reservar un libro que ya tienes prestado.")
            return

        exito = self._modelo.crearReserva(isbn, self._correo_usuario)
        if exito:
            self._libroPrestado.lanzarAviso("Reserva realizada con éxito.")
            self.cargarCatalogo()
        else:
            self._libroPrestado.lanzarAviso(
                "No se pudo reservar el libro. "
                "Puede que ya tengas una reserva activa."
            )

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

    def cerrarLibroDisponible(self):
        self._libroDisponible.close()

    def cerrarLibroPrestado(self):
        self._libroPrestado.close()

    def registroAtras(self):
        self._vista_catalogo.close()
        if self._tipo_usuario == "Bibliotecario":
            self._vista_bibliotecario.showMaximized()
        elif self._tipo_usuario == "Administrador":
            self._vista_administrador.showMaximized()
        else:
            self._vista_estudiante.showMaximized()