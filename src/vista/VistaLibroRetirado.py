from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5 import uic
from PyQt5.QtCore import Qt

Form, Window = uic.loadUiType("./src/vista/Ui/VistaLibroRetirado.ui")

class VistaLibroRetirado(QDialog, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Libro retirado — BiblioULE")
        self._controlador = None
        self._isbn_actual = None
        self.boton_devolver.clicked.connect(self.on_devolver_click)
        self.boton_cerrar.clicked.connect(self.on_cerrar_click)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.MSWindowsFixedSizeDialogHint)

    def mostrarLibro(self, libro, motivo=None, fecha_retiro=None):
        self._isbn_actual = libro.isbn
        self.linea_titulo.setText(str(libro.titulo))
        self.linea_autor.setText(str(libro.autor))
        self.linea_tema.setText(str(libro.nombre_tema))
        self.linea_isbn.setText(str(libro.isbn))
        self.linea_fecha.setText(f"Fecha de llegada: {str(libro.fecha_llegada)}")
        self.linea_resumen.setText(str(libro.descripcion) if libro.descripcion else "Sin descripción")
        self.linea_fecharetirada.setText(f"Fecha de retirada: {str(fecha_retiro) if fecha_retiro else 'No disponible' }")
        self.linea_motivo.setText(f"Motivo: {motivo}" if motivo else "Motivo: Sin motivo especificado")

    def on_devolver_click(self):
        if self._isbn_actual and self._controlador:
            self._controlador.restaurarLibro(self._isbn_actual)
            self.close()

    def on_cerrar_click(self):
        if self._controlador:
            self._controlador.cerrarLibroRetirado()

    def lanzarAviso(self, aviso):
        QMessageBox.information(self, "Información", aviso)

    @property
    def controlador(self):
        return self._controlador

    @controlador.setter
    def controlador(self, ref_controlador):
        self._controlador = ref_controlador