from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5 import uic

Form, Window = uic.loadUiType("./src/vista/Ui/VistaAnadirLibro.ui")

class VistaAnadirLibro(QDialog, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Añadir libro — BiblioULE")
        self._controlador = None

        self.boton_registro.clicked.connect(self.on_anadir_click)
        self.boton_volver.clicked.connect(self.on_volver_click)

    def on_anadir_click(self):
        titulo      = self.Linea_nombre.text().strip()
        isbn        = self.Linea_confirmar_contrasena.text().strip()
        autor       = self.Linea_apellidos.text().strip()
        tema        = self.Linea_correo.text().strip()
        descripcion = self.linea_descripcion.toPlainText().strip()

        if self._controlador:
            self._controlador.anadirLibro(titulo, isbn, autor, tema, descripcion)

    def on_volver_click(self):
        if self._controlador:
            self._controlador.volver()

    def limpiarFormulario(self):
        self.Linea_nombre.clear()
        self.Linea_confirmar_contrasena.clear()
        self.Linea_apellidos.clear()
        self.Linea_correo.clear()
        self.linea_descripcion.clear()
        self.label.setText("")

    def mostrarResultado(self, mensaje):
        self.label.setText(mensaje)

    def lanzarAviso(self, aviso):
        QMessageBox.information(self, "Información", aviso)

    @property
    def controlador(self):
        return self._controlador

    @controlador.setter
    def controlador(self, ref_controlador):
        self._controlador = ref_controlador