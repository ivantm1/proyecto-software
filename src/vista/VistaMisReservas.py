import datetime
from PyQt5.QtWidgets import QDialog, QMessageBox, QTableWidgetItem
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import QHeaderView, QSizePolicy, QAbstractItemView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

Form, Window = uic.loadUiType("./src/vista/Ui/VistaMisReservas.ui")

class VistaMisReservas(QDialog, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Mis reservas — BiblioULE")
        self.controlador = None
        self._tipo_usuario = None
        self._modo_global = False

        self.boton_buscar.clicked.connect(self.on_buscar_click)
        self.boton_volver.clicked.connect(self.on_volver_click)

        self.tabla_libros.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tabla_libros.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.tabla_libros.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tabla_libros.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tabla_libros.cellClicked.connect(self.on_reserva_click)
    def on_buscar_click(self):
        if self.controlador:
            titulo = self.linea_busqueda.text().strip()
            tema   = self.opcion_buscador.currentText().strip()
            self.controlador.buscarReservas(titulo, tema)


    def on_volver_click(self):
        self.controlador.registroAtras()

    def mostrarReservas(self, lista_reservas):
        self._reservas = lista_reservas or []
        self.tabla_libros.clearContents()
        self.tabla_libros.setRowCount(0)

        correos_unicos = {r.correo_estudiante for r in self._reservas} if self._reservas else set()
        modo_global = len(correos_unicos) > 1

        if modo_global:
            self.tabla_libros.setColumnCount(5)
            self.tabla_libros.setHorizontalHeaderLabels(
                ["Alumno", "Nombre", "Autor", "Tema", "Estado"]
            )
        else:
            self.tabla_libros.setColumnCount(4)
            self.tabla_libros.setHorizontalHeaderLabels(
                ["Nombre", "Autor", "Tema", "Estado"]
            )

        self.tabla_libros.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        if not lista_reservas:
            return

        if self._tipo_usuario != "Bibliotecario":
            lista_reservas = [r for r in lista_reservas if str(r.estado).strip().lower() != 'caducada']

        self._modo_global = modo_global

        for reserva in lista_reservas:
            fila = self.tabla_libros.rowCount()
            self.tabla_libros.insertRow(fila)
            estado_mostrar = self._formatear_estado_reserva(reserva)
            titulo_item = QTableWidgetItem(str(reserva.titulo))
            titulo_item.setData(Qt.UserRole, reserva.isbn_libro)
            if modo_global:
                self.tabla_libros.setItem(fila, 0, QTableWidgetItem(str(reserva.correo_estudiante)))
                self.tabla_libros.setItem(fila, 1, titulo_item)
                self.tabla_libros.setItem(fila, 2, QTableWidgetItem(str(reserva.autor)))
                self.tabla_libros.setItem(fila, 3, QTableWidgetItem(str(reserva.nombre_tema)))
                self.tabla_libros.setItem(fila, 4, QTableWidgetItem(estado_mostrar))
            else:
                self.tabla_libros.setItem(fila, 0, titulo_item)
                self.tabla_libros.setItem(fila, 1, QTableWidgetItem(str(reserva.autor)))
                self.tabla_libros.setItem(fila, 2, QTableWidgetItem(str(reserva.nombre_tema)))
                self.tabla_libros.setItem(fila, 3, QTableWidgetItem(estado_mostrar))

            self._aplicar_color_fila(fila, reserva)

    def _formatear_estado_reserva(self, reserva):
        estado = str(reserva.estado or '').strip()
        if estado.upper() == 'RECOGER':
            dias = self._dias_restantes_para_recoger(reserva)
            if dias <= 0:
                return 'Disponible para recoger (último día)'
            return f'Disponible para recoger ({dias} días restantes)'
        if estado.lower() == 'espera':
            return 'Espera'
        return estado

    def _dias_restantes_para_recoger(self, reserva):
        fecha = reserva.fecha_reserva
        try:
            if isinstance(fecha, str):
                fecha = datetime.date.fromisoformat(fecha[:10])
            elif hasattr(fecha, 'date'):
                fecha = fecha.date()
            limite = fecha + datetime.timedelta(days=7)
            return max((limite - datetime.date.today()).days, 0)
        except Exception:
            return 0

    def _aplicar_color_fila(self, fila, reserva):
        estado = str(reserva.estado or '').strip().lower()
        if estado == 'caducada':
            color = QColor(255, 204, 204)
        elif estado == 'recoger':
            color = QColor(204, 255, 204)
        else:
            return
        for col in range(self.tabla_libros.columnCount()):
            item = self.tabla_libros.item(fila, col)
            if item:
                item.setBackground(color)

    def on_reserva_click(self, fila, columna):
        if self._tipo_usuario != 'Bibliotecario':
            return

        estado_col = 4 if self._modo_global else 3
        estado_item = self.tabla_libros.item(fila, estado_col)
        if not estado_item or estado_item.text().strip().lower() != 'caducada':
            return

        titulo_index = 1 if self._modo_global else 0
        titulo_item = self.tabla_libros.item(fila, titulo_index)
        if not titulo_item:
            return

        isbn = titulo_item.data(Qt.UserRole)
        if not isbn:
            return

        respuesta = QMessageBox.question(
            self,
            "Confirmar devolución",
            "¿Quiere devolver este libro al catálogo y así el libro vuelve al catálogo y la reserva termina y no aparece más?",
            QMessageBox.Yes | QMessageBox.No
        )
        if respuesta != QMessageBox.Yes:
            return

        if self.controlador and hasattr(self.controlador, 'finalizarReservaCaducada'):
            exito = self.controlador.finalizarReservaCaducada(isbn)
            if exito:
                QMessageBox.information(self, "Reserva terminada", "Libro devuelto al catálogo y reserva finalizada.")
                self.controlador.actualizarReservas()
            else:
                QMessageBox.warning(self, "Error", "No se pudo finalizar la reserva caducada.")

    def lanzarAviso(self, aviso):
        QMessageBox.information(self, "Información", aviso)

    @property
    def controlador(self):
        return self._controlador

    @controlador.setter
    def controlador(self, ref_controlador):
        self._controlador = ref_controlador
        self._tipo_usuario = getattr(ref_controlador, '_tipo_usuario', None)
        if self._tipo_usuario == "Bibliotecario":
            self.tabla_libros.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
            self.tabla_libros.setFocusPolicy(QtCore.Qt.StrongFocus)
        else:
            self.tabla_libros.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
            self.tabla_libros.setFocusPolicy(QtCore.Qt.NoFocus)