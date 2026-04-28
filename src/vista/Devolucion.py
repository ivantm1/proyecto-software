from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox


class Devolucion(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Registrar devolución — BiblioULE")
        self.setMinimumSize(450, 200)
        self._controlador = None

    def on_devolver_click(self):
        isbn = self.Linea_isbn.text().strip()
        if not isbn:
            self.lanzarAviso("Introduce el ISBN del libro.")
            return
        if self._controlador:
            self._controlador.registrarDevolucion(isbn)

    def mostrarResultado(self, mensaje):
        self.lbl_resultado.setText(mensaje)

    def lanzarAviso(self, aviso):
        QMessageBox.information(self, "Información", aviso)

    @property
    def controlador(self):
        return self._controlador

    @controlador.setter
    def controlador(self, ref_controlador):
        self._controlador = ref_controlador
