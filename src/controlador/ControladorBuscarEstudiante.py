from PyQt5.QtWidgets import QMessageBox
from src.modelo.logica.LoggerSingleton import Logger
from src.vista.VistaGestionarEstudiante import VistaGestionarEstudiante
from src.vista.VistaSanciones import VistaSanciones
from src.vista.VistaMisPrestamos import VistaMisPrestamos
from src.vista.VistaMisReservas import VistaMisReservas
from src.controlador.ControladorMisPrestamos import ControladorMisPrestamos
from src.controlador.ControladorMisReservas import ControladorMisReservas
from src.controlador.ControladorSanciones import ControladorSanciones

class ControladorBuscarEstudiante:
    def __init__(self, ref_modelo, ref_vista_buscar, ref_vista_bibliotecario):
        self._modelo = ref_modelo
        self._vista_buscar = ref_vista_buscar
        self._vista_bibliotecario = ref_vista_bibliotecario
        self._vista_gestion = VistaGestionarEstudiante()
        self._vista_sanciones = VistaSanciones()
        self._vista_prestamos = VistaMisPrestamos()
        self._vista_reservas = VistaMisReservas()
        self._estudiante_actual = None

    def buscarEstudiante(self, correo):
        if not correo:
            QMessageBox.warning(self._vista_buscar, "Aviso", "Por favor, introduce un correo electrónico.")
            return

        resumen = self._modelo.obtenerResumenEstudiante(correo)
        if resumen is None:
            QMessageBox.warning(self._vista_buscar, "No encontrado", 
                                "No se encontró un estudiante con ese correo.")
            return

        estudiante, num_prestamos, num_reservas, num_sanciones_activas = resumen
        self._estudiante_actual = estudiante
        self._vista_gestion.cargar_datos(estudiante, num_prestamos, num_reservas, num_sanciones_activas)
        self._vista_gestion.controlador = self
        
        self._vista_buscar.close()
        self._vista_gestion.showMaximized()

    def volverDeBuscarEstudiante(self):
        if self._vista_buscar:
            self._vista_buscar.close()
        if self._vista_bibliotecario:
            self._vista_bibliotecario.showMaximized()

    def hacerPrestamoDesdeGestion(self, isbn, correo_estudiante):
        if not isbn:
            QMessageBox.warning(self._vista_gestion, "Aviso", "Por favor, introduce un ISBN válido.")
            return

        valido, mensaje = self._modelo.validarPrestamo(isbn, correo_estudiante)
        if not valido:
            QMessageBox.warning(self._vista_gestion, "Aviso", mensaje)
            return

        exito = self._modelo.registrarPrestamo(isbn, correo_estudiante)
        if exito:
            Logger().prestamo_ok(isbn, correo_estudiante, exito.fecha_devolucion)
            QMessageBox.information(self._vista_gestion, "Éxito", "Préstamo registrado correctamente.")
            self.buscarEstudiante(correo_estudiante)
        else:
            Logger().prestamo_error(isbn, correo_estudiante, "Error en BD")
            QMessageBox.warning(self._vista_gestion, "Error", 
                                "No se pudo registrar el préstamo.")

    def volverGestionarEstudiante(self):
        self._vista_gestion.close()
        self._vista_buscar.linea_busqueda.clear()
        self._vista_buscar.showMaximized()

    def verPrestamosEstudiante(self, correo_estudiante):
        ctrl = ControladorMisPrestamos(
            self._modelo,
            self._vista_prestamos,
            self._vista_gestion,
            self._vista_gestion,
            correo_estudiante,
            "Bibliotecario"
        )
        self._vista_prestamos.controlador = ctrl
        ctrl.actualizarPrestamos()
        self._vista_gestion.close()
        self._vista_prestamos.showMaximized()
        
    def verReservasEstudiante(self, correo_estudiante):
        ctrl = ControladorMisReservas(
            self._modelo,
            self._vista_reservas,
            self._vista_gestion,
            correo_estudiante,
            "Bibliotecario"
        )
        self._vista_reservas.controlador = ctrl
        ctrl.actualizarReservas()
        self._vista_gestion.close()
        self._vista_reservas.showMaximized()

    def gestionarSanciones(self, correo_estudiante):
        sanciones = self._modelo.obtenerSancionesEstudiante(correo_estudiante)
        ctrl_sanciones = ControladorSanciones(self._modelo, self._vista_sanciones, self._vista_gestion)
        ctrl_sanciones._estudiante_actual = self._estudiante_actual
        self._vista_sanciones.controlador = ctrl_sanciones
        self._vista_sanciones.mostrarSanciones(sanciones)
        self._vista_gestion.close()
        self._vista_sanciones.showMaximized()

    def volverASanciones(self):
        self._vista_sanciones.close()
        if self._estudiante_actual is not None:
            resumen = self._modelo.obtenerResumenEstudiante(self._estudiante_actual.correo)
            if resumen is not None:
                estudiante, num_prestamos, num_reservas, num_sanciones_activas = resumen
                self._vista_gestion.cargar_datos(estudiante, num_prestamos, num_reservas, num_sanciones_activas)
        self._vista_gestion.showMaximized()
