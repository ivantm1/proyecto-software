from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.UsuariosVO import UsuariosVO
from src.modelo.vo.RegistroVO import UsuariosVO

class UserDaoJBDC(Conexion):
    SQL_SELECT = "SELECT nombre, primer_apellido, segundo_apellido, email FROM Usuarios"
    SQL_CHECK_LOGIN = "SELECT nombre, primer_apellido, segundo_apellido, email FROM Usuarios WHERE email = ? AND contrasena = ?"
    SQL_REGISTRO = "INSERT INTO Usuarios (nombre, apellidos, email, contrasena) VALUES (?, ?, ?)"

    def consultarLogin(self, loginVO):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_CHECK_LOGIN, (loginVO.nombre, loginVO.contrasena))
            row = cursor.fetchone()
            if row is None:
                return None
            nombre_user, first_name, full_name, email, tipo = row
            return UsuariosVO(nombre_user, first_name, full_name, email, tipo)
        except Exception as e:
            print(f"Error en el login: {e}")
            return None

    def registrarUsuario(self, registroVO):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_INSERT, (registroVO.nombre, registroVO.apellidos, registroVO.email, registroVO.contrasena))
            self.commit()
            return True
        except Exception as e:
            print(f"Error en el registro: {e}")
            return False

    def select(self):
        cursor = self.getCursor()
        users = []
        try:
            cursor.execute(self.SQL_SELECT)
            rows = cursor.fetchall()
            for row in rows:
                nombre, primer_apellido, segundo_apellido, email = row
                usuario = UsuariosVO(nombre, primer_apellido, segundo_apellido, email)

        except Exception as e:
            print(e)
        return users

        return users
