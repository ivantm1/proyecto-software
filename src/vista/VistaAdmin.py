from PyQt5.QtWidgets import QDialog
from PyQt5 import uic

Form, Window = uic.loadUiType("./src/vista/Ui/VistaAdmin.ui")

class VistaAdmin(QDialog, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._controlador = None

        self.boton_catalogo.clicked.connect(self.on_ver_catalogo_click)
        self.boton_cuentas.clicked.connect(self.on_gestionar_cuentas_click)
        self.boton_copia.clicked.connect(self.on_copia_seguridad_click)
        self.boton_cerrar.clicked.connect(self.on_cerrar_sesion_click)

    def on_ver_catalogo_click(self):
        if self._controlador:
            self._controlador.ventanaCatalogo()

    def on_gestionar_cuentas_click(self):
        if self._controlador:
            self._controlador.ventanaGestionarCuentas()
    
    def on_copia_seguridad_click(self):
        if self._controlador:
            self._controlador.realizarCopiaSeguridad()

    def on_cerrar_sesion_click(self):
        if self._controlador:
            self._controlador.cerrarSesion()

    @property
    def controlador(self):
        return self._controlador

    @controlador.setter
    def controlador(self, ref_controlador):
        self._controlador = ref_controlador