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
        self._vistaAnadirCuenta.controlador = self

    def abrirAgregarCuenta(self):
        self._vistaGestionarCuentas.close()
        self._vistaAnadirCuenta.Linea_nombre.clear()
        self._vistaAnadirCuenta.linea_autor.clear()
        self._vistaAnadirCuenta.linea_isbn.clear()
        self._vistaAnadirCuenta.lineEdit.clear()
        self._vistaAnadirCuenta.lineEdit_2.clear()
        self._vistaAnadirCuenta.opcion_buscador.setCurrentIndex(-1)
        self._vistaAnadirCuenta.showMaximized()

    def eliminarCuenta(self, correo):
        if not correo:
            self._vistaGestionarCuentas.lanzarAviso("Introduce el correo de la cuenta.")
            return
        if correo == self._correo_admin:
            self._vistaGestionarCuentas.lanzarAviso("No puedes eliminar tu propia cuenta.", error=True)
            return
        usuario = self._modelo.obtenerUsuarioPorCorreo(correo)
        if usuario is None:
            self._vistaGestionarCuentas.lanzarAviso("No existe ninguna cuenta con ese correo.", error=True)
            return
        if usuario.tipo == "Admin":
            self._vistaGestionarCuentas.lanzarAviso("No puedes eliminar una cuenta de administrador.", error=True)
            return

        if self._modelo.eliminarUsuario(correo):
            self._vistaGestionarCuentas.lanzarAviso("Cuenta eliminada correctamente.")
        else:
            self._vistaGestionarCuentas.lanzarAviso("No se pudo eliminar la cuenta.", error=True)

    def registrarUsuario(self, nombre, apellidos, correo, contrasena, confirmar, tipo):
        valido, mensaje = self._modelo.validarRegistroAdmin(nombre, apellidos, correo, contrasena, confirmar, tipo)
        if not valido:
            self._vistaAnadirCuenta.lanzarAviso(mensaje)
            return

        registro = RegistroVO(nombre, apellidos, correo, contrasena, tipo)
        if self._modelo.registrarUsuario(registro):
            self._vistaAnadirCuenta.lanzarAviso("Cuenta creada con éxito.")
            self._vistaAnadirCuenta.close()
            self._vistaGestionarCuentas.lineEdit.clear()
            self._vistaGestionarCuentas.showMaximized()
        else:
            self._vistaAnadirCuenta.lanzarAviso("Error al crear la cuenta. El email puede estar ya registrado.")

    def registroAtras(self):
        self._vistaAnadirCuenta.close()
        self._vistaGestionarCuentas.lineEdit.clear()
        self._vistaGestionarCuentas.showMaximized()

    def volver(self):
        self._vistaGestionarCuentas.close()
        self._vistaAdmin.showMaximized()
