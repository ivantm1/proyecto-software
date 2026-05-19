from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog
from PyQt5 import uic
from src.modelo.vo.LoginVO import LoginVO

                                                  
Form, Window = uic.loadUiType("./src/vista/Ui/VistaLogin.ui")

class VistaLogin(QDialog, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)                          
        self.controlador = None
                                        
        self.boton_inicio_sesion.clicked.connect(self.on_login_click)
        self.boton_registro.clicked.connect(self.on_register_click)
                                                        
        self.Linea_usuario.returnPressed.connect(self.on_login_click)
        self.Linea_contrasena.returnPressed.connect(self.on_login_click)

    def on_login_click(self):
        usuario = self.Linea_usuario.text()                                   
        contrasena = self.Linea_contrasena.text()                                       

        login = LoginVO(usuario, contrasena)
        if self.controlador:
            self.controlador.comprobarLogin(login)
        return login
    
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
