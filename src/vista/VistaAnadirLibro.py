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
        isbn        = self.linea_isbn.text().strip()
        autor       = self.linea_autor.text().strip()
        tema        = self.opcion_buscador.currentText().strip()
        descripcion = self.linea_descripcion.toPlainText().strip()

        if not titulo or not isbn or not autor or not tema or not descripcion:
            QMessageBox.warning(self, "Campo faltante", "Por favor completa todos los campos antes de continuar.")
            return

        if self._controlador:
            self._controlador.anadirLibro(titulo, isbn, autor, tema, descripcion)

    def on_volver_click(self):
        if self._controlador:
            self._controlador.volver()

    def limpiarFormulario(self):
        self.Linea_nombre.clear()
        self.linea_isbn.clear()
        self.linea_autor.clear()
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