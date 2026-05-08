from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QMessageBox, QComboBox
from PyQt5 import uic
from PyQt5.QtWidgets import QHeaderView, QSizePolicy, QAbstractItemView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

Form, Window = uic.loadUiType("./src/vista/Ui/VistaCatalogo.ui")

class VistaCatalogo(QDialog, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowState(self.windowState() | Qt.WindowMaximized)
        self.tabla_libros.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)        
        self.tabla_libros.horizontalHeader().setStretchLastSection(True)
        self.tabla_libros.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tabla_libros.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla_libros.setSelectionMode(QAbstractItemView.SingleSelection)
        self._controlador = None
        self._libros = []



        self.boton_volver.clicked.connect(self.on_volver_click)
        self.boton_buscar.clicked.connect(self.on_buscar_click)
        self.tabla_libros.doubleClicked.connect(self.libro_seleccionado)

    def on_buscar_click(self):
        if self.controlador:
            texto_busqueda = self.linea_busqueda.text()
            tema = self.opcion_buscador.currentText()
            self.controlador.buscarLibro(texto_busqueda, tema)

    def on_volver_click(self):
        self.controlador.registroAtras()

    def libro_seleccionado(self):
        seleccion = self.tabla_libros.selectedItems()
        if not seleccion:
            return
        fila = seleccion[0].row()
        estado = self.tabla_libros.item(fila, 3).text()
        if self.controlador:
            if estado == "Disponible":
                self.controlador.abrirDetalleLibroDisponible(fila)
            elif "Retirado" in estado:
                self.controlador.abrirDetalleLibroRetirado(fila)
            else:
                self.controlador.abrirDetalleLibroPrestado(fila)

    def obtenerLibroPorFila(self, fila):
        if 0 <= fila < len(self._libros):
            return self._libros[fila]
        return None

    def lanzarAviso(self, aviso):
        QMessageBox.information(self, "Información", aviso)



    def cargar_lista_libros_estudiante(self, lista_libros):
        if lista_libros is None:
            self.tabla_libros.setRowCount(0)
            self._libros = []
            return
        
        seleccion_actual = self.opcion_disponibilidad.currentText() if hasattr(self.opcion_disponibilidad, 'currentText') else "Todos"
        self.opcion_disponibilidad.clear()
        self.opcion_disponibilidad.addItems(["Todos", "Disponibles", "Prestados"])
        self.opcion_disponibilidad.setCurrentText(seleccion_actual)
        
        libros_filtrados = [l for l in lista_libros if str(l.disponibilidad).lower() != "retirado"]
        seleccion_actual = self.opcion_disponibilidad.currentText()
        
        if seleccion_actual == "Disponibles":
            self._libros = [l for l in libros_filtrados if str(l.disponibilidad).lower() == "disponible"]
        elif seleccion_actual == "Prestados":
            self._libros = [l for l in libros_filtrados if "prestado" in str(l.disponibilidad).lower()]
        else:
            self._libros = libros_filtrados
        
        self.tabla_libros.setRowCount(0)
        self.tabla_libros.setRowCount(len(self._libros))
        self.tabla_libros.resizeColumnsToContents()

        for fila, libro in enumerate(self._libros):
            self.tabla_libros.setItem(fila, 0, QTableWidgetItem(str(libro.titulo)))
            self.tabla_libros.setItem(fila, 1, QTableWidgetItem(str(libro.autor)))
            self.tabla_libros.setItem(fila, 2, QTableWidgetItem(str(libro.nombre_tema)))

            estado = str(libro.disponibilidad).lower()
            if estado == "prestado" and libro.fecha_devolucion:
                texto_disp = f"Prestado hasta {str(libro.fecha_devolucion)[:10]}"
            else:
                texto_disp = str(libro.disponibilidad)

            disp = QTableWidgetItem(texto_disp)
            if estado == "disponible":
                disp.setBackground(QColor(200, 240, 200))
            elif "reservado" in estado or "prestado" in estado:
                disp.setBackground(QColor(240, 200, 200))
            self.tabla_libros.setItem(fila, 3, disp)
            disp.setFlags(disp.flags() ^ Qt.ItemIsEditable)

        self.tabla_libros.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def cargar_lista_libros_bibliotecario(self, lista_libros):
        if lista_libros is None:
            self.tabla_libros.setRowCount(0)
            self._libros = []
            return

        seleccion_actual = self.opcion_disponibilidad.currentText() if hasattr(self.opcion_disponibilidad, 'currentText') else "Todos"
        self.opcion_disponibilidad.clear()
        self.opcion_disponibilidad.addItems(["Todos", "Disponibles", "Prestados", "Retirados"])    
        self.opcion_disponibilidad.setCurrentText(seleccion_actual)
        
        
        if seleccion_actual == "Disponibles":
            self._libros = [l for l in lista_libros if str(l.disponibilidad).lower() == "disponible"]
        elif seleccion_actual == "Prestados":
            self._libros = [l for l in lista_libros if "prestado" in str(l.disponibilidad).lower()]
        elif seleccion_actual == "Retirados":
            self._libros = [l for l in lista_libros if "retirado" in str(l.disponibilidad).lower()]
        else:
            self._libros = list(lista_libros)
        
        self.tabla_libros.setRowCount(0)
        self.tabla_libros.setRowCount(len(self._libros))
        self.tabla_libros.resizeColumnsToContents()

        for fila, libro in enumerate(self._libros):
            self.tabla_libros.setItem(fila, 0, QTableWidgetItem(str(libro.titulo)))
            self.tabla_libros.setItem(fila, 1, QTableWidgetItem(str(libro.autor)))
            self.tabla_libros.setItem(fila, 2, QTableWidgetItem(str(libro.nombre_tema)))

            estado = str(libro.disponibilidad).lower()
            if estado == "prestado" and libro.fecha_devolucion:
                texto_disp = f"Prestado hasta {str(libro.fecha_devolucion)[:10]}"
            else:
                texto_disp = str(libro.disponibilidad)

            disp = QTableWidgetItem(texto_disp)
            if estado == "disponible":
                disp.setBackground(QColor(200, 240, 200))
            elif "reservado" in estado or "prestado" in estado:
                disp.setBackground(QColor(255, 218, 185))
            elif "retirado" in estado:
                disp.setBackground(QColor(240, 200, 200))
            self.tabla_libros.setItem(fila, 3, disp)
            disp.setFlags(disp.flags() ^ Qt.ItemIsEditable)

        self.tabla_libros.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    @property
    def controlador(self):
        return self._controlador

    @controlador.setter
    def controlador(self, ref_controlador):
        self._controlador = ref_controlador