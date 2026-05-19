import datetime
from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.PrestamoVO import PrestamoVO
 
class PrestamoDaoJDBC(Conexion):
    SQL_REGISTRAR        = "INSERT INTO Prestamos (email, ISBN, estado, fecha_prestamo, fecha_devolucion, prorroga) VALUES (?, ?, 'Activo', ?, ?, 0)"
    SQL_DEVOLVER = "UPDATE Prestamos SET estado = 'Devuelto', fecha_devolucion = GETDATE() WHERE ISBN = ? AND (estado = 'Activo' OR estado = 'Vencido')"
    SQL_DATOS_PRESTAMO   = "SELECT p.ISBN, p.email, p.fecha_prestamo, p.fecha_devolucion, p.estado, p.prorroga FROM Prestamos p WHERE p.ISBN = ? AND p.estado = 'Activo'"
    SQL_PRESTAMO_ACTIVO_ISBN = SQL_DATOS_PRESTAMO
    SQL_PRORROGAR        = "UPDATE Prestamos SET fecha_devolucion = ?, prorroga = 1 WHERE ISBN = ? AND estado = 'Activo' AND prorroga = 0 AND NOT EXISTS (SELECT 1 FROM Reservas WHERE ISBN = ? AND estado = 'Pendiente')"
    SQL_CUENTA_PRESTAMOS = "SELECT COUNT(*) FROM Prestamos WHERE email = ? AND estado = 'Activo'"
    SQL_EXISTE_PRESTAMO_ACTIVO = "SELECT COUNT(*) FROM Prestamos WHERE email = ? AND ISBN = ? AND estado = 'Activo'"
    SQL_VERIFICAR_LIBRO_DISPONIBLE = "SELECT disponibilidad FROM Libros WHERE ISBN = ?"
    SQL_ACTUALIZAR_DISPONIBILIDAD_LIBRO = "UPDATE Libros SET disponibilidad = ? WHERE ISBN = ?"
 
                                                       
    SQL_MIS_PRESTAMOS = """
        SELECT p.ISBN, l.titulo, l.autor, l.nombre_tema, l.descripcion, p.fecha_devolucion, p.estado
        FROM Prestamos p
        JOIN Libros l ON p.ISBN = l.ISBN
        WHERE p.email = ? AND p.estado IN ('Activo', 'Vencido')
    """
 
    SQL_BUSCAR_PRESTAMOS = """
        SELECT p.ISBN, l.titulo, l.autor, l.nombre_tema, l.descripcion, p.fecha_devolucion, p.estado
        FROM Prestamos p
        JOIN Libros l ON p.ISBN = l.ISBN
        WHERE p.email = ? AND p.estado IN ('Activo', 'Vencido')
        AND l.titulo LIKE ?
    """
 
    SQL_BUSCAR_PRESTAMOS_TEMA = """
        SELECT p.ISBN, l.titulo, l.autor, l.nombre_tema, l.descripcion, p.fecha_devolucion, p.estado
        FROM Prestamos p
        JOIN Libros l ON p.ISBN = l.ISBN
        WHERE p.email = ? AND p.estado IN ('Activo', 'Vencido')
        AND l.titulo LIKE ?
        AND l.nombre_tema = ?
    """
    SQL_COOLDOWN = """
        SELECT COUNT(*) FROM Prestamos 
        WHERE email = ? AND ISBN = ? AND estado = 'Devuelto' 
        AND DATEADD(day, 7, fecha_devolucion) > GETDATE()
    """

    def registrarPrestamo(self, isbn, correo_estudiante):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_VERIFICAR_LIBRO_DISPONIBLE, (isbn,))
            disponibilidad = cursor.fetchone()
            if disponibilidad is None or disponibilidad[0] != 'Disponible':
                print(f"Error en registrarPrestamo: libro {isbn} no disponible")
                return None

            hoy = datetime.date.today()
            fecha_devolucion = hoy + datetime.timedelta(days=14)
            hoy_str = hoy.strftime('%Y-%m-%d')
            fecha_devolucion_str = fecha_devolucion.strftime('%Y-%m-%d')
            cursor.execute(self.SQL_REGISTRAR, (correo_estudiante, isbn, hoy_str, fecha_devolucion_str))
            cursor.execute(self.SQL_ACTUALIZAR_DISPONIBILIDAD_LIBRO, ('Prestado', isbn))
            self.conexion.commit()
            return PrestamoVO(isbn, correo_estudiante, hoy, fecha_devolucion, 'Activo')
        except Exception as e:
            print(f"Error en registrarPrestamo: {e}")
            return None
 
    def registrarDevolucion(self, isbn):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_DATOS_PRESTAMO, (isbn,))
            row = cursor.fetchone()
            if row is None:
                return False
            cursor.execute(self.SQL_DEVOLVER, (isbn,))
            cursor.execute(self.SQL_ACTUALIZAR_DISPONIBILIDAD_LIBRO, ('Disponible', isbn))
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error en registrarDevolucion: {e}")
            return False

    def buscarPrestamoActivoPorISBN(self, isbn):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_PRESTAMO_ACTIVO_ISBN, (isbn,))
            row = cursor.fetchone()
            if not row:
                return None
            isbn_libro, correo_estudiante, fecha_prestamo, fecha_devolucion, estado, prorroga = row
            return PrestamoVO(isbn_libro, correo_estudiante, fecha_prestamo, fecha_devolucion, estado)
        except Exception as e:
            print(f"Error en buscarPrestamoActivoPorISBN: {e}")
            return None
 
    def obtenerPrestamosEstudiante(self, correo_estudiante):
        cursor = self.getCursor()
        prestamos = []
        try:
            cursor.execute(self.SQL_MIS_PRESTAMOS, (correo_estudiante,))
            for row in cursor.fetchall():
                isbn, titulo, autor, tema, descripcion, fecha_devolucion, estado = row
                vo = PrestamoVO(isbn, correo_estudiante, None, fecha_devolucion, estado)
                vo._titulo     = titulo
                vo._autor      = autor
                vo._nombre_tema = tema
                vo._descripcion = descripcion
                prestamos.append(vo)
        except Exception as e:
            print(f"Error en obtenerPrestamosEstudiante: {e}")
        return prestamos
 
    def buscarPrestamosEstudiante(self, correo_estudiante, titulo='', tema='Ninguno'):
        cursor = self.getCursor()
        prestamos = []
        try:
            if tema != 'Ninguno':
                cursor.execute(self.SQL_BUSCAR_PRESTAMOS_TEMA, (correo_estudiante, f'%{titulo}%', tema))
            else:
                cursor.execute(self.SQL_BUSCAR_PRESTAMOS, (correo_estudiante, f'%{titulo}%'))
 
            for row in cursor.fetchall():
                isbn, titulo_libro, autor, tema_libro, descripcion, fecha_devolucion, estado = row
                vo = PrestamoVO(isbn, correo_estudiante, None, fecha_devolucion, estado)
                vo._titulo      = titulo_libro
                vo._autor       = autor
                vo._nombre_tema = tema_libro
                vo._descripcion = descripcion
                prestamos.append(vo)
        except Exception as e:
            print(f"Error en buscarPrestamosEstudiante: {e}")
        return prestamos
 
    def obtenerPrestamosProximos(self, correo_estudiante):
        limite = datetime.date.today() + datetime.timedelta(days=3)
        return [p for p in self.obtenerPrestamosEstudiante(correo_estudiante)
                if p.fecha_devolucion and p.fecha_devolucion <= limite]
 
    def prorrogarPrestamo(self, isbn):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_DATOS_PRESTAMO, (isbn,))
            row = cursor.fetchone()
            if row is None:
                return False
            _, _, _, fecha_devolucion, _, prorroga = row
            if prorroga:
                print("No se puede prorrogar: ya fue prorrogado.")
                return False

                                                   
            if isinstance(fecha_devolucion, str):
                fecha_devolucion = datetime.date.fromisoformat(fecha_devolucion[:10])

            nueva_fecha = fecha_devolucion + datetime.timedelta(days=7)
            nueva_fecha_str = nueva_fecha.strftime('%Y-%m-%d')
            cursor.execute(self.SQL_PRORROGAR, (nueva_fecha_str, isbn, isbn))
            if cursor.rowcount == 0:
                print("No se puede prorrogar: reserva activa.")
                return False
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error en prorrogarPrestamo: {e}")
            return False
 
    def contarPrestamosEstudiante(self, correo_estudiante):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_CUENTA_PRESTAMOS, (correo_estudiante,))
            return cursor.fetchone()[0]
        except Exception as e:
            print(f"Error en contarPrestamosEstudiante: {e}")
            return 0

    def tienePrestamoActivo(self, isbn, correo_estudiante):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_EXISTE_PRESTAMO_ACTIVO, (correo_estudiante, isbn))
            return cursor.fetchone()[0] > 0
        except Exception as e:
            print(f"Error en tienePrestamoActivo: {e}")
            return False
        
    def tieneCooldown(self, correo_estudiante, isbn):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_COOLDOWN, (correo_estudiante, isbn))
            return cursor.fetchone()[0] > 0
        except Exception as e:
            print(f"Error en tieneCooldown: {e}")
            return False
