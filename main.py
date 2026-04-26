from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
from src.vista.Login import Login
from src.vista.Registro import Registro
from src.vista.Estudiante import Estudiante
from src.vista.Bibliotecario import Bibliotecario
from src.vista.catalogo import VistaCatalogo

from src.modelo.Logica import Logica
from src.controlador.ControladorPrincipal import ControladorPrincipal

import os.path
os.path.dirname(os.path.abspath(__file__))
if __name__ == "__main__":
    app = QApplication([])
    login = Login()
    registro = Registro()
    modelo = Logica()
    estudiante= Estudiante()
    bibliotecario= Bibliotecario()

    controlador = ControladorPrincipal(modelo, login, registro, estudiante, bibliotecario, VistaCatalogo)

    login.controlador = controlador
    controlador.ventanaIniciarSesion()
    app.exec_()