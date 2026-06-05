from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5 import uic

Form, Window = uic.loadUiType("./src/vista/Ui/VistaAnadirCuenta.ui")

class VistaAnadirCuenta(QDialog, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._controlador = None

        self.opcion_buscador.clear()
        self.opcion_buscador.addItem("Estudiante")
        self.opcion_buscador.addItem("Bibliotecario")
        self.opcion_buscador.addItem("Admin")
        self.opcion_buscador.setCurrentIndex(-1)

        self.boton_registro.clicked.connect(self.on_anadir_cuenta_click)
        self.boton_volver.clicked.connect(self.on_volver_click)

    def on_anadir_cuenta_click(self):
        if self._controlador:
            nombre = self.Linea_nombre.text()
            apellidos = self.linea_autor.text()
            correo = self.linea_isbn.text()
            contrasena = self.lineEdit.text()
            confirmar = self.lineEdit_2.text()
            tipo = self.opcion_buscador.currentText()

            self._controlador.registrarUsuario(nombre, apellidos, correo, contrasena, confirmar, tipo)

    def on_volver_click(self):
        if self._controlador:
            self._controlador.registroAtras()

    def lanzarAviso(self, aviso):
        QMessageBox.information(self, "Información", aviso)

    @property
    def controlador(self):
        return self._controlador

    @controlador.setter
    def controlador(self, ref_controlador):
        self._controlador = ref_controlador
