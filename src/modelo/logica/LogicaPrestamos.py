from src.modelo.dao.PrestamoDaoJDBC import PrestamoDaoJDBC
from src.modelo.dao.LibroDaoJDBC import LibroDaoJDBC
from src.modelo.dao.ReservaDaoJDBC import ReservaDaoJDBC
from src.modelo.dao.SancionDaoJDBC import SancionDaoJDBC
from src.modelo.dao.BuscarEstudianteDaoJDBC import BuscarEstudianteDaoJDBC

class LogicaPrestamos:
    """Consultas de préstamos y gestión de devoluciones ."""

    MAX_PRESTAMOS_ACTIVOS = 7

    def registrarPrestamo(self, isbn, correo_estudiante):
        resultado = PrestamoDaoJDBC().registrarPrestamo(isbn, correo_estudiante)
        if resultado:
            reserva_espera = ReservaDaoJDBC().obtenerReservaEnEspera(isbn)
            if reserva_espera and reserva_espera.correo_estudiante == correo_estudiante:
                ReservaDaoJDBC().cumplirReservaEspera(isbn)
        return resultado

    def registrarDevolucion(self, isbn):
        return PrestamoDaoJDBC().registrarDevolucion(isbn)

    def buscarPrestamoActivoPorISBN(self, isbn):
        return PrestamoDaoJDBC().buscarPrestamoActivoPorISBN(isbn)

    def tieneCooldown(self, correo_estudiante, isbn):
        return PrestamoDaoJDBC().tieneCooldown(correo_estudiante, isbn)

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

    def tienePrestamoActivo(self, isbn, correo_estudiante):
        return PrestamoDaoJDBC().tienePrestamoActivo(isbn, correo_estudiante)

    def validarPrestamo(self, isbn, correo_estudiante):
        if SancionDaoJDBC().tieneSancionActiva(correo_estudiante):
            return False, "Este estudiante tiene una sanción activa y no puede realizar préstamos."

        if self.contarPrestamosEstudiante(correo_estudiante) >= self.MAX_PRESTAMOS_ACTIVOS:
            return False, f"Este estudiante ya tiene {self.MAX_PRESTAMOS_ACTIVOS} préstamos activos. No puede tener más de {self.MAX_PRESTAMOS_ACTIVOS} a la vez."

        if self.tieneCooldown(correo_estudiante, isbn):
            return False, "Este estudiante devolvió este libro hace menos de 7 días. Debe esperar antes de volver a pedirlo."

        libro = LibroDaoJDBC().buscarPorISBN(isbn)
        if libro is None:
            return False, "No se encontró el libro con ese ISBN."

        disponibilidad = str(libro.disponibilidad).lower()
        if disponibilidad == 'prestado':
            return False, "No es posible prestar el libro porque ya está prestado."

        if disponibilidad == 'reservado':
            #Si el libro está reservado solo puede tomarlo prestado el estudiante que lo tenía reservado
            reserva_espera = ReservaDaoJDBC().obtenerReservaEnEspera(isbn)
            if reserva_espera:
                if reserva_espera.correo_estudiante != correo_estudiante:
                    return False, (
                        f"Este libro está reservado para el alumno {reserva_espera.correo_estudiante}. "
                        "Solo ese alumno puede recogerlo."
                    )
                
            else:
                if ReservaDaoJDBC().reservaExpirada(isbn):
                    ReservaDaoJDBC().cancelarReserva(isbn)
                    LibroDaoJDBC().restaurarLibro(isbn)
                else:
                    return False, "No es posible prestar el libro porque está reservado."
        elif disponibilidad != 'disponible':
            return False, "No es posible prestar el libro porque no está disponible."

        return True, ""

    def obtenerNombreEstudiantePrestamo(self, isbn):
        """Obtiene el nombre completo del estudiante que tiene el libro prestado."""
        prestamo = self.buscarPrestamoActivoPorISBN(isbn)
        if prestamo is None:
            return None
        
        estudiante_vo = BuscarEstudianteDaoJDBC().buscarEstudiante(prestamo.correo_estudiante)
        if estudiante_vo:
            return f"{estudiante_vo.nombre} {estudiante_vo.apellidos}"
        return None
