from PyQt5.QtWidgets import QDialog, QMessageBox, QInputDialog, QLineEdit
from PyQt5 import uic

Form, Window = uic.loadUiType("./src/vista/Ui/VistaPerfil.ui")

class VistaPerfil(QDialog, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Mi Perfil — BiblioULE")
        self._controlador = None

        self.boton_volver.clicked.connect(self.on_volver_click)
        self.boton_cambiar.clicked.connect(self.on_cambiar_contrasena_click)

    def mostrarUsuario(self, nombre, apellidos, correo, tipo):
        self.linea_nombre.setText(nombre)
        self.linea_apellidos.setText(apellidos)
        self.linea_email.setText(correo)

    def on_volver_click(self):
        if self._controlador:
            self._controlador.cerrarPerfil()

    def on_cambiar_contrasena_click(self):
        if self._controlador:
            nueva, ok1 = QInputDialog.getText(
                self, "Cambiar contraseña", "Nueva contraseña:", QLineEdit.Password
            )
            if not ok1 or not nueva:
                return
            confirmar, ok2 = QInputDialog.getText(
                self, "Cambiar contraseña", "Confirmar contraseña:", QLineEdit.Password
            )
            if not ok2 or not confirmar:
                return
            self._controlador.cambiarContrasena(nueva, confirmar)

    def lanzarAviso(self, aviso):
        QMessageBox.information(self, "Información", aviso)

    @property
    def controlador(self):
        return self._controlador

    @controlador.setter
    def controlador(self, ref_controlador):
        self._controlador = ref_controlador