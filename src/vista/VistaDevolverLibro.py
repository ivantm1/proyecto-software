from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5 import uic

Form, Window = uic.loadUiType("./src/vista/Ui/VistaDevolverLibro.ui")

class VistaDevolverLibro(QDialog, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Devolver libro — BiblioULE")
        self._controlador = None

        self.boton_devolver.clicked.connect(self.on_devolver_click)
        self.boton_volver.clicked.connect(self.on_volver_click)

    def on_devolver_click(self):
        isbn = self.lineEdit.text().strip()
        if not isbn:
            self.lanzarAviso("Introduce el ISBN del libro.")
            return
        if self._controlador:
            self._controlador.registrarDevolucion(isbn)

    def on_volver_click(self):
        if self._controlador:
            self._controlador.volver()

    def mostrarResultado(self, mensaje):
        self.label.setText(mensaje)

    def limpiarFormulario(self):
        self.lineEdit.clear()
        self.label.setText("")

    def lanzarAviso(self, aviso):
        QMessageBox.information(self, "Información", aviso)

    @property
    def controlador(self):
        return self._controlador

    @controlador.setter
    def controlador(self, ref_controlador):
        self._controlador = ref_controlador