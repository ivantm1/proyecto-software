from src.modelo.dao.UserDaoJDBC import UserDaoJDBC
from src.modelo.dao.LibroDaoJDBC import LibroDaoJDBC
from src.modelo.dao.LibroDaoJDBC import LibroDaoJDBC
from src.modelo.dao.PrestamoDaoJDBC import PrestamoDaoJDBC
from src.modelo.dao.ReservaDaoJDBC import ReservaDaoJDBC
from src.modelo.dao.SancionDaoJDBC import SancionDaoJDBC

class Logica():
    def pruebaSelect(self):
        userDao = UserDaoJDBC()
        usuarios = userDao.select()
        for user in usuarios:
            print(user.nombre_user)

    def comprobarLogin(self, loginVO):                                               
        login_dao = UserDaoJDBC()                                                    
        return login_dao.comprobarLogin(loginVO)                                     
                                                                               
    def registrarUsuario(self, registroVO):                                          
        registro_dao = UserDaoJDBC()                                                 
        return registro_dao.registrarUsuario(registroVO) 
    
    def buscar_libros(self, linea_busqueda, tema):
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

    def bajaLibro(self, isbn):
        return LibroDaoJDBC().bajaLibro(isbn)

    def obtenerReservados(self):
        return LibroDaoJDBC().obtenerReservados()

    def buscarPorISBN(self, isbn):
        return LibroDaoJDBC().buscarPorISBN(isbn)
    
    def registrarPrestamo(self, isbn, correo_estudiante):
        return PrestamoDaoJDBC().registrarPrestamo(isbn, correo_estudiante)

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

    def aplicarSancionRetraso(self, correo_estudiante, semanas_retraso):
        return SancionDaoJDBC().aplicarSancionRetraso(correo_estudiante, semanas_retraso)

    def aplicarSancionDanio(self, correo_estudiante, semanas_sancion=3):
        return SancionDaoJDBC().aplicarSancionDanio(correo_estudiante, semanas_sancion)

    def obtenerSancionesEstudiante(self, correo_estudiante):
        return SancionDaoJDBC().obtenerSancionesEstudiante(correo_estudiante)

    def tieneSancionActiva(self, correo_estudiante):
        return SancionDaoJDBC().tieneSancionActiva(correo_estudiante)

    def crearReserva(self, isbn, correo_estudiante):
        return ReservaDaoJDBC().crearReserva(isbn, correo_estudiante)

    def cancelarReserva(self, isbn):
        return ReservaDaoJDBC().cancelarReserva(isbn)

    def obtenerReservasEstudiante(self, correo_estudiante):
        return ReservaDaoJDBC().obtenerReservasEstudiante(correo_estudiante)

    def contarReservasEstudiante(self, correo_estudiante):
        return ReservaDaoJDBC().contarReservasEstudiante(correo_estudiante)

    def reservaExpirada(self, isbn):
        return ReservaDaoJDBC().reservaExpirada(isbn)

    def obtenerReservaPorLibro(self, isbn):
        return ReservaDaoJDBC().obtenerReservaPorLibro(isbn)

