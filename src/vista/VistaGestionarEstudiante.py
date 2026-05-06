from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5 import uic

Form, Window = uic.loadUiType("./src/vista/Ui/VistaGestionarEstudiante.ui")

class VistaGestionarEstudiante(QDialog, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._controlador = None
        self._correo_estudiante = None

        # Conexión de botones
        self.boton_volver.clicked.connect(self.on_volver_click)
        self.boton_cambiar.clicked.connect(self.on_hacer_prestamo_click)
        self.boton_prestamos.clicked.connect(self.on_ver_prestamos_click)
        self.boton_reservas.clicked.connect(self.on_ver_reservas_click)
        self.boton_sanciones.clicked.connect(self.on_gestionar_sanciones_click)

    def cargar_datos(self, usuario, num_prestamos, num_reservas, num_sanciones):
        self._correo_estudiante = usuario.correo
        # Asumiendo que el objeto usuario tiene atributos nombre, apellidos y correo
        self.linea_nombre.setText(usuario.nombre)
        self.linea_apellidos.setText(usuario.apellidos)
        self.linea_email.setText(usuario.correo)
        self.linea_prestamos.setText(f"{num_prestamos} préstamos activos")
        self.linea_reservas.setText(f"{num_reservas} reservas activas")
        self.linea_sanciones.setText(f"{num_sanciones} sanciones activas")

    def on_hacer_prestamo_click(self):
        isbn = self.lineEdit.text().strip()
        if not isbn:
            QMessageBox.warning(self, "Aviso", "Por favor, introduce un ISBN válido para realizar el préstamo.")
            return
            
        if self._controlador:
            self._controlador.hacerPrestamoDesdeGestion(isbn, self._correo_estudiante)
            self.lineEdit.clear()

    def on_volver_click(self):
        if self._controlador:
            self._controlador.volverGestionarEstudiante()

    def on_ver_prestamos_click(self):
        self._controlador.verPrestamosEstudiante(self._correo_estudiante)

    def on_ver_reservas_click(self):
        # Lógica futura para ver detalles de reservas
        pass

    def on_gestionar_sanciones_click(self):
        if self._controlador and self._correo_estudiante:
            self._controlador.gestionarSanciones(self._correo_estudiante)

    @property
    def controlador(self):
        return self._controlador

    @controlador.setter
    def controlador(self, ref_controlador):
        self._controlador = ref_controlador