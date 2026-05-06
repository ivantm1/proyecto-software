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

    # JOIN con Libros para obtener título, autor y tema
    SQL_MIS_RESERVAS = """
        SELECT p.ISBN, l.titulo, l.autor, l.nombre_tema, l.descripcion, p.fecha_reserva, p.estado
        FROM Reservas p
        JOIN Libros l ON p.ISBN = l.ISBN
        WHERE p.email = ?
    """
 
    SQL_BUSCAR_RESERVAS = """
        SELECT p.ISBN, l.titulo, l.autor, l.nombre_tema, l.descripcion, p.fecha_reserva, p.estado
        FROM Reservas p
        JOIN Libros l ON p.ISBN = l.ISBN
        WHERE p.email = ?
        AND l.titulo LIKE ?
    """
 
    SQL_BUSCAR_RESERVAS_TEMA = """
        SELECT p.ISBN, l.titulo, l.autor, l.nombre_tema, l.descripcion, p.fecha_reserva, p.estado
        FROM Reservas p
        JOIN Libros l ON p.ISBN = l.ISBN
        WHERE p.email = ?
        AND l.titulo LIKE ?
        AND l.nombre_tema = ?
    """

    def crearReserva(self, isbn, correo_estudiante):
        cursor = self.getCursor()
        try:
            # Comprobar que no hay ya una reserva activa para ese libro
            cursor.execute(self.SQL_EXISTE, (isbn,))
            if cursor.fetchone()[0] > 0:
                print("No se puede reservar: el libro ya tiene una reserva activa.")
                return False

            # Comprobar que el estudiante no tenga más de 3 reservas activas
            if self.contarReservasEstudiante(correo_estudiante) >= 3:
                print("No se puede reservar: el estudiante ya tiene 3 reservas activas.")
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
            cursor.execute(self.SQL_MIS_RESERVAS, (correo_estudiante,))
            for row in cursor.fetchall():
                isbn, titulo, autor, tema, descripcion, fecha_reserva, estado = row
                vo = ReservaVO(isbn, correo_estudiante, fecha_reserva, estado)
                vo._titulo     = titulo
                vo._autor      = autor
                vo._nombre_tema = tema
                vo._descripcion = descripcion
                reservas.append(vo)
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
        
    def buscarReservasEstudiante(self, correo_estudiante, titulo='', tema='Ninguno'):
        cursor = self.getCursor()
        reservas = []
        try:
            if tema != 'Ninguno':
                cursor.execute(self.SQL_BUSCAR_RESERVAS_TEMA, (correo_estudiante, f'%{titulo}%', tema))
            else:
                cursor.execute(self.SQL_BUSCAR_RESERVAS, (correo_estudiante, f'%{titulo}%'))
 
            for row in cursor.fetchall():
                isbn, titulo_libro, autor, tema_libro, descripcion, fecha_reserva, estado = row
                vo = ReservaVO(isbn, correo_estudiante, fecha_reserva, estado)
                vo._titulo      = titulo_libro
                vo._autor       = autor
                vo._nombre_tema = tema_libro
                vo._descripcion = descripcion
                reservas.append(vo)
        except Exception as e:
            print(f"Error en buscarReservasEstudiante: {e}")
        return reservas

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