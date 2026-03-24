from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.UsuariosVO import UsuariosVO

class UserDaoJBDC(Conexion):
    SQL_SELECT = "SELECT nombre, primer_apellido, segundo_apellido, email FROM Usuarios"
    SQL_INSERT = ""
    SQL_CHECK_LOGIN = "SELECT nombre, primer_apellido, segundo_apellido, email FROM Usuarios WHERE email = ? AND contrasena = ?"

    def consultarLogin(self, loginVO):
        cursor = self.getCursor()

        try:
            cursor.execute(self.SQL_CHECK_LOGIN, (loginVO.nombre, loginVO.contrasena))
            rows = cursor.fetchone()

            if rows == None:
                return None
            else:
                nombre, primer_apellido, segundo_apellido, email = rows
                usuario = UsuariosVO(nombre, primer_apellido, segundo_apellido, email)
                return usuario
            
        except Exception as e:
            print(e)

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