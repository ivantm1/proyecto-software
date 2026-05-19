from src.modelo.dao.UserDaoJDBC import UserDaoJDBC
from src.modelo.vo.LoginVO import LoginVO
 
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
        if not actual or not nueva or not confirmar:
            self._vista.lanzarAviso("Por favor, rellena todos los campos.")
            return
 
        if nueva != confirmar:
            self._vista.lanzarAviso("Las contraseñas no coinciden.")
            return
 
        if len(nueva) < 8:
            self._vista.lanzarAviso("La contraseña debe tener al menos 8 caracteres.")
            return
 
        if not nueva.isascii():
            self._vista.lanzarAviso("La contraseña no debe contener caracteres extraños.")
            return
 
        if actual == nueva:
            self._vista.lanzarAviso("La nueva contraseña debe ser diferente a la actual.")
            return
 
        login = LoginVO(self._usuario.correo, actual)
        usuario_valido = self._modelo.comprobarLogin(login)
        if usuario_valido is None:
            self._vista.lanzarAviso("La contraseña actual no es correcta.")
            return
 
        exito = self._modelo.cambiarContrasena(self._usuario.correo, nueva)
        if exito:
            self._usuario._contrasena = nueva
            self._vista.lanzarAviso("Contraseña actualizada correctamente.")
        else:
            self._vista.lanzarAviso("Error al actualizar la contraseña. Inténtalo de nuevo.")