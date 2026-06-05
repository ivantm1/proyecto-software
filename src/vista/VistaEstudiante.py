from PyQt5.QtWidgets import QMainWindow, QMessageBox, QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QHeaderView
from PyQt5 import uic

Form, Window = uic.loadUiType("./src/vista/Ui/VistaEstudiante.ui")

class VistaEstudiante(QDialog, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.controlador = None
                                        
        self.boton_perfil.clicked.connect(self.on_ver_perfil_click)
        self.boton_catalogo.clicked.connect(self.on_ver_catalogo_click)
        self.boton_prestamos.clicked.connect(self.on_mis_prestamos_click)
        self.boton_reservas.clicked.connect(self.on_mis_reservas_click)
        self.boton_cerrar.clicked.connect(self.on_cerrar_sesion_click)

    def on_ver_perfil_click(self):
        if self.controlador:
            self.controlador.ventanaVerPerfil()

    def on_ver_catalogo_click(self):
        if self.controlador:
            self.controlador.ventanaCatalogo()

    def on_mis_prestamos_click(self):
        if self.controlador:
            self.controlador.ventanaMisPrestamos()

    def on_mis_reservas_click(self):
        if self.controlador:
            self.controlador.ventanaMisReservas()

    def on_cerrar_sesion_click(self):
        if self.controlador:
            self.controlador.cerrarSesion()

    def actualizar_datos_estudiante(self):
        if not self.controlador or not hasattr(self.controlador, '_usuario_activo'):
            return
        
        usuario = self.controlador._usuario_activo
        modelo = self.controlador._modelo
        
        # Actualizar nombre
        nombre_completo = f"{usuario.nombre}"
        self.linea_nombre.setText(f"Bienvenido: {nombre_completo}")
        
        # Actualizar prestamos
        num_prestamos = modelo._prestamos.contarPrestamosEstudiante(usuario.correo)
        self.linea_prestamos.setText(f"Prestamos activos: {num_prestamos}")
        
        # Actualizar reservas
        num_reservas = modelo._reservas.contarReservasEstudiante(usuario.correo)
        self.linea_reservas.setText(f"Reservas activas: {num_reservas}")

    @property
    def controlador(self):
        return self._controlador

    @controlador.setter
    def controlador(self, ref_controlador):
        self._controlador = ref_controlador
        self.actualizar_datos_estudiante()