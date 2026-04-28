from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QTableWidget, QTableWidgetItem,
                              QMessageBox)


class MisPrestamos(QDialog):
    """
    Vista para el Estudiante: muestra sus préstamos activos y permite
    solicitar prórroga de 7 días en el seleccionado.
    Sin fichero .ui — construida programáticamente (patrón de Prestamo.py).
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Mis préstamos — BiblioULE")
        self.setMinimumSize(800, 500)
        self._controlador = None
        self._construir_ui()

    

    # ------------------------------------------------------------------
    # Manejadores
    # ------------------------------------------------------------------

    def on_prorrogar_click(self):
        fila = self.tabla_prestamos.currentRow()
        if fila < 0:
            self.lanzarAviso("Selecciona un préstamo de la tabla.")
            return
        isbn = self.tabla_prestamos.item(fila, 0).text()
        if self._controlador:
            self._controlador.prorrogarPrestamo(isbn)

    def on_actualizar_click(self):
        if self._controlador:
            self._controlador.actualizarPrestamos()

    # ------------------------------------------------------------------
    # Métodos de visualización
    # ------------------------------------------------------------------

    def cargarPrestamos(self, modelo, correo_estudiante):
        """Llamado por el controlador principal al abrir la ventana."""
        from src.controlador.MisPrestamosControlador import MisPrestamosControlador
        ctrl = MisPrestamosControlador(modelo, self, correo_estudiante)
        self.controlador = ctrl
        ctrl.actualizarPrestamos()

    def mostrarPrestamos(self, lista_prestamos):
        self.tabla_prestamos.setRowCount(0)
        for p in lista_prestamos:
            fila = self.tabla_prestamos.rowCount()
            self.tabla_prestamos.insertRow(fila)
            self.tabla_prestamos.setItem(fila, 0, QTableWidgetItem(str(p.isbn_libro)))
            self.tabla_prestamos.setItem(fila, 1, QTableWidgetItem(str(p.fecha_prestamo)))
            self.tabla_prestamos.setItem(fila, 2, QTableWidgetItem(str(p.fecha_devolucion)))
            self.tabla_prestamos.setItem(fila, 3, QTableWidgetItem("—"))

    def lanzarAviso(self, aviso):
        QMessageBox.information(self, "Información", aviso)

    @property
    def controlador(self):
        return self._controlador

    @controlador.setter
    def controlador(self, ref_controlador):
        self._controlador = ref_controlador
