from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5 import uic
from PyQt5.QtCore import Qt

Form, Window = uic.loadUiType("./src/vista/Ui/VistaLibroBibliotecario.ui")

class VistaLibroBibliotecario(QDialog, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Detalle del libro — BiblioULE")
        self.controlador = None
        self._isbn_actual = None

        self.boton_reserva.clicked.connect(self.on_retirar_click)
        self.boton_cerrar.clicked.connect(self.on_cerrar_click)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.MSWindowsFixedSizeDialogHint)

    def mostrarLibro(self, libro):
        self._isbn_actual = libro.isbn
        self.linea_titulo.setText(str(libro.titulo))
        self.linea_autor.setText(f"Autor: {str(libro.autor)}")
        self.linea_tema.setText(str(libro.nombre_tema))
        self.linea_isbn.setText(f"ISBN: {str(libro.isbn)}")
        self.linea_fecha.setText(f"Llegada: {str(libro.fecha_llegada)}")
        self.linea_resumen.setText(str(libro.descripcion) if libro.descripcion else "Sin descripción")
        self.linea_estado.setText(str(libro.disponibilidad))
        self.lineEdit.clear()

    def on_retirar_click(self):
        if not self._isbn_actual:
            self.lanzarAviso("No hay ningún libro seleccionado.")
            return

        motivo = self.lineEdit.text().strip()
        if not motivo:
            QMessageBox.warning(self, "Aviso", "Debes introducir un motivo para retirar el libro.")
            return

        if self.controlador:
            exito = self.controlador.bajaLibro(self._isbn_actual, motivo)
            if exito:
                self.close()

    def on_cerrar_click(self):
        if self.controlador:
            self.controlador.cerrarLibroVistaBibliotecario()

    def lanzarAviso(self, aviso):
        QMessageBox.information(self, "Información", aviso)

    @property
    def controlador(self):
        return self._controlador

    @controlador.setter
    def controlador(self, ref_controlador):
        self._controlador = ref_controlador
