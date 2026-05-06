from PyQt5.QtWidgets import QApplication
from src.vista.Login import Login
from src.vista.VistaRegistro import VistaRegistro
from src.vista.Estudiante import Estudiante
from src.vista.Bibliotecario import Bibliotecario
from src.vista.VistaCatalogo import VistaCatalogo
from src.vista.MisPrestamos import MisPrestamos
from src.vista.MisReservas import MisReservas
from src.vista.VistaPerfil import VistaPerfil
from src.vista.VistaDevolverLibro import VistaDevolverLibro
from src.vista.VistaAnadirLibro import VistaAnadirLibro
from src.vista.VistaBuscarEstudiante import VistaBuscarEstudiante
from src.modelo.Logica import Logica
from src.controlador.ControladorPrincipal import ControladorPrincipal

if __name__ == "__main__":
    app = QApplication([])
    login            = Login()
    registro         = VistaRegistro()
    modelo           = Logica()
    estudiante       = Estudiante()
    bibliotecario    = Bibliotecario()
    mis_prestamos    = MisPrestamos()
    mis_reservas     = MisReservas()
    perfil           = VistaPerfil()
    devolucion       = VistaDevolverLibro()
    anadirLibro      = VistaAnadirLibro()
    buscarEstudiante = VistaBuscarEstudiante()
    vistaCatalogo    = VistaCatalogo()

    controlador = ControladorPrincipal(
        modelo, login,
        ref_vista_registro=registro,
        ref_vista_estudiante=estudiante,
        ref_vista_bibliotecario=bibliotecario,
        ref_vista_catalogo=vistaCatalogo,
        ref_vista_mis_prestamos=mis_prestamos,
        ref_vista_mis_reservas=mis_reservas,
        ref_vista_perfil=perfil,
        ref_vista_devolucion=devolucion,
        ref_vista_buscar_estudiante=buscarEstudiante,
        ref_vista_anadir_libro=anadirLibro,
    )

    login.controlador = controlador
    controlador.ventanaIniciarSesion()
    app.exec_()