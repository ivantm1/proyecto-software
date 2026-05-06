from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5 import uic
from PyQt5.QtCore import Qt

Form, Window = uic.loadUiType("./src/vista/Ui/VistaLibroPrestado.ui")

class VistaLibroPrestado(QDialog, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Detalle del libro — BiblioULE")
        self.controlador = None
        self._isbn_actual = None

        self.boton_reserva.clicked.connect(self.on_reservar_click)
        self.boton_cerrar.clicked.connect(self.on_cerrar_click)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.MSWindowsFixedSizeDialogHint)


    def on_reservar_click(self):
        if not self._isbn_actual:
            self.lanzarAviso("No hay ningún libro seleccionado.")
            return
        if self.controlador:
            self.controlador.reservarLibro(self._isbn_actual)

    def mostrarLibro(self, libro):
        """Rellena los labels con los datos del libro seleccionado"""
        self._isbn_actual = libro.isbn
        self.linea_titulo.setText(str(libro.titulo))
        self.linea_autor.setText(str(libro.autor))
        self.linea_tema.setText(str(libro.nombre_tema))
        self.linea_resumen.setText(str(libro.descripcion) if libro.descripcion else "Sin descripción")

        estado = str(libro.disponibilidad).lower()
        if estado == "prestado" and libro.fecha_devolucion:
            texto_disp = f"Prestado hasta {str(libro.fecha_devolucion)[:10]}"
        else:
            texto_disp = str(libro.disponibilidad)

        self.linea_estado.setText(str(texto_disp))

    def on_cerrar_click(self):
        self.controlador.cerrarLibroPrestado()

    def lanzarAviso(self, aviso):
        QMessageBox.information(self, "Información", aviso)

    @property
    def controlador(self):
        return self._controlador

    @controlador.setter
    def controlador(self, ref_controlador):
        self._controlador = ref_controlador