from PyQt5.QtWidgets import QDialog, QMessageBox, QTableWidgetItem
from PyQt5 import uic
from PyQt5.QtWidgets import QHeaderView, QSizePolicy, QAbstractItemView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

Form, Window = uic.loadUiType("./src/vista/Ui/VistaMisPrestamos.ui")

class VistaMisPrestamos(QDialog, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Mis préstamos — BiblioULE")
        self.controlador = None

        self.boton_buscar.clicked.connect(self.on_buscar_click)
        self.tabla_libros.cellDoubleClicked.connect(self.on_fila_doble_click)
        self.boton_volver.clicked.connect(self.on_volver_click)

    def on_buscar_click(self):
        if self.controlador:
            titulo = self.linea_busqueda.text()
            tema   = self.opcion_buscador.currentText()
            self.controlador.buscarPrestamos(titulo, tema)

    def on_fila_doble_click(self, fila, columna):
                                                                           
        if self.controlador:
            self.controlador.abrirDetallePrestamo(fila)

    def on_volver_click(self):
        self.controlador.registroAtras()

    def mostrarPrestamos(self, lista_prestamos):
        self._prestamos = lista_prestamos or []
        self.tabla_libros.clearContents()
        self.tabla_libros.setRowCount(0)
        self.tabla_libros.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        if not lista_prestamos:
            return

        import datetime

        tipo_usuario = None
        try:
            if self.controlador:
                tipo_usuario = getattr(self.controlador, '_tipo_usuario', None)
        except Exception:
            tipo_usuario = None

        if tipo_usuario == 'Estudiante':
            lista_prestamos = [p for p in (lista_prestamos or []) if getattr(p, 'estado', '') in ('Activo', 'Vencido')]

        for prestamo in lista_prestamos:
            fila = self.tabla_libros.rowCount()
            self.tabla_libros.insertRow(fila)
            self.tabla_libros.setItem(fila, 0, QTableWidgetItem(str(prestamo.titulo)))
            self.tabla_libros.setItem(fila, 1, QTableWidgetItem(str(prestamo.autor)))
            self.tabla_libros.setItem(fila, 2, QTableWidgetItem(str(prestamo.nombre_tema)))
            
            try:
                fecha = prestamo.fecha_devolucion
                if isinstance(fecha, str):
                    fecha_dt = datetime.date.fromisoformat(str(fecha)[:10])
                else:
                    fecha_dt = fecha

                dias_restantes = (fecha_dt - datetime.date.today()).days
                if dias_restantes < 0:
                    texto_fin = f"Vencido el: {fecha_dt}"
                    item_fin = QTableWidgetItem(texto_fin)
                    item_fin.setForeground(QColor(200, 0, 0))
                else:
                    texto_fin = f"{dias_restantes} días"
                    item_fin = QTableWidgetItem(texto_fin)

                self.tabla_libros.setItem(fila, 3, item_fin)
            except Exception:
                # Fallback: mostrar fecha original
                self.tabla_libros.setItem(fila, 3, QTableWidgetItem(str(prestamo.fecha_devolucion)))
        
            if getattr(prestamo, 'estado', '') == 'Devuelto' and tipo_usuario != 'Estudiante':
                for col in range(self.tabla_libros.columnCount()):
                    item = self.tabla_libros.item(fila, col)
                    if item:
                        item.setBackground(QColor(220, 220, 220))

    def obtenerPrestamoPorFila(self, fila):
        if hasattr(self, '_prestamos') and 0 <= fila < len(self._prestamos):
            return self._prestamos[fila]
        return None

    def lanzarAviso(self, aviso):
        QMessageBox.information(self, "Información", aviso)

    @property
    def controlador(self):
        return self._controlador

    @controlador.setter
    def controlador(self, ref_controlador):
        self._controlador = ref_controlador