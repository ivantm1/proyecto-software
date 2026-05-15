from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.UsuarioVO import UsuarioVO

class UserDaoJDBC(Conexion):
    SQL_CHECK_LOGIN = "SELECT nombre, apellidos, email, contrasena, tipo FROM Usuarios WHERE email = ? AND contrasena = ?"
    SQL_REGISTRO = "INSERT INTO Usuarios (nombre, apellidos, email, contrasena, tipo) VALUES (?, ?, ?, ?, ?)"
    SQL_CAMBIAR_CONTRASENA = "UPDATE Usuarios SET contrasena = ? WHERE email = ?"
    SQL_OBTENER_USUARIO = "SELECT nombre, apellidos, email, contrasena, tipo FROM Usuarios WHERE email = ?"
    SQL_ELIMINAR_USUARIO = "DELETE FROM Usuarios WHERE email = ?"
 
    def cambiarContrasena(self, correo, nueva_contrasena):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_CAMBIAR_CONTRASENA, (nueva_contrasena, correo))
            self.conexion.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error al cambiar contraseña: {e}")
            return False

    def comprobarLogin(self, loginVO):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_CHECK_LOGIN, (loginVO.nombre, loginVO.contrasena))
            row = cursor.fetchone()
            if row is None:
                return None
            nombre, apellidos, email, contrasena, tipo = row
            return UsuarioVO(nombre, apellidos, email, contrasena, tipo)
        except Exception as e:
            print(f"Error en el login: {e}")
            return None

    def obtenerUsuarioPorCorreo(self, correo):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_OBTENER_USUARIO, (correo,))
            row = cursor.fetchone()
            if row is None:
                return None
            nombre, apellidos, email, contrasena, tipo = row
            return UsuarioVO(nombre, apellidos, email, contrasena, tipo)
        except Exception as e:
            print(f"Error al obtener usuario: {e}")
            return None

    def eliminarUsuario(self, correo):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_ELIMINAR_USUARIO, (correo,))
            self.conexion.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error al eliminar usuario: {e}")
            return False

    def registrarUsuario(self, registroVO):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_REGISTRO, (registroVO.nombre, registroVO.apellidos, registroVO.correo, registroVO.contrasena, registroVO.tipo))
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error en el registro: {e}")
            return False