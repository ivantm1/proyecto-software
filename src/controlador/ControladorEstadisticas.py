from PyQt5.QtWidgets import QMessageBox
from src.modelo.logica.LogicaEstadisticas import LogicaEstadisticas


class ControladorEstadisticas:
    def __init__(self, ref_modelo=None, ref_vista_grafica=None, ref_vista_bibliotecario=None):
        self._modelo = ref_modelo
        self._vista = ref_vista_grafica
        self._vistaBibliotecario = ref_vista_bibliotecario
        self._logica = LogicaEstadisticas()

    def generarGrafica(self, sel):
        if 'Última semana' == sel:
            periodo = '1w'
        elif 'Último mes' == sel:
            periodo = '1m'
        elif 'Últimos 3 meses' == sel:
            periodo = '3m'
        else:
            self._vista.lanzarAviso("Elija un periodo")
            return

        figura, titulo_or_msg = self._logica.crear_grafica_top_temas(periodo, self._vista.figure)
        if figura is None:
            self._vista.lanzarAviso(titulo_or_msg)
            return

        self._vista.mostrarGrafica(figura)

    def volver(self):
        self._vista.close()
        self._vistaBibliotecario.showMaximized()

