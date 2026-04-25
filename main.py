from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
from src.vista.Login import Login
from src.vista.Registro import Registro
from src.modelo.Logica import Logica
from src.controlador.ControladorPrincipal import ControladorPrincipal

import os.path
os.path.dirname(os.path.abspath(__file__))
if __name__ == "__main__":
    app = QApplication([])
    login = Login()
    registro = Registro()
    modelo = Logica()
    controlador = ControladorPrincipal(modelo, login, registro)

    login.controlador = controlador
    controlador.ventanaIniciarSesion()
    app.exec_()