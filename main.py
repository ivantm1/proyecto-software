from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
from src.vista.Login import Login
from src.vista.Registro import Registro
from src.vista.Estudiante import Estudiante
from src.vista.Bibliotecario import Bibliotecario
from src.modelo.Logica import Logica
from src.controlador.ControladorPrincipal import ControladorPrincipal
from src.vista.Catalogo import Catalogo
from src.vista.MisPrestamos import MisPrestamos
from src.vista.Perfil import Perfil
from src.vista.Sanciones import Sanciones
from src.vista.Devolucion import Devolucion

import os.path
os.path.dirname(os.path.abspath(__file__))
if __name__ == "__main__":
    app = QApplication([])
    login = Login()
    registro = Registro()
    modelo = Logica()
    estudiante= Estudiante()
    bibliotecario= Bibliotecario()
    catalogo      = Catalogo()
    mis_prestamos = MisPrestamos()
    perfil        = Perfil()
    sanciones     = Sanciones()
    devolucion    = Devolucion()

    controlador = ControladorPrincipal(
            modelo, login, registro, estudiante, bibliotecario,
            catalogo, mis_prestamos, perfil, sanciones, devolucion
        )

    login.controlador = controlador
    controlador.ventanaIniciarSesion()
    app.exec_()