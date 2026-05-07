from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.LibroVO import LibroVO

class LibroDaoJDBC(Conexion):
    SQL_SELECT_ALL = """
    SELECT l.ISBN, l.titulo, l.autor, l.fecha_llegada, l.num_copias, 
           l.disponibilidad, l.descripcion, l.nombre_tema,
           p.fecha_devolucion
    FROM Libros l
    LEFT JOIN Prestamos p ON l.ISBN = p.ISBN AND p.estado = 'Activo'
    """
    SQL_SELECT_ISBN = "SELECT ISBN, titulo, autor, fecha_llegada, num_copias, disponibilidad, descripcion, nombre_tema FROM Libros WHERE ISBN = ?"
    SQL_RESERVADOS  = "SELECT l.ISBN, l.titulo, l.autor, l.fecha_llegada, l.num_copias, l.disponibilidad, l.descripcion, l.nombre_tema FROM Libros l JOIN Reservas r ON l.ISBN = r.ISBN WHERE r.estado = 'Pendiente'"
    SQL_CHECK_LIBRE = "SELECT COUNT(*) FROM Libros WHERE ISBN = ? AND disponibilidad = 'Disponible'"
    SQL_INSERT = """
        INSERT INTO Libros (ISBN, titulo, autor, fecha_llegada, num_copias, disponibilidad, descripcion, nombre_tema)
        VALUES (?, ?, ?, ?, 1, 'Disponible', ?, ?)
    """
    SQL_DELETE = "DELETE FROM Libros WHERE ISBN = ?"
    SQL_RESTAURAR = "UPDATE Libros SET disponibilidad = 'Disponible' WHERE ISBN = ?"
    SQL_DELETE_RETIRADO = "DELETE FROM Retirados WHERE ISBN = ?"
    SQL_MARCAR_RETIRADO = "UPDATE Libros SET disponibilidad = 'Retirado' WHERE ISBN = ?"
    SQL_INSERT_RETIRADO = "INSERT INTO Retirados (ISBN, motivo) VALUES (?, ?)"

    def _fila_a_vo(self, row):
        if len(row) == 9:
            isbn, titulo, autor, fecha_llegada, num_copias, disponibilidad, descripcion, nombre_tema, fecha_devolucion = row
        else:
            isbn, titulo, autor, fecha_llegada, num_copias, disponibilidad, descripcion, nombre_tema = row
            fecha_devolucion = None
        vo = LibroVO(isbn, titulo, autor, fecha_llegada, num_copias, disponibilidad, descripcion, nombre_tema)
        vo._fecha_devolucion = fecha_devolucion
        return vo

    def obtenerCatalogo(self):
        cursor = self.getCursor()
        libros = []
        try:
            cursor.execute(self.SQL_SELECT_ALL)
            for row in cursor.fetchall():
                libros.append(self._fila_a_vo(row))
        except Exception as e:
            print(f"Error en obtenerCatalogo: {e}")
        return libros

    def buscarLibros(self, titulo, tema):
        cursor = self.getCursor()
        libros_vo = []
        titulo_like = f"%{titulo}%"
        sql = """
            SELECT l.ISBN, l.titulo, l.autor, l.fecha_llegada, l.num_copias, 
                l.disponibilidad, l.descripcion, l.nombre_tema,
                p.fecha_devolucion
            FROM Libros l
            LEFT JOIN Prestamos p ON l.ISBN = p.ISBN AND p.estado = 'Activo'
            WHERE l.titulo LIKE ?
        """
        params = [titulo_like]
        if tema != "Ninguno":
            sql += " AND l.nombre_tema = ?"
            params.append(tema)
        try:
            cursor.execute(sql, params)
            for row in cursor.fetchall():
                libros_vo.append(self._fila_a_vo(row))
        except Exception as e:
            print(f"Error en buscarLibros (DAO): {e}")
        return libros_vo

    def altaLibro(self, libroVO):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_INSERT, (
                libroVO.isbn,
                libroVO.titulo,
                libroVO.autor,
                libroVO.fecha_llegada,
                libroVO.descripcion,
                libroVO.nombre_tema
            ))
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error en altaLibro (DAO): {e}")
            return False

    def bajaLibro(self, isbn, motivo="Retirado por el bibliotecario"):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_CHECK_LIBRE, (isbn,))
            if cursor.fetchone()[0] == 0:
                print(f"No se puede retirar {isbn}: está prestado, reservado o no existe.")
                return False
            cursor.execute(self.SQL_MARCAR_RETIRADO, (isbn,))
            cursor.execute(self.SQL_INSERT_RETIRADO, (isbn, motivo))
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error en bajaLibro (DAO): {e}")
            return False

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

    def buscarPorISBN(self, isbn):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_SELECT_ISBN, (isbn,))
            row = cursor.fetchone()
            return self._fila_a_vo(row) if row else None
        except Exception as e:
            print(f"Error en buscarPorISBN: {e}")
            return None
        
    def restaurarLibro(self, isbn):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_RESTAURAR, (isbn,))
            cursor.execute(self.SQL_DELETE_RETIRADO, (isbn,))
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error en restaurarLibro: {e}")
            return False