from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import uic

Form, Window = uic.loadUiType("./src/vista/Ui/VistaEstudiante.ui")

class Estudiante(QMainWindow, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.controlador = None

    def lanzarAviso(self, aviso):
        QMessageBox.information(self, "Información", aviso)

    @property
    def controlador(self):
        return self._controlador

    @controlador.setter
    def controlador(self, ref_controlador):
        self._controlador = ref_controlador