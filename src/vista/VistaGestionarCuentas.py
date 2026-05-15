from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5 import uic

Form, Window = uic.loadUiType("./src/vista/Ui/VistaGestionarCuentas.ui")

class VistaGestionarCuentas(QDialog, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._controlador = None

        self.boton_cuenta.clicked.connect(self.on_anadir_cuenta_click)
        self.boton_eliminar.clicked.connect(self.on_eliminar_cuenta_click)
        self.boton_volver.clicked.connect(self.on_volver_click)

    def on_anadir_cuenta_click(self):
        if self._controlador:
            self._controlador.abrirAgregarCuenta()

    def on_eliminar_cuenta_click(self):
        correo = self.lineEdit.text().strip()
        if self._controlador:
            self._controlador.eliminarCuenta(correo)

    def on_volver_click(self):
        if self._controlador:
            self._controlador.volver()

    def lanzarAviso(self, mensaje, error=False):
        if error:
            QMessageBox.critical(self, "Error", mensaje)
        else:
            QMessageBox.information(self, "Información", mensaje)

    @property
    def controlador(self):
        return self._controlador

    @controlador.setter
    def controlador(self, ref_controlador):
        self._controlador = ref_controlador
