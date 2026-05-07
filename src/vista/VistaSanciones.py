from PyQt5.QtWidgets import QDialog, QMessageBox, QTableWidgetItem
from PyQt5 import uic
from PyQt5.QtWidgets import QHeaderView

Form, Window = uic.loadUiType("./src/vista/Ui/VistaSanciones.ui")

class VistaSanciones(QDialog, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Sanciones — BiblioULE")
        self._controlador = None

        self.pushButton.clicked.connect(self.on_aplicar_sancion_click)
        self.tabla_sanciones.cellDoubleClicked.connect(self.on_sancion_double_clicked)
        self.boton_volver.clicked.connect(self.on_volver_click)

    def on_aplicar_sancion_click(self):
        motivo = self.linea_motivo.text().strip()
        dias_texto = self.linea_dias.text().strip()

        if not motivo:
            self.lanzarAviso("Introduce un motivo para la sanción.")
            return

        if not dias_texto.isdigit() or int(dias_texto) <= 0:
            self.lanzarAviso("Introduce un número válido de días para la sanción.")
            return

        if not self._controlador or not hasattr(self._controlador, '_estudiante_actual'):
            self.lanzarAviso("No se ha identificado el estudiante para aplicar la sanción.")
            return

        estudiante = self._controlador._estudiante_actual
        if estudiante is None or not hasattr(estudiante, 'correo'):
            self.lanzarAviso("No se ha identificado el estudiante para aplicar la sanción.")
            return

        correo = estudiante.correo
        from src.modelo.dao.SancionDaoJDBC import SancionDaoJDBC

        dias = int(dias_texto)
        resultado = SancionDaoJDBC().aplicarSancionDanio(correo, motivo, dias)

        if resultado:
            self.lanzarAviso("Sanción registrada correctamente.")
            self.linea_motivo.clear()
            self.linea_dias.clear()
            sanciones = self._controlador._modelo.obtenerSancionesEstudiante(correo)
            self.mostrarSanciones(sanciones)
        else:
            self.lanzarAviso("Error al aplicar la sanción.")

    def on_sancion_double_clicked(self, fila, columna):
        if fila < 0:
            return

        item_fecha = self.tabla_sanciones.item(fila, 0)
        item_dias = self.tabla_sanciones.item(fila, 1)
        item_tipo = self.tabla_sanciones.item(fila, 2)

        if not item_fecha or not item_dias or not item_tipo:
            return

        fecha_inicio = item_fecha.text().strip()
        dias = item_dias.text().strip()
        motivo = item_tipo.text().strip()

        respuesta = QMessageBox.question(
            self,
            "Eliminar sanción",
            f"¿Eliminar la sanción:\n{motivo} - {dias} días - {fecha_inicio}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if respuesta != QMessageBox.Yes:
            return

        if not self._controlador or not hasattr(self._controlador, '_estudiante_actual'):
            self.lanzarAviso("No se ha identificado el estudiante para eliminar la sanción.")
            return

        estudiante = self._controlador._estudiante_actual
        if estudiante is None or not hasattr(estudiante, 'correo'):
            self.lanzarAviso("No se ha identificado el estudiante para eliminar la sanción.")
            return

        correo = estudiante.correo
        from src.modelo.dao.SancionDaoJDBC import SancionDaoJDBC

        eliminado = SancionDaoJDBC().eliminarSancion(correo, motivo, fecha_inicio, dias)
        if eliminado:
            self.lanzarAviso("Sanción eliminada correctamente.")
            sanciones = self._controlador._modelo.obtenerSancionesEstudiante(correo)
            self.mostrarSanciones(sanciones)
        else:
            self.lanzarAviso("No se pudo eliminar la sanción seleccionada.")

    def on_volver_click(self):
        if self._controlador:
            self._controlador.volverASanciones()

    def mostrarSanciones(self, lista_sanciones):
        self.tabla_sanciones.setRowCount(0)
        self.tabla_sanciones.resizeColumnsToContents()

        total_dias = 0
        if lista_sanciones:
            for sancion in lista_sanciones:
                fila = self.tabla_sanciones.rowCount()
                self.tabla_sanciones.insertRow(fila)
                self.tabla_sanciones.setItem(fila, 0, QTableWidgetItem(str(sancion.fecha_inicio)))
                self.tabla_sanciones.setItem(fila, 1, QTableWidgetItem(str(sancion.duracion_sancion)))
                self.tabla_sanciones.setItem(fila, 2, QTableWidgetItem(str(sancion.tipo)))
                try:
                    total_dias += int(sancion.duracion_sancion)
                except Exception:
                    pass
            self.tabla_sanciones.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        if total_dias == 0:
            self.linea_tiempo.setText("El estudiante no tiene sanciones activas.")
        else:   
            self.linea_tiempo.setText(f"Total sanciones: {total_dias} días")
            self.linea_tiempo.setStyleSheet("font-weight: bold; text-transform: uppercase; font-size: 22px; letter-spacing: 1px; color: #B22222")

    def lanzarAviso(self, aviso):
        QMessageBox.information(self, "Información", aviso)

    @property
    def controlador(self):
        return self._controlador

    @controlador.setter
    def controlador(self, ref_controlador):
        self._controlador = ref_controlador