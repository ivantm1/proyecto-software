from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import uic
from src.modelo.vo.LoginVO import LoginVO

# Cargar la interfaz generada desde el archivo .ui
Form, Window = uic.loadUiType("./src/vista/Ui/VistaLogin.ui")

class MiVentana(QMainWindow, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Inicializa los widgets
        self.controlador = None
        # Conectar el botón a la función
        self.botonAceptar.clicked.connect(self.on_button_click)

    def on_button_click(self):
        texto_usuario = self.textoUsuario.text() #Obtener el texto del campo nombre
        texto_contrasena = self.textoContra.text() #Obtener el texto del campo Contraseña
        self.controlador.comprobarLogin(texto_usuario, texto_contrasena)
        login = LoginVO(texto_usuario, texto_contrasena)
        return login
    
    def lanzarAviso(self, aviso):
        QMessageBox.information(self, "Info", aviso)
    
    @property
    def controlador(self):
        return self._controlador
    
    @controlador.setter
    def controlador(self, ref_controlador):
        self._controlador = ref_controlador
