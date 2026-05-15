from PyQt5.QtWidgets import QMainWindow, QMessageBox, QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QHeaderView
from PyQt5 import uic

Form, Window = uic.loadUiType("./src/vista/Ui/VistaEstudiante.ui")

class VistaEstudiante(QDialog, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.controlador = None
        # Conectar el botón a la función
        self.boton_perfil.clicked.connect(self.on_ver_perfil_click)
        self.boton_catalogo.clicked.connect(self.on_ver_catalogo_click)
        self.boton_prestamos.clicked.connect(self.on_mis_prestamos_click)
        self.boton_reservas.clicked.connect(self.on_mis_reservas_click)
        self.boton_cerrar.clicked.connect(self.on_cerrar_sesion_click)
        try:
            self.boton_favoritos.clicked.connect(self.on_ver_favoritos_click)
        except AttributeError:
            pass    # El botón aún no existe en el .ui, pendiente de añadir

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

    def on_ver_favoritos_click(self):
        if not self.controlador:
            return
        libros = self.controlador.obtenerHistorialTemasFavoritos()

        dialog = QDialog(self)
        dialog.setWindowTitle("Libros de mis temas favoritos")
        dialog.setMinimumSize(700, 400)
        layout = QVBoxLayout(dialog)

        if not libros:
            layout.addWidget(QLabel("No tienes temas favoritos o no hay libros disponibles."))
        else:
            tabla = QTableWidget()
            tabla.setColumnCount(4)
            tabla.setHorizontalHeaderLabels(["Título", "Autor", "Tema", "Estado"])
            tabla.setRowCount(len(libros))
            tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            for i, libro in enumerate(libros):
                tabla.setItem(i, 0, QTableWidgetItem(str(libro.titulo)))
                tabla.setItem(i, 1, QTableWidgetItem(str(libro.autor)))
                tabla.setItem(i, 2, QTableWidgetItem(str(libro.nombre_tema)))
                tabla.setItem(i, 3, QTableWidgetItem(str(libro.disponibilidad)))
            layout.addWidget(tabla)

        dialog.exec_()


    @property
    def controlador(self):
        return self._controlador

    @controlador.setter
    def controlador(self, ref_controlador):
        self._controlador = ref_controlador