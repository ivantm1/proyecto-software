from src.modelo.dao.UserDaoJDBC import UserDaoJDBC
from src.modelo.logica.LogicaInicioSesion import LogicaInicioSesion
from src.modelo.logica.LogicaLibros import LogicaLibros
from src.modelo.logica.LogicaPrestamos import LogicaPrestamos
from src.modelo.logica.LogicaReservas import LogicaReservas
from src.modelo.logica.LogicaSanciones import LogicaSanciones
from src.modelo.logica.LogicaEstudiantes import LogicaEstudiantes

class Logica:
    def __init__(self):
        self._sesion = LogicaInicioSesion()
        self._libros = LogicaLibros()
        self._prestamos = LogicaPrestamos()
        self._reservas = LogicaReservas()
        self._sanciones = LogicaSanciones()
        self._estudiantes = LogicaEstudiantes()

    def pruebaSelect(self):
        userDao = UserDaoJDBC()
        usuarios = userDao.select()
        for user in usuarios:
            pass                             

                                             
    def comprobarLogin(self, loginVO):
        return self._sesion.comprobarLogin(loginVO)

    def registrarUsuario(self, registroVO):
        return self._sesion.registrarUsuario(registroVO)

    def cambiarContrasena(self, correo, nueva_contrasena):
        return self._sesion.cambiarContrasena(correo, nueva_contrasena)

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

    def buscarPorTitulo(self, titulo):
        return self._libros.buscarPorTitulo(titulo)

    def buscarPorTema(self, tema):
        return self._libros.buscarPorTema(tema)

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
