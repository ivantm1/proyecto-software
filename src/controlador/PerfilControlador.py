from src.modelo.dao.UserDaoJDBC import UserDaoJDBC
 
class PerfilControlador:
    def __init__(self, ref_modelo, ref_vista_perfil, ref_vista_anterior, usuario_activo):
        self._modelo          = ref_modelo
        self._vista           = ref_vista_perfil
        self._vista_anterior  = ref_vista_anterior  # Estudiante o Bibliotecario
        self._usuario         = usuario_activo       # UsuarioVO del usuario logueado
 
    def cerrarPerfil(self):
        self._vista.close()
        self._vista_anterior.showMaximized()
 
    def cambiarContrasena(self, nueva, confirmar):
        if not nueva or not confirmar:
            self._vista.lanzarAviso("Por favor, rellena ambos campos.")
            return
 
        if nueva != confirmar:
            self._vista.lanzarAviso("Las contraseñas no coinciden.")
            return
 

        exito = self._modelo.cambiarContrasena(self._usuario.correo, nueva)
        if exito:
            self._vista.lanzarAviso("Contraseña actualizada correctamente.")
        else:
            self._vista.lanzarAviso("Error al actualizar la contraseña. Inténtalo de nuevo.")