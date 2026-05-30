from src.modelo.dao.UserDaoJDBC import UserDaoJDBC
from src.modelo.vo.LoginVO import LoginVO

class LogicaInicioSesion:
                                                               

    def comprobarLogin(self, loginVO):
        return UserDaoJDBC().comprobarLogin(loginVO)

    def registrarUsuario(self, registroVO):
        return UserDaoJDBC().registrarUsuario(registroVO)

    def cambiarContrasena(self, correo, nueva_contrasena):
        return UserDaoJDBC().cambiarContrasena(correo, nueva_contrasena)

    def obtenerUsuarioPorCorreo(self, correo):
        return UserDaoJDBC().obtenerUsuarioPorCorreo(correo)

    def eliminarUsuario(self, correo):
        return UserDaoJDBC().eliminarUsuario(correo)

    def validarRegistro(self, nombre, apellidos, correo, contrasena, confirmar):
        if not all([nombre, apellidos, correo, contrasena, confirmar]):
            return False, "Rellena todos los campos."
        if not correo.endswith("@estudiantes.unileon.es"):
            return False, "Usa un correo institucional @estudiantes.unileon.es"
        if contrasena != confirmar:
            return False, "Las contraseñas no coinciden."
        if len(contrasena) < 8:
            return False, "La contraseña debe tener al menos 8 caracteres."
        if not contrasena.isascii():
            return False, "La contraseña no debe contener caracteres extraños."
        return True, ""

    def validarRegistroAdmin(self, nombre, apellidos, correo, contrasena, confirmar, tipo):
        """Valida registro de Admin o Bibliotecario con validaciones específicas."""
        if not all([nombre, apellidos, correo, contrasena, confirmar, tipo]):
            return False, "Rellena todos los campos."
        
        if tipo == "Estudiante" and not correo.endswith("@estudiantes.unileon.es"):
            return False, "Usa un correo institucional válido (@estudiantes.unileon.es)."
        
        if (tipo == "Bibliotecario" or tipo == "Admin") and not correo.endswith("@unileon.es"):
            return False, "Usa un correo institucional válido (@unileon.es)."
        
        if contrasena != confirmar:
            return False, "Las contraseñas no coinciden."
        
        if len(contrasena) < 8:
            return False, "La contraseña debe tener al menos 8 caracteres."
        
        if not contrasena.isascii():
            return False, "La contraseña no debe contener caracteres extraños."
        
        return True, ""

    def validarCambioContrasena(self, correo, actual, nueva, confirmar):
        """Valida el cambio de contraseña y verifica que la contraseña actual sea correcta."""
        if not actual or not nueva or not confirmar:
            return False, "Por favor, rellena todos los campos."
        
        if nueva != confirmar:
            return False, "Las contraseñas no coinciden."
        
        if len(nueva) < 8:
            return False, "La contraseña debe tener al menos 8 caracteres."
        
        if not nueva.isascii():
            return False, "La contraseña no debe contener caracteres extraños."
        
        if actual == nueva:
            return False, "La nueva contraseña debe ser diferente a la actual."
        
        login = LoginVO(correo, actual)
        usuario_valido = self.comprobarLogin(login)
        if usuario_valido is None:
            return False, "La contraseña actual no es correcta."
        
        return True, ""
