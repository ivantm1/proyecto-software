from src.modelo.logica.LoggerSingleton import Logger

class ControladorPrestamo:
    def __init__(self, ref_vista):
        self._vista = ref_vista

    def registrarPrestamo(self, id_usuario, isbn, ref_modelo):
        if not id_usuario or not isbn:
            self._vista.lanzarAviso("Por favor, introduce el ID de usuario y el ISBN.")
            return

        try:
            id_usuario = int(id_usuario)
        except ValueError:
            self._vista.lanzarAviso("El ID de usuario debe ser un número.")
            return

        valido, mensaje = ref_modelo.validarPrestamo(isbn, str(id_usuario))
        if not valido:
            Logger().prestamo_error(isbn, str(id_usuario), mensaje)
            self._vista.lanzarAviso(mensaje)
            return

        resultado = ref_modelo.registrarPrestamo(isbn, str(id_usuario))
        if resultado:
            Logger().prestamo_ok(isbn, str(id_usuario), resultado.fecha_devolucion)
            self._vista.lanzarAviso(f"Préstamo registrado con éxito. Fecha de devolución: {resultado.fecha_devolucion}")
        else:
            Logger().prestamo_error(isbn, str(id_usuario), "Error en BD")
            self._vista.lanzarAviso("Error al registrar el préstamo.")
