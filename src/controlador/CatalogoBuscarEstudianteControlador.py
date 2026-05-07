from PyQt5.QtWidgets import QMessageBox
from src.vista.VistaGestionarEstudiante import VistaGestionarEstudiante
from src.vista.VistaSanciones import VistaSanciones
from src.vista.VistaMisPrestamos import VistaMisPrestamos
from src.controlador.CatalogoMisPrestamosControlador import CatalogoMisPrestamosControlador

class CatalogoBuscarEstudianteControlador:
    def __init__(self, ref_modelo, ref_vista_buscar, ref_vista_bibliotecario):
        self._modelo = ref_modelo
        self._vista_buscar = ref_vista_buscar
        self._vista_bibliotecario = ref_vista_bibliotecario
        self._vista_gestion = VistaGestionarEstudiante()
        self._vista_sanciones = VistaSanciones()
        self._vista_prestamos = VistaMisPrestamos()
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

        # Comprobar estado actual del libro
        libro = self._modelo.buscarPorISBN(isbn)
        if libro is None:
            QMessageBox.warning(self._vista_gestion, "Error", "No se encontró el libro con ese ISBN.")
            return

        if str(libro.disponibilidad).lower() == 'prestado':
            QMessageBox.warning(self._vista_gestion, "Error", "No es posible prestar el libro porque ya está prestado.")
            return
        elif str(libro.disponibilidad).lower() == 'reservado':
            QMessageBox.warning(self._vista_gestion, "Error", "No es posible prestar el libro porque está reservado.")
            return
        elif str(libro.disponibilidad).lower() != 'disponible':
            QMessageBox.warning(self._vista_gestion, "Error", "No es posible prestar el libro porque no está disponible.")
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
        self._vista_buscar.linea_busqueda.clear()
        self._vista_buscar.showMaximized()

    def verPrestamosEstudiante(self, correo_estudiante):
        ctrl = CatalogoMisPrestamosControlador(
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
        reservas = self._modelo.obtenerReservasEstudiante(correo_estudiante)
        if reservas:
            reservas_str = "\n".join([
                f"{r.isbn} - Estado: {r.estado} - Fecha: {r.fecha_reserva}"
                for r in reservas
            ])
            QMessageBox.information(self._vista_gestion, "Reservas del Estudiante", reservas_str)
        else:
            QMessageBox.information(self._vista_gestion, "Reservas del Estudiante", "No hay reservas activas para este estudiante.")

    def gestionarSanciones(self, correo_estudiante):
        """Abre la vista de sanciones para el estudiante"""
        sanciones = self._modelo.obtenerSancionesEstudiante(correo_estudiante)
        self._vista_sanciones.mostrarSanciones(sanciones)
        self._vista_sanciones.controlador = self
        self._vista_gestion.close()
        self._vista_sanciones.showMaximized()

    def volverASanciones(self):
        """Cierra la vista de sanciones y vuelve a la vista de gestión"""
        self._vista_sanciones.close()
        self._vista_gestion.showMaximized()
