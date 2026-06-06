from PyQt5.QtWidgets import QDialog, QMessageBox, QVBoxLayout, QSizePolicy
from PyQt5 import uic

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

Form, Window = uic.loadUiType("./src/vista/Ui/VistaEstadisticas.ui")


class VistaEstadisticas(QDialog, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Estadísticas — BiblioULE")

        self.boton_buscar.clicked.connect(self.on_generar_grafica)
        self.boton_volver.clicked.connect(self.on_volver_click)

        # Canvas de Matplotlib embebido
        self.figure = Figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Poner el canvas en label_2
        if hasattr(self, 'label_2'):
            container = self.label_2
            container.setText("")
            container.setStyleSheet("background-color: white;")
            layout = QVBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(self.canvas)
            container.setLayout(layout)
            self.canvas.updateGeometry()

        self._controlador = None

    def on_generar_grafica(self):
        # Mapear selección a código de periodo
        sel = self.opcion_buscador.currentText()
        self._controlador.generarGrafica(sel)

    def mostrarGrafica(self, figura):
        """Muestra la gráfica ya generada en el canvas embebido."""
        try:
            if figura is None:
                return
            self.figure = figura
            self.canvas.figure = self.figure
            self.canvas.draw()
        except Exception:
            pass

    def on_volver_click(self):
        self._controlador.volver()

    def lanzarAviso(self, mensaje):
        QMessageBox.information(self, "Información", mensaje)

    @property
    def controlador(self):
        return self._controlador

    @controlador.setter
    def controlador(self, ref_controlador):
        self._controlador = ref_controlador
