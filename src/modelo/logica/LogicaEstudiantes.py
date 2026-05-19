from src.modelo.dao.BuscarEstudianteDaoJDBC import BuscarEstudianteDaoJDBC
from src.modelo.dao.TemaFavoritosDaoJDBC import TemaFavoritosDaoJDBC

class LogicaEstudiantes:
                                                                                

    def buscarEstudiante(self, correo):
        return BuscarEstudianteDaoJDBC().buscarEstudiante(correo)

    def agregarTemaFavorito(self, correo, nombre_tema):
        return TemaFavoritosDaoJDBC().agregarFavorito(correo, nombre_tema)

    def eliminarTemaFavorito(self, correo, nombre_tema):
        return TemaFavoritosDaoJDBC().eliminarFavorito(correo, nombre_tema)

    def obtenerTemasFavoritos(self, correo):
        return TemaFavoritosDaoJDBC().obtenerFavoritos(correo)
