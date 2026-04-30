import datetime
from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.ReservaVO import ReservaVO

class ReservaDaoJDBC(Conexion):
    SQL_CREAR           = "INSERT INTO Reservas (email, ISBN, fecha_reserva) VALUES (?, ?, ?)"
    SQL_CANCELAR        = "UPDATE Reservas SET estado = 'Cumplida' WHERE ISBN = ? AND estado = 'Pendiente'"
    SQL_RESERVAS_EST    = "SELECT ISBN, email, fecha_reserva FROM Reservas WHERE email = ? AND estado = 'Pendiente'"
    SQL_RESERVA_LIBRO   = "SELECT email, fecha_reserva FROM Reservas WHERE ISBN = ? AND estado = 'Pendiente'"
    SQL_CUENTA_RESERVAS = "SELECT COUNT(*) FROM Reservas WHERE email = ? AND estado = 'Pendiente'"
    SQL_EXISTE          = "SELECT COUNT(*) FROM Reservas WHERE ISBN = ? AND estado = 'Pendiente'"

    def crearReserva(self, isbn, correo_estudiante):
        cursor = self.getCursor()
        try:
            # Comprobar que no hay ya una reserva activa para ese libro
            cursor.execute(self.SQL_EXISTE, (isbn,))
            if cursor.fetchone()[0] > 0:
                print("No se puede reservar: el libro ya tiene una reserva activa.")
                return False

            hoy = datetime.date.today().strftime('%Y-%m-%d')
            cursor.execute(self.SQL_CREAR, (correo_estudiante, isbn, hoy))
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error en crearReserva: {e}")
            return False

    def cancelarReserva(self, isbn):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_CANCELAR, (isbn,))
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error en cancelarReserva: {e}")
            return False

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

    def obtenerReservaPorLibro(self, isbn):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_RESERVA_LIBRO, (isbn,))
            row = cursor.fetchone()
            if row is None:
                return None
            correo, fecha_reserva = row
            return ReservaVO(isbn, correo, fecha_reserva)
        except Exception as e:
            print(f"Error en obtenerReservaPorLibro: {e}")
            return None

    def contarReservasEstudiante(self, correo_estudiante):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_CUENTA_RESERVAS, (correo_estudiante,))
            return cursor.fetchone()[0]
        except Exception as e:
            print(f"Error en contarReservasEstudiante: {e}")
            return 0

    def reservaExpirada(self, isbn):
        reserva = self.obtenerReservaPorLibro(isbn)
        if reserva is None:
            return False
        if isinstance(reserva.fecha_reserva, str):
            fecha = datetime.date.fromisoformat(reserva.fecha_reserva[:10])
        else:
            fecha = reserva.fecha_reserva
        limite = fecha + datetime.timedelta(days=7)
        return datetime.date.today() > limite