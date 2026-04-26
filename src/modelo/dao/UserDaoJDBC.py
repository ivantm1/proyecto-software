from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.UsuarioVO import UsuarioVO

class UserDaoJDBC(Conexion):
    SQL_CHECK_LOGIN = "SELECT nombre, apellidos, email, contrasena, tipo FROM Usuarios WHERE email = ? AND contrasena = ?"
    SQL_REGISTRO = "INSERT INTO Usuarios (nombre, apellidos, email, contrasena) VALUES (?, ?, ?, ?)"

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

    def registrarUsuario(self, registroVO):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_REGISTRO, (registroVO.nombre_user, registroVO.apellidos, registroVO.email, registroVO.contrasena))
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error en el registro: {e}")
            return False