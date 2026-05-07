from PyQt5.QtWidgets import QDialog, QMessageBox, QLineEdit, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
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

    def mostrarUsuario(self, nombre, apellidos, correo, tipo, sancion=None):
        self.linea_nombre.setText(nombre)
        self.linea_apellidos.setText(apellidos)
        self.linea_email.setText(correo)
        if tipo=="Bibliotecario" or tipo=="Admin":
            self.label_6.setText("")
        elif sancion:
            self.label_6.setText(f"⚠️ Sanción activa hasta: {sancion}")
        else:
            self.label_6.setText("Sin sanciones activas.")

    def on_volver_click(self):
        if self._controlador:
            self._controlador.cerrarPerfil()

    def on_cambiar_contrasena_click(self):
        if self._controlador:
            actual, nueva, confirmar = self.pedir_contrasenas()
            if actual is None:
                return
            self._controlador.cambiarContrasena(actual, nueva, confirmar)

    def pedir_contrasenas(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Cambiar contraseña")
        dialog.setModal(True)

        layout = QVBoxLayout(dialog)

        input_actual = QLineEdit()
        input_actual.setEchoMode(QLineEdit.Password)
        input_nueva = QLineEdit()
        input_nueva.setEchoMode(QLineEdit.Password)
        input_confirmar = QLineEdit()
        input_confirmar.setEchoMode(QLineEdit.Password)

        for label_text, widget in [
            ("Contraseña actual:", input_actual),
            ("Nueva contraseña:", input_nueva),
            ("Repetir nueva contraseña:", input_confirmar),
        ]:
            row_layout = QVBoxLayout()
            row_layout.addWidget(QLabel(label_text))
            row_layout.addWidget(widget)
            layout.addLayout(row_layout)

        buttons_layout = QHBoxLayout()
        aceptar = QPushButton("Aceptar")
        cancelar = QPushButton("Cancelar")
        buttons_layout.addStretch()
        buttons_layout.addWidget(aceptar)
        buttons_layout.addWidget(cancelar)
        layout.addLayout(buttons_layout)

        aceptar.clicked.connect(dialog.accept)
        cancelar.clicked.connect(dialog.reject)

        if dialog.exec_() == QDialog.Accepted:
            return input_actual.text(), input_nueva.text(), input_confirmar.text()
        return None, None, None

    def lanzarAviso(self, aviso):
        QMessageBox.information(self, "Información", aviso)

    @property
    def controlador(self):
        return self._controlador

    @controlador.setter
    def controlador(self, ref_controlador):
        self._controlador = ref_controlador