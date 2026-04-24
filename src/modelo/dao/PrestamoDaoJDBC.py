import datetime
from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.PrestamoVO import PrestamoVO

class PrestamoDaoJDBC(Conexion):
    SQL_REGISTRAR        = "UPDATE Libros SET estado = 'prestamo', fecha_prestamo = ?, fecha_devolucion = ?, correo_prestamo = ? WHERE isbn = ?"
    SQL_DEVOLVER         = "UPDATE Libros SET estado = 'disponible', fecha_prestamo = NULL, fecha_devolucion = NULL, correo_prestamo = NULL WHERE isbn = ?"
    SQL_INSERTAR_HIST    = "INSERT INTO Historial (isbn_libro, correo_estudiante, fecha_prestamo, fecha_devolucion) VALUES (?, ?, ?, ?)"
    SQL_MIS_PRESTAMOS    = "SELECT isbn, correo_prestamo, fecha_prestamo, fecha_devolucion FROM Libros WHERE correo_prestamo = ?"
    SQL_DATOS_PRESTAMO   = "SELECT isbn, correo_prestamo, fecha_prestamo, fecha_devolucion FROM Libros WHERE isbn = ?"
    SQL_PRORROGAR        = "UPDATE Libros SET fecha_devolucion = ? WHERE isbn = ? AND correo_reserva IS NULL"
    SQL_CUENTA_PRESTAMOS = "SELECT COUNT(*) FROM Libros WHERE correo_prestamo = ?"

    # RF10 — registrar préstamo: estado='prestamo', plazo 14 días
    def registrarPrestamo(self, isbn, correo_estudiante):
        cursor = self.getCursor()
        try:
            hoy = datetime.date.today()
            fecha_devolucion = hoy + datetime.timedelta(days=14)
            cursor.execute(self.SQL_REGISTRAR, (hoy, fecha_devolucion, correo_estudiante, isbn))
            self.conexion.commit()
            return PrestamoVO(isbn, correo_estudiante, hoy, fecha_devolucion)
        except Exception as e:
            print(f"Error en registrarPrestamo: {e}")
            return None

    # RF11 — registrar devolución y guardar en historial
    def registrarDevolucion(self, isbn):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_DATOS_PRESTAMO, (isbn,))
            row = cursor.fetchone()
            if row is None:
                return False
            _, correo_estudiante, fecha_prestamo, fecha_devolucion = row
            cursor.execute(self.SQL_DEVOLVER, (isbn,))
            cursor.execute(self.SQL_INSERTAR_HIST, (isbn, correo_estudiante, fecha_prestamo, fecha_devolucion))
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error en registrarDevolucion: {e}")
            return False

    # RF14 — préstamos activos de un estudiante
    def obtenerPrestamosEstudiante(self, correo_estudiante):
        cursor = self.getCursor()
        prestamos = []
        try:
            cursor.execute(self.SQL_MIS_PRESTAMOS, (correo_estudiante,))
            for row in cursor.fetchall():
                isbn, correo, fecha_prestamo, fecha_devolucion = row
                prestamos.append(PrestamoVO(isbn, correo, fecha_prestamo, fecha_devolucion))
        except Exception as e:
            print(f"Error en obtenerPrestamosEstudiante: {e}")
        return prestamos

    # RF14 — préstamos a 3 días o menos de vencer
    def obtenerPrestamosProximos(self, correo_estudiante):
        limite = datetime.date.today() + datetime.timedelta(days=3)
        return [p for p in self.obtenerPrestamosEstudiante(correo_estudiante)
                if p.fecha_devolucion <= limite]

    # RF21 — prórroga de 7 días (solo si el libro no está reservado)
    def prorrogarPrestamo(self, isbn):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_DATOS_PRESTAMO, (isbn,))
            row = cursor.fetchone()
            if row is None:
                return False
            _, _, _, fecha_devolucion = row
            nueva_fecha = fecha_devolucion + datetime.timedelta(days=7)
            cursor.execute(self.SQL_PRORROGAR, (nueva_fecha, isbn))
            if cursor.rowcount == 0:
                print("No se puede prorrogar: el libro tiene una reserva activa.")
                return False
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error en prorrogarPrestamo: {e}")
            return False

    # RF06 — número de préstamos activos de un estudiante
    def contarPrestamosEstudiante(self, correo_estudiante):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_CUENTA_PRESTAMOS, (correo_estudiante,))
            return cursor.fetchone()[0]
        except Exception as e:
            print(f"Error en contarPrestamosEstudiante: {e}")
            return 0
