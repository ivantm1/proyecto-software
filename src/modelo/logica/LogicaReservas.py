from src.modelo.dao.ReservaDaoJDBC import ReservaDaoJDBC
from src.modelo.dao.LibroDaoJDBC import LibroDaoJDBC
from src.modelo.dao.SancionDaoJDBC import SancionDaoJDBC

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

    def validarReserva(self, isbn, correo_estudiante):
        """Valida si se puede hacer una reserva del libro."""
        if SancionDaoJDBC().tieneSancionActiva(correo_estudiante):
            return False, "Tienes una sanción activa y no puedes realizar reservas."
        
        from src.modelo.logica.LogicaPrestamos import LogicaPrestamos
        prestamos_logica = LogicaPrestamos()
        

        num_reservas = self.contarReservasEstudiante(correo_estudiante)
        if num_reservas >= 3:
            return False, "Ya tienes 3 reservas activas. No puedes tener más de 3 a la vez."
        
        if prestamos_logica.tienePrestamoActivo(isbn, correo_estudiante):
            return False, "No puedes reservar un libro que ya tienes prestado."
        
        return True, ""

    def actualizarReservasEstudiante(self, correo_estudiante):
        """Obtiene reservas del estudiante y libera las expiradas automáticamente."""
        reservas = self.obtenerReservasEstudiante(correo_estudiante)
        for reserva in reservas:
            if self.reservaExpirada(reserva.isbn_libro):
                self.liberarReservaExpirada(reserva.isbn_libro)
        return self.obtenerReservasEstudiante(correo_estudiante)

    def marcarReservaDisponible(self, isbn):
        return ReservaDaoJDBC().marcarReservaDisponible(isbn)
