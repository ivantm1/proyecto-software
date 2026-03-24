from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.UsuariosVo import UsuariosVo

class UserDaoJBDC(Conexion):
    SQL_SELECT = "SELECT nombre, primer_apellido, segundo_apellido, email FROM Usuarios"
    SQL_INSERT = ""

    def select(self):
        cursor = self.getCursor()
        users = []

        try:
            cursor.execute(self.SQL_SELECT)
            rows = cursor.fetchall()

            for row in rows:
                nombre, primer_apellido, segundo_apellido, email = row
                usuario = UsuariosVo(nombre, primer_apellido, segundo_apellido, email)


        except Exception as e:
            print(e)

        return users