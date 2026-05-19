from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5 import uic

Form, Window = uic.loadUiType("./src/vista/Ui/VistaBuscarEstudiante.ui")

class VistaBuscarEstudiante(QDialog, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._controlador = None
        
                             
        self.boton_buscar.clicked.connect(self.on_buscar_click)
        self.boton_volver.clicked.connect(self.on_volver_click)

    def on_buscar_click(self):
        correo = self.linea_busqueda.text().strip()
        if not correo:
            QMessageBox.warning(self, "Aviso", "Por favor, introduce un correo electrónico.")
            return
            
        if self._controlador:
            self._controlador.buscarEstudiante(correo)

    def on_volver_click(self):
        if self._controlador:
            self._controlador.volverDeBuscarEstudiante()

    @property
    def controlador(self):
        return self._controlador

    @controlador.setter
    def controlador(self, ref_controlador):
        self._controlador = ref_controlador