from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
from src.modelo.vo.LoginVo import LoginVo
import os.path
base_path = os.path.dirname(os.path.abspath(__file__))
ui_path = os.path.join(base_path, "vista", "Ui", "Login.ui")

# Cargar la interfaz generada desde el archivo .ui
Form, Window = uic.loadUiType("./src/vista/Ui/VistaLogin.ui")

class MiVentana(QMainWindow, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Inicializa los widgets

        # Conectar el botón a la función
        self.Boton.clicked.connect(self.on_button_click)

    def on_button_click(self):
        print("Botón presionado")
        texto_nombre = self.textoNombre.text() #Obtener el texto del campo nombre
        texto_contrasena = self.textoNombre.text() #Obtener el texto del campo Contraseña
        print("El texto es: ")
        print(texto_nombre)
        login = LoginVo(texto_nombre, texto_contrasena)
        return login

if __name__ == "__main__":
    app = QApplication([])
    ventana = MiVentana()
    ventana.show()
    app.exec_()