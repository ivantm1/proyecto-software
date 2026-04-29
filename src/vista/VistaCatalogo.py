from PyQt5.QtWidgets import QDialog, QTableWidgetItem
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
        
        self.boton_buscar.clicked.connect(self.on_buscar_click)
        self.tabla_libros.doubleClicked.connect(self.libro_seleccionado)  

    def on_buscar_click(self):
        if self.controlador:
            texto_busqueda = self.linea_busqueda.text()
            
            tema = self.opcion_buscador.currentText()

            self.controlador.buscarLibro(texto_busqueda, tema)

    def libro_seleccionado(self):
        seleccion = self.tabla_libros.selectedItems()
        
        if not seleccion:
            return

        fila = seleccion[0].row()
        
        ISBN = self.tabla_libros.item(fila, 0).text()
        print(ISBN)
        #self.controlador.abrir_detalle_libro(titulo, autor)

    def cargar_lista_libros_estudiante(self, lista_libros):

        if lista_libros is None:
            self.tabla_libros.setRowCount(0)
            return
        
        lista_libros = [l for l in lista_libros if str(l.disponibilidad).lower() != "retirado"]
        self.tabla_libros.setRowCount(0)
        self.tabla_libros.setRowCount(len(lista_libros))
        self.tabla_libros.resizeColumnsToContents()
        
        for fila, libro in enumerate(lista_libros):
            self.tabla_libros.setItem(fila, 0, QTableWidgetItem(str(libro.titulo)))
            self.tabla_libros.setItem(fila, 1, QTableWidgetItem(str(libro.autor)))
            self.tabla_libros.setItem(fila, 2, QTableWidgetItem(str(libro.nombre_tema)))

            estado = str(libro.disponibilidad).lower()
            disp = QTableWidgetItem(str(libro.disponibilidad)) # Creamos el item real

            if estado == "disponible":
                disp.setBackground(QColor(200, 240, 200)) # Verde
            elif "reservado" in estado or "prestado" in estado:
                disp.setBackground(QColor(240, 200, 200)) # Rojo

            self.tabla_libros.setItem(fila, 3, disp) # Insertamos el objeto PINTADO        
            disp.setFlags(disp.flags() ^ Qt.ItemIsEditable)

        self.tabla_libros.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


    def cargar_lista_libros_bibliotecario(self, lista_libros):

        if lista_libros is None:
            self.tabla_libros.setRowCount(0)
            return
        
        lista_libros = [l for l in lista_libros]
        self.tabla_libros.setRowCount(0)
        self.tabla_libros.setRowCount(len(lista_libros))
        self.tabla_libros.resizeColumnsToContents()
        
        for fila, libro in enumerate(lista_libros):
            self.tabla_libros.setItem(fila, 0, QTableWidgetItem(str(libro.titulo)))
            self.tabla_libros.setItem(fila, 1, QTableWidgetItem(str(libro.autor)))
            self.tabla_libros.setItem(fila, 2, QTableWidgetItem(str(libro.nombre_tema)))

            estado = str(libro.disponibilidad).lower()
            disp = QTableWidgetItem(str(libro.disponibilidad)) # Creamos el item real

            if estado == "disponible":
                disp.setBackground(QColor(200, 240, 200)) # Verde
            elif "reservado" in estado or "prestado" in estado:
                disp.setBackground(QColor(255, 218, 185)) # Naranja
            elif "retirado" in estado:
                disp.setBackground(QColor(240, 200, 200)) # Rojo

            self.tabla_libros.setItem(fila, 3, disp) # Insertamos el objeto PINTADO        
            disp.setFlags(disp.flags() ^ Qt.ItemIsEditable)

        self.tabla_libros.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    @property
    def controlador(self):
        return self._controlador

    @controlador.setter
    def controlador(self, ref_controlador):
        self._controlador = ref_controlador