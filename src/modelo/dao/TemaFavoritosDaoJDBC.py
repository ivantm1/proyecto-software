from src.modelo.conexion.Conexion import Conexion

class TemaFavoritosDaoJDBC(Conexion):
    SQL_INSERTAR = "INSERT INTO TemasFavoritos (email, nombre_tema) VALUES (?, ?)"
    SQL_ELIMINAR = "DELETE FROM TemasFavoritos WHERE email = ? AND nombre_tema = ?"
    SQL_OBTENER  = "SELECT nombre_tema FROM TemasFavoritos WHERE email = ?"
    SQL_EXISTE   = "SELECT COUNT(*) FROM TemasFavoritos WHERE email = ? AND nombre_tema = ?"

    def agregarFavorito(self, correo, nombre_tema):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_EXISTE, (correo, nombre_tema))
            if cursor.fetchone()[0] > 0:
                return False
            cursor.execute(self.SQL_INSERTAR, (correo, nombre_tema))
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error en agregarFavorito: {e}")
            return False

    def eliminarFavorito(self, correo, nombre_tema):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_ELIMINAR, (correo, nombre_tema))
            self.conexion.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error en eliminarFavorito: {e}")
            return False

    def obtenerFavoritos(self, correo):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_OBTENER, (correo,))
            return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error en obtenerFavoritos: {e}")
            return []