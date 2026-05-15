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

    def registrarUsuario(self, registro, confirmar):
        if not all([registro.nombre, registro.apellidos, registro.correo, registro.contrasena, confirmar]):
            self._vistaAnadirCuenta.lanzarAviso("Rellena todos los campos.")
            return
        if registro.tipo == "Estudiante" and not registro.correo.endswith("@estudiantes.unileon.es"):
            self._vistaAnadirCuenta.lanzarAviso("Usa un correo institucional válido (@estudiantes.unileon.es).")
            return
        
        if (registro.tipo == "Bibliotecario" or registro.tipo == "Admin") and not registro.correo.endswith("@unileon.es"):
            self._vistaAnadirCuenta.lanzarAviso("Usa un correo institucional válido (@unileon.es).")
            return
        if registro.contrasena != confirmar:
            self._vistaAnadirCuenta.lanzarAviso("Las contraseñas no coinciden.")
            return
        if len(registro.contrasena) < 8:
            self._vistaAnadirCuenta.lanzarAviso("La contraseña debe tener al menos 8 caracteres.")
            return
        if not registro.contrasena.isascii():
            self._vistaAnadirCuenta.lanzarAviso("La contraseña no debe contener caracteres extraños.")
            return

        tipo = self._vistaAnadirCuenta.opcion_buscador.currentText()
        if not tipo:
            self._vistaAnadirCuenta.lanzarAviso("Selecciona un tipo de cuenta.")
            return

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
