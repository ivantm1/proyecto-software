from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import uic
from src.modelo.vo.RegistroVO import RegistroVO

# Cargar la interfaz generada desde el archivo .ui
Form, Window = uic.loadUiType("./src/vista/Ui/VistaRegistro.ui")

class MiVentana(QMainWindow, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Inicializa los widgets
        self.controlador = None
        # Conectar el botón a la función
        self.boton_registro.clicked.connect(self.on_register_click)
    
    def on_register_click(self):
        if self.controlador:
            self.controlador.ventanaRegistro()
    
    def lanzarAviso(self, aviso):
        QMessageBox.information(self, "Información", aviso)
    
    @property
    def controlador(self):
        return self._controlador
    
    @controlador.setter
    def controlador(self, ref_controlador):
        self._controlador = ref_controlador