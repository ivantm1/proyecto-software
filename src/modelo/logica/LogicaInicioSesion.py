from src.modelo.dao.UserDaoJDBC import UserDaoJDBC

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
