import datetime
from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.ReservaVO import ReservaVO

class ReservaDaoJDBC(Conexion):
    SQL_CREAR          = "UPDATE Libros SET correo_reserva = ?, fecha_reserva = ? WHERE isbn = ? AND correo_reserva IS NULL"
    SQL_CANCELAR       = "UPDATE Libros SET correo_reserva = NULL, fecha_reserva = NULL WHERE isbn = ?"
    SQL_RESERVAS_EST   = "SELECT isbn, correo_reserva, fecha_reserva FROM Libros WHERE correo_reserva = ?"
    SQL_RESERVA_LIBRO  = "SELECT correo_reserva, fecha_reserva FROM Libros WHERE isbn = ?"
    SQL_CUENTA_RESERVAS= "SELECT COUNT(*) FROM Libros WHERE correo_reserva = ?"

    # RF15 — crear reserva (solo si el libro no tiene ya otra reserva)
    def crearReserva(self, isbn, correo_estudiante):
        cursor = self.getCursor()
        try:
            hoy = datetime.date.today()
            cursor.execute(self.SQL_CREAR, (correo_estudiante, hoy, isbn))
            if cursor.rowcount == 0:
                print("No se puede reservar: el libro ya tiene una reserva activa.")
                return False
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error en crearReserva: {e}")
            return False

    # RF20 — cancelar reserva (libro devuelto a catálogo por expiración)
    def cancelarReserva(self, isbn):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_CANCELAR, (isbn,))
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error en cancelarReserva: {e}")
            return False

    # RF18 — reservas activas de un estudiante
    def obtenerReservasEstudiante(self, correo_estudiante):
        cursor = self.getCursor()
        reservas = []
        try:
            cursor.execute(self.SQL_RESERVAS_EST, (correo_estudiante,))
            for row in cursor.fetchall():
                isbn, correo, fecha_reserva = row
                reservas.append(ReservaVO(isbn, correo, fecha_reserva))
        except Exception as e:
            print(f"Error en obtenerReservasEstudiante: {e}")
        return reservas

    # RF17 — comprobar si un libro tiene reserva (se llama al devolver)
    def obtenerReservaPorLibro(self, isbn):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_RESERVA_LIBRO, (isbn,))
            row = cursor.fetchone()
            if row is None or row[0] is None:
                return None
            correo_reserva, fecha_reserva = row
            return ReservaVO(isbn, correo_reserva, fecha_reserva)
        except Exception as e:
            print(f"Error en obtenerReservaPorLibro: {e}")
            return None

    # RF16 — número de reservas activas de un estudiante
    def contarReservasEstudiante(self, correo_estudiante):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_CUENTA_RESERVAS, (correo_estudiante,))
            return cursor.fetchone()[0]
        except Exception as e:
            print(f"Error en contarReservasEstudiante: {e}")
            return 0

    # RF20 — devuelve True si la reserva lleva más de 7 días sin ser recogida
    def reservaExpirada(self, isbn):
        reserva = self.obtenerReservaPorLibro(isbn)
        if reserva is None:
            return False
        limite = reserva.fecha_reserva + datetime.timedelta(days=7)
        return datetime.date.today() > limite
