from src.vista.VistaLibroDisponible import VistaLibroDisponible
from src.vista.VistaLibroPrestado import VistaLibroPrestado
from src.vista.VistaLibroBibliotecario import VistaLibroBibliotecario
from src.vista.VistaLibroRetirado import VistaLibroRetirado
from PyQt5.QtWidgets import QMessageBox, QInputDialog

class ControladorCatalogo:
    def __init__(self, ref_modelo, ref_vista_catalogo, ref_vista_estudiante, ref_vista_bibliotecario, ref_vista_administrador=None, correo_usuario=None, tipo_usuario=None):
        self._modelo          = ref_modelo
        self._vista_catalogo  = ref_vista_catalogo
        self._vista_estudiante = ref_vista_estudiante
        self._vista_bibliotecario = ref_vista_bibliotecario
        self._vista_administrador = ref_vista_administrador
        self._correo_usuario  = correo_usuario
        self._tipo_usuario    = tipo_usuario
        self._libroDisponible         = VistaLibroDisponible()
        self._libroBibliotecario      = VistaLibroBibliotecario()
        self._libroPrestado        = VistaLibroPrestado()
        self._libroRetirado = VistaLibroRetirado()

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

        if self._tipo_usuario == "Bibliotecario":
            self._libroBibliotecario.controlador = self
            self._libroBibliotecario.mostrarLibro(libro)
            self._libroBibliotecario.show()
        else:
            self._libroDisponible.controlador = self
            self._libroDisponible.mostrarLibro(libro)
            self._libroDisponible.show()

    def abrirDetalleLibroPrestado(self, fila):
        libro = self._vista_catalogo.obtenerLibroPorFila(fila)
        if libro is None:
            return
        
        estudiante = None
        if self._tipo_usuario in ["Bibliotecario", "Administrador"]:
            estudiante = self._modelo.obtenerNombreEstudiantePrestamo(libro.isbn)
        
        self._libroPrestado.controlador = self
        self._libroPrestado.mostrarLibro(libro, estudiante, self._tipo_usuario)
        if self._tipo_usuario == "Bibliotecario":
            self._libroPrestado.boton_reserva.setVisible(False)
        else:
            self._libroPrestado.boton_reserva.setVisible(True)
        self._libroPrestado.show()


    def reservarLibro(self, isbn):
        if not self._correo_usuario:
            self._libroPrestado.lanzarAviso("No hay usuario identificado.")
            return

        valido, mensaje = self._modelo.validarReserva(isbn, self._correo_usuario)
        if not valido:
            self._libroPrestado.lanzarAviso(mensaje)
            return

        exito = self._modelo.crearReserva(isbn, self._correo_usuario)
        if exito:
            self._libroPrestado.lanzarAviso("Reserva realizada con éxito.")
            self.cargarCatalogo()
        else:
            self._libroPrestado.lanzarAviso(
                "No se pudo reservar el libro. "
                "Verifica que no excedas el límite de 3 reservas activas o que el libro esté disponible."
            )

    def bajaLibro(self, isbn, motivo="Retirado por el bibliotecario"):
        exito = self._modelo.bajaLibro(isbn, motivo)
        if exito:
            self._vista_catalogo.lanzarAviso("Libro retirado del catálogo.")
            self.cargarCatalogo()
        else:
            self._vista_catalogo.lanzarAviso(
                "No se pudo retirar el libro. "
                "Comprueba que no tenga préstamos o reservas activas."
            )
        return exito

    def ventanaAltaLibro(self):
        self._vista_catalogo.lanzarAviso("La ventana de Alta de libro aún no está implementada.")

    def verReservados(self):
        libros = self._modelo.obtenerReservados()
        self._vista_catalogo.cargar_lista_libros_bibliotecario(libros)

    def cerrarLibroDisponible(self):
        self._libroDisponible.close()

    def cerrarLibroBibliotecario(self):
        self._libroBibliotecario.close()

    def cerrarLibroPrestado(self):
        self._libroPrestado.close()

    def registroAtras(self):
        self._vista_catalogo.close()
        if self._tipo_usuario == "Bibliotecario":
            self._vista_bibliotecario.showMaximized()
        elif self._tipo_usuario == "Admin":
            self._vista_administrador.showMaximized()
        else:
            self._vista_estudiante.showMaximized()
            
    def abrirDetalleLibroRetirado(self, fila):
        libro = self._vista_catalogo.obtenerLibroPorFila(fila)
        if libro is None:
            return

        detalle = self._modelo.buscarRetiradoPorISBN(libro.isbn)
        if detalle is None:
            self._vista_catalogo.lanzarAviso("No se encontró información de retirada para este libro.")
            return

        libro_detalle, motivo, fecha_retiro = detalle
        self._libroRetirado.controlador = self
        self._libroRetirado.mostrarLibro(libro_detalle, motivo, fecha_retiro)
        self._libroRetirado.show()

    def restaurarLibro(self, isbn):
        exito = self._modelo.restaurarLibro(isbn)
        if exito:
            self._vista_catalogo.lanzarAviso("Libro restaurado al catálogo correctamente.")
            self.cargarCatalogo()
        else:
            self._vista_catalogo.lanzarAviso("Error al restaurar el libro.")

    def cerrarLibroRetirado(self):
        self._libroRetirado.close()