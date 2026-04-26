from PyQt5.QtWidgets import QApplication
from src.vista.Login import Login
from src.vista.Registro import Registro
from src.vista.Estudiante import Estudiante
from src.vista.Bibliotecario import Bibliotecario
from src.vista.Catalogo import Catalogo
from src.vista.MisPrestamos import MisPrestamos
from src.vista.Perfil import Perfil
from src.vista.Prestamo import Prestamo
from src.vista.Sanciones import Sanciones
from src.vista.Devolucion import Devolucion
from src.modelo.Logica import Logica
from src.controlador.ControladorPrincipal import ControladorPrincipal

if __name__ == "__main__":
    app = QApplication([])

    login         = Login()
    registro      = Registro()
    estudiante    = Estudiante()
    bibliotecario = Bibliotecario()
    catalogo      = Catalogo()
    mis_prestamos = MisPrestamos()
    perfil        = Perfil()
    prestamo      = Prestamo()
    sanciones     = Sanciones()
    devolucion    = Devolucion()
    modelo        = Logica()

    controlador = ControladorPrincipal(
        modelo, login, registro, estudiante, bibliotecario,
        catalogo, mis_prestamos, perfil, prestamo, sanciones, devolucion
    )

    login.controlador = controlador
    controlador.ventanaIniciarSesion()
    app.exec_()
