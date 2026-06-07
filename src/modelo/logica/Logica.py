from ..dao.UserDaoJDBC import UserDaoJDBC
from .LogicaInicioSesion import LogicaInicioSesion
from .LogicaLibros import LogicaLibros
from .LogicaPrestamos import LogicaPrestamos
from .LogicaReservas import LogicaReservas
from .LogicaSanciones import LogicaSanciones
from .LogicaEstudiantes import LogicaEstudiantes
from .LogicaCopiaSeguridad import LogicaCopiaSeguridad

class Logica:
    def __init__(self):
        self._sesion = LogicaInicioSesion()
        self._libros = LogicaLibros()
        self._prestamos = LogicaPrestamos()
        self._reservas = LogicaReservas()
        self._sanciones = LogicaSanciones()
        self._estudiantes = LogicaEstudiantes()
        self._copias = LogicaCopiaSeguridad()

    def comprobarLogin(self, loginVO):
        return self._sesion.comprobarLogin(loginVO)

    def registrarUsuario(self, registroVO):
        return self._sesion.registrarUsuario(registroVO)

    def validarRegistroAdmin(self, nombre, apellidos, correo, contrasena, confirmar, tipo):
        return self._sesion.validarRegistroAdmin(nombre, apellidos, correo, contrasena, confirmar, tipo)

    def validarCambioContrasena(self, correo, actual, nueva, confirmar):
        return self._sesion.validarCambioContrasena(correo, actual, nueva, confirmar)

    def obtenerUsuarioPorCorreo(self, correo):
        return self._sesion.obtenerUsuarioPorCorreo(correo)

    def eliminarUsuario(self, correo):
        return self._sesion.eliminarUsuario(correo)

    def validarRegistro(self, nombre, apellidos, correo, contrasena, confirmar):
        return self._sesion.validarRegistro(nombre, apellidos, correo, contrasena, confirmar)

                                       
    def buscarLibro(self, linea_busqueda, tema):
        return self._libros.buscarLibro(linea_busqueda, tema)

    def obtenerCatalogo(self):
        return self._libros.obtenerCatalogo()

    def altaLibro(self, libroVO):
        return self._libros.altaLibro(libroVO)

    def bajaLibro(self, isbn, motivo="Retirado por el bibliotecario"):
        return self._libros.bajaLibro(isbn, motivo)

    def restaurarLibro(self, isbn):
        return self._libros.restaurarLibro(isbn)

    def obtenerReservados(self):
        return self._libros.obtenerReservados()

    def buscarPorISBN(self, isbn):
        return self._libros.buscarPorISBN(isbn)

    def buscarRetiradoPorISBN(self, isbn):
        return self._libros.buscarRetiradoPorISBN(isbn)

    def validarAltaLibro(self, titulo, isbn, autor, tema, descripcion):
        return self._libros.validarAltaLibro(titulo, isbn, autor, tema, descripcion)

    def crearLibroVO(self, titulo, isbn, autor, tema, descripcion):
        return self._libros.crearLibroVO(titulo, isbn, autor, tema, descripcion)

                                          
    def registrarPrestamo(self, isbn, correo_estudiante):
        return self._prestamos.registrarPrestamo(isbn, correo_estudiante)

    def registrarDevolucion(self, isbn):
        return self._prestamos.registrarDevolucion(isbn)

    def buscarPrestamoActivoPorISBN(self, isbn):
        return self._prestamos.buscarPrestamoActivoPorISBN(isbn)

    def tieneCooldown(self, correo_estudiante, isbn):
        return self._prestamos.tieneCooldown(correo_estudiante, isbn)

    def obtenerPrestamosEstudiante(self, correo_estudiante):
        return self._prestamos.obtenerPrestamosEstudiante(correo_estudiante)

    def obtenerPrestamosProximos(self, correo_estudiante):
        return self._prestamos.obtenerPrestamosProximos(correo_estudiante)

    def prorrogarPrestamo(self, isbn):
        return self._prestamos.prorrogarPrestamo(isbn)

    def contarPrestamosEstudiante(self, correo_estudiante):
        return self._prestamos.contarPrestamosEstudiante(correo_estudiante)

    def buscarPrestamosEstudiante(self, correo_estudiante, titulo='', tema='Ninguno'):
        return self._prestamos.buscarPrestamosEstudiante(correo_estudiante, titulo, tema)

    def tienePrestamoActivo(self, isbn, correo_estudiante):
        return self._prestamos.tienePrestamoActivo(isbn, correo_estudiante)

    def validarPrestamo(self, isbn, correo_estudiante):
        return self._prestamos.validarPrestamo(isbn, correo_estudiante)

    def obtenerNombreEstudiantePrestamo(self, isbn):
        return self._prestamos.obtenerNombreEstudiantePrestamo(isbn)

                                          
    def aplicarSancionRetraso(self, correo_estudiante, semanas_retraso):
        return self._sanciones.aplicarSancionRetraso(correo_estudiante, semanas_retraso)

    def aplicarSancionDanio(self, correo_estudiante, estado_libro):
        return self._sanciones.aplicarSancionDanio(correo_estudiante, estado_libro)

    def aplicarSancionManual(self, correo_estudiante, motivo, dias):
        return self._sanciones.aplicarSancionManual(correo_estudiante, motivo, dias)

    def eliminarSancion(self, correo_estudiante, tipo, fecha_inicio, duracion):
        return self._sanciones.eliminarSancion(correo_estudiante, tipo, fecha_inicio, duracion)

    def obtenerSancionesEstudiante(self, correo_estudiante):
        return self._sanciones.obtenerSancionesEstudiante(correo_estudiante)

    def tieneSancionActiva(self, correo_estudiante):
        return self._sanciones.tieneSancionActiva(correo_estudiante)

    def calcularDiasSancionActiva(self, correo_estudiante):
        return self._sanciones.calcularDiasSancionActiva(correo_estudiante)

    def calcularSemanasRetraso(self, fecha_devolucion):
        return self._sanciones.calcularSemanasRetraso(fecha_devolucion)

                                         
    def crearReserva(self, isbn, correo_estudiante):
        return self._reservas.crearReserva(isbn, correo_estudiante)

    def cancelarReserva(self, isbn):
        return self._reservas.cancelarReserva(isbn)

    def liberarReservaExpirada(self, isbn):
        return self._reservas.liberarReservaExpirada(isbn)

    def obtenerReservasEstudiante(self, correo_estudiante):
        return self._reservas.obtenerReservasEstudiante(correo_estudiante)

    def contarReservasEstudiante(self, correo_estudiante):
        return self._reservas.contarReservasEstudiante(correo_estudiante)

    def reservaExpirada(self, isbn):
        return self._reservas.reservaExpirada(isbn)

    def validarReserva(self, isbn, correo_estudiante):
        return self._reservas.validarReserva(isbn, correo_estudiante)

    def actualizarReservasEstudiante(self, correo_estudiante):
        return self._reservas.actualizarReservasEstudiante(correo_estudiante)

    def marcarReservaEspera(self, isbn):
        return self._reservas.marcarReservaEspera(isbn)

    def cumplirReservaEspera(self, isbn):
        return self._reservas.cumplirReservaEspera(isbn)

    def obtenerReservaEnEspera(self, isbn):
        return self._reservas.obtenerReservaEnEspera(isbn)

    def esperaExpirada(self, isbn):
        return self._reservas.esperaExpirada(isbn)

    def liberarEsperaExpirada(self, isbn):
        return self._reservas.liberarEsperaExpirada(isbn)

    def obtenerTodasReservas(self):
        return self._reservas.obtenerTodasReservas()

    def obtenerReservaPorLibro(self, isbn):
        return self._reservas.obtenerReservaPorLibro(isbn)

    def buscarReservasEstudiante(self, correo_estudiante, titulo='', tema='Ninguno'):
        return self._reservas.buscarReservasEstudiante(correo_estudiante, titulo, tema)

                                            
    def buscarEstudiante(self, correo):
        return self._estudiantes.buscarEstudiante(correo)

    def agregarTemaFavorito(self, correo, nombre_tema):
        return self._estudiantes.agregarTemaFavorito(correo, nombre_tema)

    def eliminarTemaFavorito(self, correo, nombre_tema):
        return self._estudiantes.eliminarTemaFavorito(correo, nombre_tema)

    def obtenerTemasFavoritos(self, correo):
        return self._estudiantes.obtenerTemasFavoritos(correo)

    def obtenerResumenEstudiante(self, correo):
        return self._estudiantes.obtenerResumenEstudiante(correo)

    def marcarReservaDisponible(self, isbn):
        return self._reservas.marcarReservaDisponible(isbn)

    # ── Copia de seguridad ──────────────────────────────────────────
    def realizarCopiaSeguridad(self) -> tuple[bool, str]:
        return self._copias.realizarCopiaSeguridad()
