from PyQt5.QtWidgets import QApplication
from src.vista.Login import Login
from src.vista.Registro import Registro
from src.vista.Estudiante import Estudiante
from src.vista.Bibliotecario import Bibliotecario
from src.vista.catalogo import VistaCatalogo
from src.vista.MisPrestamos import MisPrestamos
from src.vista.Devolucion import Devolucion
from src.modelo.Logica import Logica
from src.controlador.ControladorPrincipal import ControladorPrincipal

if __name__ == "__main__":
    app = QApplication([])
    login = Login()
    registro = Registro()
    modelo = Logica()
    estudiante = Estudiante()
    bibliotecario = Bibliotecario()
    mis_prestamos = MisPrestamos()
    devolucion = Devolucion()
    vistaCatalogo = VistaCatalogo()


    controlador = ControladorPrincipal(
        modelo, login, registro, estudiante, bibliotecario,
        vistaCatalogo,
        mis_prestamos,
        devolucion,
    )

    login.controlador = controlador
    controlador.ventanaIniciarSesion()
    app.exec_()
