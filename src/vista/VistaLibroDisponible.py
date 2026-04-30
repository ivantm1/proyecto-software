from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5 import uic
from PyQt5.QtCore import Qt

Form, Window = uic.loadUiType("./src/vista/Ui/VistaLibroDisponible.ui")

class VistaLibroDisponible(QDialog, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Detalle del libro — BiblioULE")
        self.controlador = None
        self._isbn_actual = None
        self.boton_cerrar.clicked.connect(self.on_cerrar_click)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.MSWindowsFixedSizeDialogHint)

    def mostrarLibro(self, libro):
        self._isbn_actual = libro.isbn
        self.linea_titulo.setText(str(libro.titulo))
        self.linea_autor.setText(f"Autor: {str(libro.autor)}")
        self.linea_tema.setText(str(libro.nombre_tema))
        self.linea_resumen.setText(str(libro.descripcion) if libro.descripcion else "Sin descripción")


    def on_cerrar_click(self):
        self.controlador.cerrarLibroDisponible()

    @property
    def controlador(self):
        return self._controlador

    @controlador.setter
    def controlador(self, ref_controlador):
        self._controlador = ref_controlador