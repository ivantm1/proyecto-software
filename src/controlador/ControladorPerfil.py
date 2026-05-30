from src.modelo.dao.UserDaoJDBC import UserDaoJDBC
 
class ControladorPerfil:
    def __init__(self, ref_modelo, ref_vista_perfil, ref_vista_anterior, usuario_activo):
        self._modelo          = ref_modelo
        self._vista           = ref_vista_perfil
        self._vista_anterior  = ref_vista_anterior                              
        self._usuario         = usuario_activo                                       
 
    def cerrarPerfil(self):
        self._vista.close()
        self._vista_anterior.showMaximized()
 
    def cambiarContrasena(self, actual, nueva, confirmar):
        valido, mensaje = self._modelo.validarCambioContrasena(self._usuario.correo, actual, nueva, confirmar)
        if not valido:
            self._vista.lanzarAviso(mensaje)
            return

        exito = self._modelo.cambiarContrasena(self._usuario.correo, nueva)
        if exito:
            self._usuario._contrasena = nueva
            self._vista.lanzarAviso("Contraseña actualizada correctamente.")
        else:
            self._vista.lanzarAviso("Error al actualizar la contraseña. Inténtalo de nuevo.")