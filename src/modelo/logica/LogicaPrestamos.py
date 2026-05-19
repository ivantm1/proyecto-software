from src.modelo.dao.PrestamoDaoJDBC import PrestamoDaoJDBC

class LogicaPrestamos:
                                                                  

    def registrarPrestamo(self, isbn, correo_estudiante):
        return PrestamoDaoJDBC().registrarPrestamo(isbn, correo_estudiante)

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
