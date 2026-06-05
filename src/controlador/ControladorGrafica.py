from PyQt5.QtWidgets import QMessageBox
from src.modelo.logica.LogicaGrafica import LogicaGrafica


class ControladorGrafica:
    def __init__(self, ref_modelo=None, ref_vista_grafica=None):
        self._modelo = ref_modelo
        self._vista = ref_vista_grafica
        self._logica = LogicaGrafica()

    def generarGrafica(self):
        ok, mensaje = self._logica.generar_grafica_top_temas_ultimo_mes()
        if not ok:
            QMessageBox.information(self._vista, "Información", mensaje or "No hay datos disponibles")

    def volver(self):
        pass
