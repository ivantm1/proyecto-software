from src.modelo.dao.UserDaoJDBC import UserDaoJDBC
from src.modelo.dao.LibroDaoJDBC import LibroDaoJDBC
from src.modelo.dao.PrestamoDaoJDBC import PrestamoDaoJDBC
from src.modelo.dao.ReservaDaoJDBC import ReservaDaoJDBC
from src.modelo.dao.SancionDaoJDBC import SancionDaoJDBC
from src.modelo.dao.BuscarEstudianteDaoJDBC import BuscarEstudianteDaoJDBC
from src.modelo.dao.TemaFavoritosDaoJDBC import TemaFavoritosDaoJDBC

class Logica():
    def pruebaSelect(self):
        userDao = UserDaoJDBC()
        usuarios = userDao.select()
        for user in usuarios:
            pass  # Método de prueba obsoleto

    def comprobarLogin(self, loginVO):                                               
        login_dao = UserDaoJDBC()                                                    
        return login_dao.comprobarLogin(loginVO)                                     
                                                                               
    def registrarUsuario(self, registroVO):                                          
        registro_dao = UserDaoJDBC()                                                 
        return registro_dao.registrarUsuario(registroVO) 
    
    def buscarLibro(self, linea_busqueda, tema):
        libros_dao = LibroDaoJDBC()
        lista = libros_dao.buscarLibros(linea_busqueda, tema)
        if len(lista)==0:
            return None
        else:
            return lista

    def obtenerCatalogo(self):
        return LibroDaoJDBC().obtenerCatalogo()

    def buscarPorTitulo(self, titulo):
        return LibroDaoJDBC().buscarPorTitulo(titulo)

    def buscarPorTema(self, tema):
        return LibroDaoJDBC().buscarPorTema(tema)

    def altaLibro(self, libroVO):
        return LibroDaoJDBC().altaLibro(libroVO)

    def bajaLibro(self, isbn, motivo="Retirado por el bibliotecario"):
        return LibroDaoJDBC().bajaLibro(isbn, motivo)
    
    def restaurarLibro(self, isbn):
        return LibroDaoJDBC().restaurarLibro(isbn)

    def obtenerReservados(self):
        return LibroDaoJDBC().obtenerReservados()

    def buscarPorISBN(self, isbn):
        return LibroDaoJDBC().buscarPorISBN(isbn)

    def buscarRetiradoPorISBN(self, isbn):
        return LibroDaoJDBC().buscarRetiradoPorISBN(isbn)

    def buscarPrestamoActivoPorISBN(self, isbn):
        return PrestamoDaoJDBC().buscarPrestamoActivoPorISBN(isbn)
    
    def registrarPrestamo(self, isbn, correo_estudiante):
        return PrestamoDaoJDBC().registrarPrestamo(isbn, correo_estudiante)

    def tieneCooldown(self, correo_estudiante, isbn):
        return PrestamoDaoJDBC().tieneCooldown(correo_estudiante, isbn)

    def registrarDevolucion(self, isbn):
        return PrestamoDaoJDBC().registrarDevolucion(isbn)

    def obtenerPrestamosEstudiante(self, correo_estudiante):
        return PrestamoDaoJDBC().obtenerPrestamosEstudiante(correo_estudiante)

    def obtenerPrestamosProximos(self, correo_estudiante):
        return PrestamoDaoJDBC().obtenerPrestamosProximos(correo_estudiante)

    def prorrogarPrestamo(self, isbn):
        return PrestamoDaoJDBC().prorrogarPrestamo(isbn)

    def contarPrestamosEstudiante(self, correo_estudiante):
        return PrestamoDaoJDBC().contarPrestamosEstudiante(correo_estudiante)
    
    def buscarPrestamosEstudiante(self, correo_estudiante, titulo='', tema='Ninguno'):
        return PrestamoDaoJDBC().buscarPrestamosEstudiante(correo_estudiante, titulo, tema)

    def aplicarSancionRetraso(self, correo_estudiante, semanas_retraso):
        return SancionDaoJDBC().aplicarSancionRetraso(correo_estudiante, semanas_retraso)

    def aplicarSancionDanio(self, correo_estudiante, estado_libro):
        if estado_libro == "Dañado":
            return SancionDaoJDBC().aplicarSancionDanio(correo_estudiante, "Dañado", 10)
        elif estado_libro == "Roto":
            return SancionDaoJDBC().aplicarSancionDanio(correo_estudiante, "Roto", 30)

    def aplicarSancionManual(self, correo_estudiante, motivo, dias):
        return SancionDaoJDBC().aplicarSancionDanio(correo_estudiante, motivo, dias)

    def eliminarSancion(self, correo_estudiante, tipo, fecha_inicio, duracion):
        return SancionDaoJDBC().eliminarSancion(correo_estudiante, tipo, fecha_inicio, duracion)

    def obtenerSancionesEstudiante(self, correo_estudiante):
        return SancionDaoJDBC().obtenerSancionesEstudiante(correo_estudiante)

    def tieneSancionActiva(self, correo_estudiante):
        return SancionDaoJDBC().tieneSancionActiva(correo_estudiante)

    def crearReserva(self, isbn, correo_estudiante):
        return ReservaDaoJDBC().crearReserva(isbn, correo_estudiante)

    def tienePrestamoActivo(self, isbn, correo_estudiante):
        return PrestamoDaoJDBC().tienePrestamoActivo(isbn, correo_estudiante)

    def cancelarReserva(self, isbn):
        return ReservaDaoJDBC().cancelarReserva(isbn)
    
    def liberarReservaExpirada(self, isbn):
        ReservaDaoJDBC().cancelarReserva(isbn)
        LibroDaoJDBC().restaurarLibro(isbn)

    def obtenerReservasEstudiante(self, correo_estudiante):
        return ReservaDaoJDBC().obtenerReservasEstudiante(correo_estudiante)

    def contarReservasEstudiante(self, correo_estudiante):
        return ReservaDaoJDBC().contarReservasEstudiante(correo_estudiante)

    def reservaExpirada(self, isbn):
        return ReservaDaoJDBC().reservaExpirada(isbn)

    def obtenerReservaPorLibro(self, isbn):
        return ReservaDaoJDBC().obtenerReservaPorLibro(isbn)
    
    def buscarReservasEstudiante(self, correo_estudiante, titulo='', tema='Ninguno'):
        return ReservaDaoJDBC().buscarReservasEstudiante(correo_estudiante, titulo, tema)
    
    def cambiarContrasena(self, correo, nueva_contrasena):
        return UserDaoJDBC().cambiarContrasena(correo, nueva_contrasena)

    def eliminarUsuario(self, correo):
        return UserDaoJDBC().eliminarUsuario(correo)
    
    def buscarEstudiante(self, correo):
        return BuscarEstudianteDaoJDBC().buscarEstudiante(correo)
    
    def agregarTemaFavorito(self, correo, nombre_tema):
        return TemaFavoritosDaoJDBC().agregarFavorito(correo, nombre_tema)

    def eliminarTemaFavorito(self, correo, nombre_tema):
        return TemaFavoritosDaoJDBC().eliminarFavorito(correo, nombre_tema)

    def obtenerTemasFavoritos(self, correo):
        return TemaFavoritosDaoJDBC().obtenerFavoritos(correo)