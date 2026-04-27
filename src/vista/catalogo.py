from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5 import uic

Form, Window = uic.loadUiType("./src/vista/Ui/VistaCatalogo.ui")

class VistaCatalogo(QDialog, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._controlador = None
        
        self.boton_buscar.clicked.connect(self.on_buscar_click)

    def on_buscar_click(self):
        if self.controlador:
            texto_busqueda = self.linea_busqueda.text()
            
            tema = self.opcion_buscador.currentText()

            self.controlador.buscarLibro(texto_busqueda, tema)


    def cargar_lista_libros(self, lista_libros):

        if lista_libros is None:
            self.tabla_libros.setRowCount(0)
            return

        self.tabla_libros.setRowCount(0)
        self.tabla_libros.setRowCount(len(lista_libros))
        
        for fila, libro in enumerate(lista_libros):
            self.tabla_libros.setItem(fila, 0, QTableWidgetItem(str(libro.titulo)))
            self.tabla_libros.setItem(fila, 1, QTableWidgetItem(str(libro.autor)))
            self.tabla_libros.setItem(fila, 2, QTableWidgetItem(str(libro.disponibilidad)))
            self.tabla_libros.setItem(fila, 3, QTableWidgetItem(str(libro.nombre_tema)))

    @property
    def controlador(self):
        return self._controlador

    @controlador.setter
    def controlador(self, ref_controlador):
        self._controlador = ref_controlador