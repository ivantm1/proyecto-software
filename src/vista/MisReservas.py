from PyQt5.QtWidgets import QDialog, QMessageBox, QTableWidgetItem
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import QHeaderView, QSizePolicy, QAbstractItemView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

Form, Window = uic.loadUiType("./src/vista/Ui/VistaMisReservas.ui")

class MisReservas(QDialog, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Mis reservas — BiblioULE")
        self.controlador = None

        self.boton_buscar.clicked.connect(self.on_buscar_click)
        self.boton_volver.clicked.connect(self.on_volver_click)

        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.tableWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
    def on_buscar_click(self):
        if self.controlador:
            titulo = self.linea_busqueda.text()
            tema   = self.opcion_buscador.currentText()
            self.controlador.buscarReservas(titulo, tema)


    def on_volver_click(self):
        self.controlador.registroAtras()

    def mostrarReservas(self, lista_reservas):
        self.tabla_libros.setRowCount(0)
        
        self.tabla_libros.resizeColumnsToContents()

        self._reservas = lista_reservas  # guardamos para acceder por índice

        if not lista_reservas:
            return

        for reserva in lista_reservas:
            fila = self.tabla_libros.rowCount()
            self.tabla_libros.insertRow(fila)
            self.tabla_libros.setItem(fila, 0, QTableWidgetItem(str(reserva.titulo)))
            self.tabla_libros.setItem(fila, 1, QTableWidgetItem(str(reserva.autor)))
            self.tabla_libros.setItem(fila, 2, QTableWidgetItem(str(reserva.nombre_tema)))
            self.tabla_libros.setItem(fila, 3, QTableWidgetItem(str(reserva.estado)))
        self.tabla_libros.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def obtenerReservaPorFila(self, fila):
        if hasattr(self, '_reservas') and 0 <= fila < len(self._reservas):
            return self._reservas[fila]
        return None

    def lanzarAviso(self, aviso):
        QMessageBox.information(self, "Información", aviso)

    @property
    def controlador(self):
        return self._controlador

    @controlador.setter
    def controlador(self, ref_controlador):
        self._controlador = ref_controlador