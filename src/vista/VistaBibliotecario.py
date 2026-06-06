from PyQt5.QtWidgets import QMainWindow, QMessageBox, QDialog
from PyQt5 import uic

Form, Window = uic.loadUiType("./src/vista/Ui/VistaBibliotecario.ui")

class VistaBibliotecario(QDialog, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._controlador = None

        self.boton_perfil.clicked.connect(self.on_ver_perfil_click)
        self.boton_catalogo.clicked.connect(self.on_ver_catalogo_click)
        self.boton_estudiante.clicked.connect(self.on_buscar_estudiante_click)
        self.boton_devolucion.clicked.connect(self.on_devolucion_click)
        self.boton_estadisticas.clicked.connect(self.on_ver_estadisticas_click)
        self.boton_cerrar.clicked.connect(self.on_cerrar_sesion_click)
        self.pushButton.clicked.connect(self.on_anadir_libro_click)

    def on_ver_perfil_click(self):
        if self._controlador:
            self._controlador.ventanaVerPerfil()

    def on_ver_catalogo_click(self):
        if self._controlador:
            self._controlador.ventanaCatalogo()

    def on_buscar_estudiante_click(self):
        if self._controlador:
            self._controlador.ventanaBuscarEstudiante()

    def on_devolucion_click(self):
        if self._controlador:
            self._controlador.ventanaDevolucion()

    def on_ver_estadisticas_click(self):
        if self._controlador:
            self._controlador.ventanaEstadisticas()

    def on_cerrar_sesion_click(self):
        if self._controlador:
            self._controlador.cerrarSesion()

    def on_anadir_libro_click(self):
        if self._controlador:
            self._controlador.ventanaAnadirLibro()

    @property
    def controlador(self):
        return self._controlador

    @controlador.setter
    def controlador(self, ref_controlador):
        self._controlador = ref_controlador