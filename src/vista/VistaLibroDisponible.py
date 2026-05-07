from PyQt5.QtWidgets import QDialog, QMessageBox, QInputDialog
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

    def configurarParaBibliotecario(self, es_bibliotecario):
        # La versión de bibliotecario usa una vista específica distinta
        # en lugar de añadir un botón extra aquí.
        if hasattr(self, '_boton_baja') and self._boton_baja:
            self._boton_baja.setVisible(False)

    def on_dar_baja_click(self):
        if self.controlador and self._isbn_actual:
            motivo, ok = QInputDialog.getText(self, "Motivo de baja", "Introduce el motivo de retirada:")
            if ok and motivo.strip():
                self.controlador.bajaLibro(self._isbn_actual, motivo.strip())
                self.close()
            elif ok:
                QMessageBox.warning(self, "Aviso", "Debes introducir un motivo.")

    @property
    def controlador(self):
        return self._controlador

    @controlador.setter
    def controlador(self, ref_controlador):
        self._controlador = ref_controlador