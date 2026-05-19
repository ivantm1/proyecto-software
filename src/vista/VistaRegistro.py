from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog
from PyQt5 import uic

Form, Window = uic.loadUiType("./src/vista/Ui/VistaRegistro.ui")

class VistaRegistro(QDialog, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)                          
        self.controlador = None

        self.boton_registro.clicked.connect(self.on_register_click)
        self.boton_volver.clicked.connect(self.on_volver_click)

    
    def on_register_click(self):
        nombre = self.Linea_nombre.text()
        apellidos = self.Linea_apellidos.text()
        correo = self.Linea_correo.text()
        contrasena = self.Linea_contrasena.text()
        confirmar_contrasena = self.Linea_confirmar_contrasena.text()

        if self.controlador:
            self.controlador.registrarUsuario(nombre, apellidos, correo, contrasena, confirmar_contrasena)
        
    def on_volver_click(self):
        self.controlador.registroAtras()
    
    def lanzarAviso(self, aviso):
        QMessageBox.information(self, "Información", aviso)
    
    @property
    def controlador(self):
        return self._controlador
    
    @controlador.setter
    def controlador(self, ref_controlador):
        self._controlador = ref_controlador
