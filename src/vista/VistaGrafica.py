from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5 import uic

Form, Window = uic.loadUiType("./src/vista/Ui/VistaGrafica.ui")


class VistaGrafica(QDialog, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Gráfica — BiblioULE")

    def on_volver_click(self):
        if self._controlador:
            self._controlador.volver()

    @property
    def controlador(self):
        return self._controlador

    @controlador.setter
    def controlador(self, ref_controlador):
        self._controlador = ref_controlador
