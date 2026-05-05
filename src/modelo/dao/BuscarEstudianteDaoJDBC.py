from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.UsuarioVO import UsuarioVO

class BuscarEstudianteDaoJDBC(Conexion):
    SQL_BUSCAR_ESTUDIANTE = "SELECT nombre, apellidos, email, contrasena, tipo FROM Usuarios WHERE email = ? AND tipo = 'Estudiante'"

    def _fila_a_vo(self, row):
        nombre, apellidos, email, contrasena, tipo = row
        return UsuarioVO(nombre, apellidos, email, contrasena, tipo)

    def buscarEstudiante(self, correo):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_BUSCAR_ESTUDIANTE, (correo,))
            row = cursor.fetchone()
            if row is None:
                return None
            return self._fila_a_vo(row)
        except Exception as e:
            print(f"Error al buscar estudiante: {e}")
            return None