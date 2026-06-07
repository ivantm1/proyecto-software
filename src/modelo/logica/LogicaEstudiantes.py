from src.modelo.dao.BuscarEstudianteDaoJDBC import BuscarEstudianteDaoJDBC
from src.modelo.dao.TemaFavoritosDaoJDBC import TemaFavoritosDaoJDBC
from src.modelo.logica.LogicaPrestamos import LogicaPrestamos
from src.modelo.logica.LogicaReservas import LogicaReservas
from src.modelo.logica.LogicaSanciones import LogicaSanciones

class LogicaEstudiantes:
    """Búsqueda de estudiantes y gestión de temas favoritos."""

    def buscarEstudiante(self, correo):
        return BuscarEstudianteDaoJDBC().buscarEstudiante(correo)

    def obtenerResumenEstudiante(self, correo):
        estudiante = self.buscarEstudiante(correo)
        if estudiante is None:
            return None

        num_prestamos = LogicaPrestamos().contarPrestamosEstudiante(correo)
        num_reservas = LogicaReservas().contarReservasEstudiante(correo)
        sanciones = LogicaSanciones().obtenerSancionesEstudiante(correo)
        num_sanciones_activas = len([s for s in sanciones if s.estado in ("Activa", "Pendiente")])

        return estudiante, num_prestamos, num_reservas, num_sanciones_activas

    def agregarTemaFavorito(self, correo, nombre_tema):
        return TemaFavoritosDaoJDBC().agregarFavorito(correo, nombre_tema)

    def eliminarTemaFavorito(self, correo, nombre_tema):
        return TemaFavoritosDaoJDBC().eliminarFavorito(correo, nombre_tema)

    def obtenerTemasFavoritos(self, correo):
        return TemaFavoritosDaoJDBC().obtenerFavoritos(correo)
