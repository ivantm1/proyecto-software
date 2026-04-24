from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.UsuariosVO import UsuariosVO

class UserDaoJBDC(Conexion):
    SQL_SELECT = "SELECT nombre_user, first_name, full_name, email, tipo FROM Usuarios"
    SQL_CHECK_LOGIN = "SELECT nombre_user, first_name, full_name, email, tipo FROM Usuarios WHERE nombre_user = ? AND contrasena = ?"

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
            print(e)
            return None

    def select(self):
        cursor = self.getCursor()
        users = []
        try:
            cursor.execute(self.SQL_SELECT)
            rows = cursor.fetchall()
            for row in rows:
                nombre_user, first_name, full_name, email, tipo = row
                users.append(UsuariosVO(nombre_user, first_name, full_name, email, tipo))
        except Exception as e:
            print(e)
        return users

        return users
