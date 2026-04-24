from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.RegistroVO import RegistroVO
from src.modelo.vo.UsuariosVO import UsuariosVO

class UserDaoJDBC(Conexion):
    SQL_SELECT = "SELECT nombre, primer_apellido, segundo_apellido, correo, tipo FROM Usuarios"
    SQL_CHECK_LOGIN = "SELECT nombre, primer_apellido, segundo_apellido, correo, tipo FROM Usuarios WHERE correo = ? AND contrasena = ?"
    SQL_REGISTRO = "INSERT INTO Usuarios (nombre, apellidos, correo, contrasena) VALUES (?, ?, ?, ?)"

    def comprobarLogin(self, loginVO):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_CHECK_LOGIN, (loginVO.nombre, loginVO.contrasena))
            row = cursor.fetchone()
            if row is None:
                return None
            nombre_user, first_name, full_name, correo, tipo = row
            return UsuariosVO(nombre_user, first_name, full_name, correo, tipo)
        except Exception as e:
            print(f"Error en el login: {e}")
            return None

    def registrarUsuario(self, registroVO):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_REGISTRO, (registroVO.nombre, registroVO.apellidos, registroVO.correo, registroVO.contrasena))
            self.conexion.commit()
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
                nombre, primer_apellido, segundo_apellido, correo, tipo = row
                usuario = UsuariosVO(nombre, primer_apellido, segundo_apellido, correo, tipo)
                users.append(usuario)
        except Exception as e:
            print(e)
        return users
