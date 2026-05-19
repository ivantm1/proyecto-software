from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5 import uic

Form, Window = uic.loadUiType("./src/vista/Ui/VistaSeleccionPrestamo.ui")

class VistaSeleccionPrestamo(QDialog, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Detalle del préstamo — BiblioULE")
        self.controlador = None
        self._isbn_actual = None
        self._tipo_usuario = None

        self.boton_extender.clicked.connect(self.on_extender_click)
        self.boton_cerrar.clicked.connect(self.on_cerrar_click)

    def on_extender_click(self):
        if not self._isbn_actual:
            self.lanzarAviso("No hay ningún préstamo seleccionado.")
            return
        if self.controlador:
            if self._tipo_usuario == "Bibliotecario":
                self.controlador.terminarPrestamo(self._isbn_actual)
            else:
                self.controlador.prorrogarPrestamo(self._isbn_actual)

    def on_cerrar_click(self):
        self.close()

    def mostrarPrestamo(self, prestamo, tipo_usuario=None):
        self._isbn_actual = prestamo.isbn_libro
        self._tipo_usuario = tipo_usuario
        self.linea_titulo.setText(str(prestamo.titulo))
        self.linea_autor.setText(str(prestamo.autor))
        self.linea_tema.setText(str(prestamo.nombre_tema))
        self.linea_resumen.setText(str(prestamo.descripcion) if prestamo.descripcion else "Sin descripción")
        self.linea_estado.setText(f"Activo — Devolución: {prestamo.fecha_devolucion}")
        
                                                             
        if tipo_usuario == "Bibliotecario":
            self.boton_extender.setText("Terminar préstamo")
        else:
            self.boton_extender.setText("Extender préstamo")

    def lanzarAviso(self, aviso):
        QMessageBox.information(self, "Información", aviso)

    @property
    def controlador(self):
        return self._controlador

    @controlador.setter
    def controlador(self, ref_controlador):
        self._controlador = ref_controlador