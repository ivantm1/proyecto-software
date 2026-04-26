import datetime
from src.modelo.dao.PrestamoDaoJDBC import PrestamoDaoJDBC

LIMITE_PRESTAMOS = 3

class PrestamoControlador:
    def __init__(self, ref_vista):
        self._vista = ref_vista

    def registrarPrestamo(self, id_usuario, isbn):
        if not id_usuario or not isbn:
            self._vista.lanzarAviso("Por favor, introduce el ID de usuario y el ISBN.")
            return

        try:
            id_usuario = int(id_usuario)
        except ValueError:
            self._vista.lanzarAviso("El ID de usuario debe ser un número.")
            return

        dao = PrestamoDaoJDBC()

        if dao.tieneSancionActiva(id_usuario):
            self._vista.lanzarAviso("El usuario tiene una sanción activa y no puede solicitar préstamos.")
            return

        if dao.contarPrestamosActivos(id_usuario) >= LIMITE_PRESTAMOS:
            self._vista.lanzarAviso(f"El usuario ha alcanzado el límite de {LIMITE_PRESTAMOS} préstamos activos.")
            return

        if not dao.libroDisponible(isbn):
            self._vista.lanzarAviso("El libro no está disponible para préstamo.")
            return

        resultado = dao.registrarPrestamo(id_usuario, isbn)
        if resultado:
            self._vista.lanzarAviso(f"Préstamo registrado con éxito. Fecha de devolución: {resultado.fecha_devolucion}")
            self.cargarPrestamosUsuario(str(id_usuario))
        else:
            self._vista.lanzarAviso("Error al registrar el préstamo.")

    def devolverPrestamo(self, id_prestamo, isbn):
        try:
            id_prestamo = int(id_prestamo)
        except ValueError:
            self._vista.lanzarAviso("ID de préstamo inválido.")
            return

        dao = PrestamoDaoJDBC()
        prestamo = dao.obtenerPorId(id_prestamo)
        if prestamo is None:
            self._vista.lanzarAviso("No se encontró el préstamo.")
            return

        exito = dao.registrarDevolucion(id_prestamo, isbn)
        if not exito:
            self._vista.lanzarAviso("Error al registrar la devolución.")
            return

        hoy = datetime.date.today()
        if hoy > prestamo.fecha_devolucion:
            dias_retraso = (hoy - prestamo.fecha_devolucion).days
            semanas_retraso = max(1, (dias_retraso + 6) // 7)
            dao.aplicarSancionRetraso(prestamo.id_usuario, semanas_retraso)
            self._vista.lanzarAviso(
                f"Devolución registrada con {dias_retraso} día(s) de retraso. Se ha aplicado una sanción."
            )
        else:
            self._vista.lanzarAviso("Devolución registrada correctamente.")

        self.cargarPrestamosUsuario(str(prestamo.id_usuario))

    def cargarPrestamosUsuario(self, id_usuario):
        try:
            id_usuario = int(id_usuario)
        except ValueError:
            self._vista.lanzarAviso("El ID de usuario debe ser un número.")
            return

        dao = PrestamoDaoJDBC()
        prestamos = dao.obtenerPrestamosActivos(id_usuario)
        self._vista.mostrarPrestamos(prestamos)
