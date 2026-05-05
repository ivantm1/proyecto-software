from PyQt5.QtWidgets import QMessageBox
from src.vista.VistaGestionarEstudiante import VistaGestionarEstudiante

class ControladorBuscarEstudiante:
    def __init__(self, ref_modelo, ref_vista_buscar, ref_vista_bibliotecario):
        self._modelo = ref_modelo
        self._vista_buscar = ref_vista_buscar
        self._vista_bibliotecario = ref_vista_bibliotecario
        self._vista_gestion = VistaGestionarEstudiante()
        self._estudiante_actual = None

    def buscarEstudiante(self, correo):
        """Busca un estudiante por correo y abre la vista de gestión"""
        if not correo:
            QMessageBox.warning(self._vista_buscar, "Aviso", "Por favor, introduce un correo electrónico.")
            return

        estudiante = self._modelo.buscarEstudiante(correo)
        
        if estudiante is None:
            QMessageBox.warning(self._vista_buscar, "No encontrado", 
                              f"No se encontró un estudiante con el correo: {correo}")
            return

        # Guardar estudiante actual y cargar datos en la vista
        self._estudiante_actual = estudiante
        
        # Obtener información adicional del estudiante
        num_prestamos = self._modelo.contarPrestamosEstudiante(correo)
        num_reservas = self._modelo.contarReservasEstudiante(correo)
        num_sanciones = len(self._modelo.obtenerSancionesEstudiante(correo))
        
        # Cargar datos en la vista de gestión
        self._vista_gestion.cargar_datos(estudiante, num_prestamos, num_reservas, num_sanciones)
        self._vista_gestion.controlador = self
        
        # Mostrar la vista de gestión
        self._vista_buscar.close()
        self._vista_gestion.showMaximized()

    def volverDeBuscarEstudiante(self):
        """Cierra la vista de búsqueda y vuelve a la vista del bibliotecario"""
        if self._vista_buscar:
            self._vista_buscar.close()
        if self._vista_bibliotecario:
            self._vista_bibliotecario.showMaximized()

    def hacerPrestamoDesdeGestion(self, isbn, correo_estudiante):
        """Realiza un préstamo para el estudiante desde la vista de gestión"""
        if not isbn:
            QMessageBox.warning(self._vista_gestion, "Aviso", "Por favor, introduce un ISBN válido.")
            return

        # Verificar si el estudiante tiene sanciones activas
        if self._modelo.tieneSancionActiva(correo_estudiante):
            QMessageBox.warning(self._vista_gestion, "Aviso", 
                              "Este estudiante tiene una sanción activa y no puede realizar préstamos.")
            return

        # Realizar el préstamo
        exito = self._modelo.registrarPrestamo(isbn, correo_estudiante)
        
        if exito:
            QMessageBox.information(self._vista_gestion, "Éxito", "Préstamo registrado correctamente.")
            # Actualizar datos
            self.buscarEstudiante(correo_estudiante)
        else:
            QMessageBox.warning(self._vista_gestion, "Error", 
                              "No se pudo registrar el préstamo. El libro puede no estar disponible.")

    def volverGestionarEstudiante(self):
        """Cierra la vista de gestión y vuelve a la vista de búsqueda"""
        self._vista_gestion.close()
        self._vista_buscar.showMaximized()

    def verPrestamosEstudiante(self, correo_estudiante):
        prestamos = self._modelo.obtenerPrestamosEstudiante(correo_estudiante)
        if prestamos:
            prestamos_str = "\n".join([
                f"{p.titulo} (ISBN: {p.isbn_libro}) - {'Activo' if p.estado == 'Activo' else 'Devuelto'}"
                for p in prestamos
            ])
            QMessageBox.information(self._vista_gestion, "Préstamos del Estudiante", prestamos_str)
        else:
            QMessageBox.information(self._vista_gestion, "Préstamos del Estudiante", "No hay préstamos activos para este estudiante.")
