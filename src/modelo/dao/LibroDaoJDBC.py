from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.LibroVO import LibroVO

class LibroDaoJDBC(Conexion):
    SQL_INSERT = """
        INSERT INTO Libros (
            isbn, titulo, autor, fecha_llegada, num_copias, 
            disponibilidad, descripcion, nombre_tema, estado
        ) VALUES (?, ?, ?, ?, 1, ?, ?, ?, 'disponible')
    """

    SQL_DELETE = "DELETE FROM Libros WHERE isbn = ?"

    def _fila_a_vo(self, row):
        isbn, titulo, autor, fecha_llegada, num_copias, disponibilidad, descripcion, nombre_tema = row
        return LibroVO(isbn, titulo, autor, fecha_llegada, num_copias, disponibilidad, descripcion, nombre_tema)

    # RF01 — dar de alta un libro nuevo
    def altaLibro(self, libroVO):
        cursor = self.getCursor()
        try:
            datos = (
                libroVO.isbn, 
                libroVO.titulo, 
                libroVO.autor, 
                libroVO.fecha_llegada, 
                libroVO.disponibilidad, 
                libroVO.descripcion, 
                libroVO.nombre_tema
            )
            
            cursor.execute(self.SQL_INSERT, datos)
            self.conexion.commit()
            return True
            
        except Exception as e:
            self.conexion.rollback() 
            print(f"Error en altaLibro (DAO): {e}")
            return False

    def bajaLibro(self, isbn):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_CHECK_LIBRE, (isbn,))
            resultado = cursor.fetchone()
            
            # Si el conteo es 0, significa que el libro no existe o está ocupado
            if resultado[0] == 0:
                print(f"No se puede eliminar el ISBN {isbn}: El libro está prestado, reservado o no existe.")
                return False

            # 2. Si pasó la validación, procedemos a borrar
            cursor.execute(self.SQL_DELETE, (isbn,))
            
            # 3. Confirmamos la operación
            self.conexion.commit()
            print(f"Libro con ISBN {isbn} eliminado correctamente.")
            return True

        except Exception as e:
            # En caso de error de base de datos, deshacemos cambios
            self.conexion.rollback()
            print(f"Error en bajaLibro (DAO): {e}")
            return False


    def buscarLibros(self, titulo, tema):

        cursor = self.getCursor()
        libros_vo = [] # Aquí guardaremos la lista de objetos

        titulo_like = f"%{titulo}%"

        sql = "SELECT ISBN, titulo, autor, fecha_llegada, num_copias, disponibilidad, descripcion, nombre_tema FROM Libros WHERE titulo LIKE ?"
        params = [titulo_like]

        if tema != "Ninguno":
            sql += " AND nombre_tema = ?"
            params.append(tema)

        try:
            cursor.execute(sql, params)
            filas = cursor.fetchall()

            for row in filas:
                nuevo_libro = self._fila_a_vo(row)
                libros_vo.append(nuevo_libro)

        except Exception as e:
            print(f"Error en buscarLibros (DAO): {e}")
            
        return libros_vo





    # RF23 — solo libros en reserva (bibliotecario)
    def obtenerReservados(self):
        cursor = self.getCursor()
        libros = []
        try:
            cursor.execute(self.SQL_RESERVADOS)
            for row in cursor.fetchall():
                libros.append(self._fila_a_vo(row))
        except Exception as e:
            print(f"Error en obtenerReservados: {e}")
        return libros

    # Utilidad interna usada por otros DAOs
    def buscarPorISBN(self, isbn):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_SELECT_ISBN, (isbn,))
            row = cursor.fetchone()
            return self._fila_a_vo(row) if row else None
        except Exception as e:
            print(f"Error en buscarPorISBN: {e}")
            return None
