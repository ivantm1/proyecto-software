from src.modelo.dao.ReservaDaoJDBC import ReservaDaoJDBC
from src.modelo.dao.LibroDaoJDBC import LibroDaoJDBC

class LogicaReservas:
                                                                                  

    def crearReserva(self, isbn, correo_estudiante):
        return ReservaDaoJDBC().crearReserva(isbn, correo_estudiante)

    def cancelarReserva(self, isbn):
        return ReservaDaoJDBC().cancelarReserva(isbn)

    def liberarReservaExpirada(self, isbn):
        ReservaDaoJDBC().cancelarReserva(isbn)
        return LibroDaoJDBC().restaurarLibro(isbn)

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
