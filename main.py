from PyQt5.QtWidgets import QApplication
from src.vista.VistaLogin import VistaLogin
from src.vista.VistaRegistro import VistaRegistro
from src.vista.VistaEstudiante import VistaEstudiante
from src.vista.VistaBibliotecario import VistaBibliotecario
from src.vista.VistaCatalogo import VistaCatalogo
from src.vista.VistaMisPrestamos import VistaMisPrestamos
from src.vista.VistaMisReservas import VistaMisReservas
from src.vista.VistaPerfil import VistaPerfil
from src.vista.VistaDevolverLibro import VistaDevolverLibro
from src.vista.VistaAnadirLibro import VistaAnadirLibro
from src.vista.VistaBuscarEstudiante import VistaBuscarEstudiante
from src.vista.VistaAdmin import VistaAdmin
from src.vista.VistaGestionarCuentas import VistaGestionarCuentas
from src.vista.VistaAnadirCuenta import VistaAnadirCuenta
from src.vista.VistaEstadisticas import VistaEstadisticas
from src.modelo.Logica import Logica
from src.modelo.logica.LoggerSingleton import Logger
from src.controlador.ControladorPrincipal import ControladorPrincipal

if __name__ == "__main__":
    app = QApplication([])
    login            = VistaLogin()
    registro         = VistaRegistro()
    modelo           = Logica()
    estudiante       = VistaEstudiante()
    bibliotecario    = VistaBibliotecario()
    mis_prestamos    = VistaMisPrestamos()
    mis_reservas     = VistaMisReservas()
    perfil           = VistaPerfil()
    devolucion       = VistaDevolverLibro()
    anadirLibro      = VistaAnadirLibro()
    buscarEstudiante = VistaBuscarEstudiante()
    vistaCatalogo    = VistaCatalogo()
    admin            = VistaAdmin()
    gestionarCuentas = VistaGestionarCuentas()
    anadirCuenta      = VistaAnadirCuenta()
    estadisticas      = VistaEstadisticas()

    controlador = ControladorPrincipal(
        modelo, login,
        ref_vista_registro=registro,
        ref_vista_estudiante=estudiante,
        ref_vista_bibliotecario=bibliotecario,
        ref_vista_admin=admin,
        ref_vista_gestionar_cuentas=gestionarCuentas,
        ref_vista_anadir_cuenta=anadirCuenta,
        ref_vista_catalogo=vistaCatalogo,
        ref_vista_mis_prestamos=mis_prestamos,
        ref_vista_mis_reservas=mis_reservas,
        ref_vista_perfil=perfil,
        ref_vista_devolucion=devolucion,
        ref_vista_buscar_estudiante=buscarEstudiante,
        ref_vista_anadir_libro=anadirLibro,
        ref_vista_estadistica=estadisticas
    )

    def registrar_cierre_sesion():
        if getattr(controlador, '_cerrando_por_cerrar_sesion', False):
            return
        if controlador._usuario_activo:
            Logger().cierre_sesion(controlador._usuario_activo.correo)

    app.aboutToQuit.connect(registrar_cierre_sesion)

    login.controlador = controlador
    controlador.ventanaIniciarSesion()
    app.exec_()