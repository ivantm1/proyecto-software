from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import uic

Form, Window = uic.loadUiType("./src/vista/Ui/VistaEstudiante.ui")

class MiVentana(QMainWindow, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Inicializa los widgets
        self.controlador = None
        # Conectar el botón a la función
        self.boton_registro.clicked.connect(self.on_register_click)
        self.boton_registro.clicked.connect(self.on_register_click)
        self.boton_registro.clicked.connect(self.on_register_click)


    
    def on_register_click(self):
        nombre = self.Linea_nombre.text()
        apellidos = self.Linea_apellidos.text()
        correo = self.Linea_correo.text()
        contrasena = self.Linea_contrasena.text()
        confirmar_contrasena = self.Linea_confirmar_contrasena.text()
    
    def lanzarAviso(self, aviso):
        QMessageBox.information(self, "Información", aviso)
    
    @property
    def controlador(self):
        return self._controlador
    
    @controlador.setter
    def controlador(self, ref_controlador):
        self._controlador = ref_controlador