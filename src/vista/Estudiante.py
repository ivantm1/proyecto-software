from PyQt5.QtWidgets import QMainWindow, QMessageBox, QDialog
from PyQt5 import uic

Form, Window = uic.loadUiType("./src/vista/Ui/VistaEstudiante.ui")

class Estudiante(QDialog, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.controlador = None
        # Conectar el botón a la función
        self.boton_perfil.clicked.connect(self.on_ver_perfil_click)
        self.boton_catalogo.clicked.connect(self.on_ver_catalogo_click)
        self.boton_prestamos.clicked.connect(self.on_mis_prestamos_click)

    def on_ver_perfil_click(self):
        if self.controlador:
            self.controlador.ventanaVerPerfil()

    def on_ver_catalogo_click(self):
        if self.controlador:
            self.controlador.ventanaCatalogo()

    def on_mis_prestamos_click(self):
        if self.controlador:
            self.controlador.ventanaMisPrestamos()


    @property
    def controlador(self):
        return self._controlador

    @controlador.setter
    def controlador(self, ref_controlador):
        self._controlador = ref_controlador