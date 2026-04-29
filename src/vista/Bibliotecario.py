from PyQt5.QtWidgets import QMainWindow, QMessageBox, QDialog
from PyQt5 import uic

Form, Window = uic.loadUiType("./src/vista/Ui/VistaBibliotecario.ui")

class Bibliotecario(QDialog, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.controlador = None
        # Conectar el botón a la función
        self.boton_perfil.clicked.connect(self.on_ver_perfil_click)
        self.boton_catalogo.clicked.connect(self.on_ver_catalogo_click)
        self.boton_devolucion.clicked.connect(self.on_devolucion_click)
        self.boton_prestamo.clicked.connect(self.on_prestamo_click)
        self.boton_sanciones.clicked.connect(self.on_sanciones_click)
        self.boton_cerrar.clicked.connect(self.on_cerrar_perfil_click)

    def on_ver_perfil_click(self):
        if self.controlador:
            self.controlador.ventanaVerPerfil()

    def on_ver_catalogo_click(self):
        if self.controlador:
            self.controlador.ventanaCatalogo()

    def on_devolucion_click(self):
        if self.controlador:
            self.controlador.ventanaDevolucion()

    def on_prestamo_click(self):
        if self.controlador:
            self.controlador.ventanaPrestamo()

    def on_sanciones_click(self):
        if self.controlador:
            self.controlador.ventanaSanciones()

    def on_cerrar_perfil_click(self):
        if self.controlador:
            self.controlador.CerrarPerfil()




    @property
    def controlador(self):
        return self._controlador

    @controlador.setter
    def controlador(self, ref_controlador):
        self._controlador = ref_controlador