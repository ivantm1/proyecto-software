from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.LibroVO import LibroVO

class LibroDaoJDBC(Conexion):
    SQL_INSERT       = "INSERT INTO Libros (isbn, titulo, autores, tema, fecha_llegada, descripcion, estado) VALUES (?, ?, ?, ?, ?, ?, ?)"
    SQL_DELETE       = "DELETE FROM Libros WHERE isbn = ?"
    SQL_SELECT_ALL   = "SELECT ISBN, titulo, autor, fecha_llegada, num_copias, disponibilidad, descripcion, nombre_tema FROM Libros"
    SQL_SELECT_ISBN  = "SELECT isbn, titulo, autores, tema, fecha_llegada, descripcion, estado FROM Libros WHERE isbn = ?"
    SQL_SELECT_TITULO= "SELECT isbn, titulo, autores, tema, fecha_llegada, descripcion, estado FROM Libros WHERE titulo LIKE ?"
    SQL_SELECT_TEMA  = "SELECT isbn, titulo, autores, tema, fecha_llegada, descripcion, estado FROM Libros WHERE tema = ?"
    SQL_RESERVADOS   = "SELECT isbn, titulo, autores, tema, fecha_llegada, descripcion, estado FROM Libros WHERE estado = 'reserva'"
    SQL_CHECK_LIBRE  = "SELECT COUNT(*) FROM Libros WHERE isbn = ? AND estado = 'disponible'"

    def _fila_a_vo(self, row):
        ISBN, titulo, autor, fecha_llegada, num_copias, disponibilidad, descripcion, nombre_tema,  estado = row
        return LibroVO(ISBN, titulo, autor, fecha_llegada, num_copias, disponibilidad, descripcion, nombre_tema, estado)

    # RF01 — dar de alta un libro nuevo
    def altaLibro(self, libroVO):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_INSERT, (
                libroVO.isbn, libroVO.titulo, libroVO.autores, libroVO.tema,
                libroVO.fecha_llegada, libroVO.descripcion, libroVO.estado
            ))
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error en altaLibro: {e}")
            return False

    # RF03 — retirar libro (solo si no tiene préstamo activo ni reserva)
    def bajaLibro(self, isbn):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_CHECK_LIBRE, (isbn,))
            count = cursor.fetchone()[0]
            if count == 0:
                print("No se puede retirar: el libro tiene un préstamo activo o una reserva.")
                return False
            cursor.execute(self.SQL_DELETE, (isbn,))
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error en bajaLibro: {e}")
            return False

    # RF22 — buscar por título (estudiante)
    def buscarPorTitulo(self, titulo):
        cursor = self.getCursor()
        libros = []
        try:
            cursor.execute(self.SQL_SELECT_TITULO, (f"%{titulo}%",))
            for row in cursor.fetchall():
                libros.append(self._fila_a_vo(row))
        except Exception as e:
            print(f"Error en buscarPorTitulo: {e}")
        return libros

    def buscarLibros(self, titulo, tema):

        cursor = self.getCursor()
        libros_vo = [] # Aquí guardaremos la lista de objetos

        sql = "SELECT ISBN, titulo, autor, fecha_llegada, num_copias, disponibilidad, descripcion, nombre_tema FROM Libros WHERE titulo LIKE ?"
        params = [f"%{titulo}%"]

        if tema != "Ninguno":
            sql += " AND tema = ?"
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

    # RF22 — buscar por tema (estudiante)
    def buscarPorTema(self, tema):
        cursor = self.getCursor()
        libros = []
        try:
            cursor.execute(self.SQL_SELECT_TEMA, (tema,))
            for row in cursor.fetchall():
                libros.append(self._fila_a_vo(row))
        except Exception as e:
            print(f"Error en buscarPorTema: {e}")
        return libros

    # RF23 — catálogo completo (bibliotecario)
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
