from PyQt5.QtWidgets import QDialog, QMessageBox, QTableWidgetItem
from PyQt5 import uic
from PyQt5.QtWidgets import QHeaderView, QSizePolicy, QAbstractItemView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

Form, Window = uic.loadUiType("./src/vista/Ui/VistaMisPrestamos.ui")

class MisPrestamos(QDialog, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Mis préstamos — BiblioULE")
        self.controlador = None

        self.boton_buscar.clicked.connect(self.on_buscar_click)
        self.tabla_libros.cellDoubleClicked.connect(self.on_fila_doble_click)
        self.boton_volver.clicked.connect(self.on_volver_click)

    def on_buscar_click(self):
        if self.controlador:
            titulo = self.linea_busqueda.text()
            tema   = self.opcion_buscador.currentText()
            self.controlador.buscarPrestamos(titulo, tema)

    def on_fila_doble_click(self, fila, columna):
        """Al hacer doble clic en una fila, abre el detalle del préstamo"""
        if self.controlador:
            self.controlador.abrirDetallePrestamo(fila)

    def on_volver_click(self):
        self.controlador.registroAtras()

    def mostrarPrestamos(self, lista_prestamos):
        self.tabla_libros.setRowCount(0)
        self.tabla_libros.resizeColumnsToContents()

        self._prestamos = lista_prestamos  # guardamos para acceder por índice

        if not lista_prestamos:
            return

        for prestamo in lista_prestamos:
            fila = self.tabla_libros.rowCount()
            self.tabla_libros.insertRow(fila)
            self.tabla_libros.setItem(fila, 0, QTableWidgetItem(str(prestamo.titulo)))
            self.tabla_libros.setItem(fila, 1, QTableWidgetItem(str(prestamo.autor)))
            self.tabla_libros.setItem(fila, 2, QTableWidgetItem(str(prestamo.nombre_tema)))
            self.tabla_libros.setItem(fila, 3, QTableWidgetItem(str(prestamo.fecha_devolucion)))
        self.tabla_libros.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def obtenerPrestamoPorFila(self, fila):
        if hasattr(self, '_prestamos') and 0 <= fila < len(self._prestamos):
            return self._prestamos[fila]
        return None

    def lanzarAviso(self, aviso):
        QMessageBox.information(self, "Información", aviso)

    @property
    def controlador(self):
        return self._controlador

    @controlador.setter
    def controlador(self, ref_controlador):
        self._controlador = ref_controlador