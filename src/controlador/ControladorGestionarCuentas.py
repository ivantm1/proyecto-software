from PyQt5.QtWidgets import QMessageBox
from src.modelo.vo.RegistroVO import RegistroVO

class ControladorGestionarCuentas:
    def __init__(self, modelo, vistaGestionarCuentas, vistaAdmin, vistaAnadirCuenta, correo_admin):
        self._modelo = modelo
        self._vistaGestionarCuentas = vistaGestionarCuentas
        self._vistaAdmin = vistaAdmin
        self._vistaAnadirCuenta = vistaAnadirCuenta
        self._correo_admin = correo_admin
        self._vistaGestionarCuentas.controlador = self

    def abrirAgregarCuenta(self):
        self._vistaGestionarCuentas.close()
        self._vistaAnadirCuenta.Linea_nombre.clear()
        self._vistaAnadirCuenta.linea_autor.clear()
        self._vistaAnadirCuenta.linea_isbn.clear()
        self._vistaAnadirCuenta.lineEdit.clear()
        self._vistaAnadirCuenta.lineEdit_2.clear()
        self._vistaAnadirCuenta.opcion_buscador.setCurrentIndex(-1)
        self._vistaAnadirCuenta.controlador = self
        self._vistaAnadirCuenta.showMaximized()

    def eliminarCuenta(self):
        correo = self._vistaGestionarCuentas.lineEdit.text().strip()
        if not correo:
            self._vistaGestionarCuentas.mostrarEstado("Introduce el correo de la cuenta.")
            return
        if correo == self._correo_admin:
            self._vistaGestionarCuentas.mostrarEstado("No puedes eliminar tu propia cuenta.")
            return
        usuario = self._modelo.obtenerUsuarioPorCorreo(correo)
        if usuario is None:
            self._vistaGestionarCuentas.mostrarEstado("No existe ninguna cuenta con ese correo.")
            return

        if self._modelo.eliminarUsuario(correo):
            self._vistaGestionarCuentas.lanzarAviso("Cuenta eliminada correctamente.")
            self._vistaGestionarCuentas.lineEdit.clear()
            self._vistaGestionarCuentas.mostrarEstado("")
        else:
            self._vistaGestionarCuentas.mostrarEstado("No se pudo eliminar la cuenta.")

    def registrarUsuario(self, nombre, apellidos, correo, contrasena, confirmar):
        if not all([nombre, apellidos, correo, contrasena, confirmar]):
            self._vistaAnadirCuenta.lanzarAviso("Rellena todos los campos.")
            return
        if not correo:
            self._vistaAnadirCuenta.lanzarAviso("Introduce un correo.")
            return
        if "@estudiantes.unileon.es" not in correo and "@unileon.es" not in correo:
            self._vistaAnadirCuenta.lanzarAviso("Usa un correo institucional válido.")
            return
        if contrasena != confirmar:
            self._vistaAnadirCuenta.lanzarAviso("Las contraseñas no coinciden.")
            return
        if len(contrasena) < 8:
            self._vistaAnadirCuenta.lanzarAviso("La contraseña debe tener al menos 8 caracteres.")
            return
        if not contrasena.isascii():
            self._vistaAnadirCuenta.lanzarAviso("La contraseña no debe contener caracteres extraños.")
            return

        tipo = self._vistaAnadirCuenta.opcion_buscador.currentText()
        if not tipo:
            self._vistaAnadirCuenta.lanzarAviso("Selecciona un tipo de cuenta.")
            return

        registro = RegistroVO(nombre, apellidos, correo, contrasena, tipo)
        if self._modelo.registrarUsuario(registro):
            self._vistaAnadirCuenta.lanzarAviso("Cuenta creada con éxito.")
            self._vistaAnadirCuenta.close()
            self._vistaGestionarCuentas.showMaximized()
        else:
            self._vistaAnadirCuenta.lanzarAviso("Error al crear la cuenta. El email puede estar ya registrado.")

    def registroAtras(self):
        self._vistaAnadirCuenta.close()
        self._vistaGestionarCuentas.showMaximized()

    def volver(self):
        self._vistaGestionarCuentas.close()
        self._vistaAdmin.showMaximized()
