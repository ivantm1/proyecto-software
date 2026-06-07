import datetime
from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.ReservaVO import ReservaVO
from src.modelo.dao.LibroDaoJDBC import LibroDaoJDBC

class ReservaDaoJDBC(Conexion):
    SQL_CREAR           = "INSERT INTO Reservas (email, ISBN, fecha_reserva) VALUES (?, ?, ?)"
    SQL_CANCELAR        = "DELETE FROM Reservas WHERE ISBN = ? AND estado = 'Pendiente'"
    SQL_CANCELAR_CADUCADA = "DELETE FROM Reservas WHERE ISBN = ? AND estado = 'Caducada'"
    SQL_RESERVAS_EST    = "SELECT ISBN, email, fecha_reserva FROM Reservas WHERE email = ? AND estado = 'Pendiente'"
    SQL_RESERVA_LIBRO   = "SELECT email, fecha_reserva FROM Reservas WHERE ISBN = ? AND estado = 'Pendiente'"
    SQL_CUENTA_RESERVAS = "SELECT COUNT(*) FROM Reservas WHERE email = ? AND estado IN ('Pendiente', 'Espera')"
    SQL_EXISTE          = "SELECT COUNT(*) FROM Reservas WHERE ISBN = ? AND estado = 'Pendiente'"
    SQL_MARCAR_DISPONIBLE = "UPDATE Reservas SET fecha_reserva = ? WHERE ISBN = ? AND estado = 'Pendiente'"
    SQL_MARCAR_ESPERA   = "UPDATE Reservas SET estado = 'Espera', fecha_reserva = ? WHERE ISBN = ? AND estado = 'Pendiente'"
    SQL_CUMPLIR_ESPERA  = "DELETE FROM Reservas WHERE ISBN = ? AND estado = 'Espera'"
    SQL_CADUCAR_PENDIENTE = "UPDATE Reservas SET estado = 'Caducada' WHERE ISBN = ? AND estado = 'Pendiente'"
    SQL_CADUCAR_ESPERA = "UPDATE Reservas SET estado = 'Caducada' WHERE ISBN = ? AND estado = 'Espera'"
    SQL_RESERVA_EN_ESPERA = "SELECT email, fecha_reserva FROM Reservas WHERE ISBN = ? AND estado = 'Espera'"
    SQL_ESPERA_EXPIRADA = "SELECT COUNT(*) FROM Reservas WHERE ISBN = ? AND estado = 'Espera' AND DATEADD(day, 7, fecha_reserva) < GETDATE()"
    SQL_TODAS_RESERVAS = """
        SELECT p.ISBN, l.titulo, l.autor, l.nombre_tema, l.descripcion, p.fecha_reserva, p.estado, p.email
        FROM Reservas p
        JOIN Libros l ON p.ISBN = l.ISBN
    """


                                                       
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
        AND l.titulo COLLATE Latin1_General_CI_AI LIKE ? COLLATE Latin1_General_CI_AI
    """
 
    SQL_BUSCAR_RESERVAS_TEMA = """
        SELECT p.ISBN, l.titulo, l.autor, l.nombre_tema, l.descripcion, p.fecha_reserva, p.estado
        FROM Reservas p
        JOIN Libros l ON p.ISBN = l.ISBN
        WHERE p.email = ?
        AND l.titulo COLLATE Latin1_General_CI_AI LIKE ? COLLATE Latin1_General_CI_AI
        AND l.nombre_tema = ?
    """

    def crearReserva(self, isbn, correo_estudiante):
        cursor = self.getCursor()
        try:
                                                                       
            cursor.execute(self.SQL_EXISTE, (isbn,))
            if cursor.fetchone()[0] > 0:
                print("No se puede reservar: el libro ya tiene una reserva activa.")
                return False

                                                                            
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
            # Restaurar disponibilidad del libro al cancelar la reserva
            try:
                LibroDaoJDBC().restaurarLibro(isbn)
            except Exception:
                pass
            return True
        except Exception as e:
            print(f"Error en cancelarReserva: {e}")
            return False

    def cancelarReservaCaducada(self, isbn):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_CANCELAR_CADUCADA, (isbn,))
            self.conexion.commit()
            try:
                LibroDaoJDBC().restaurarLibro(isbn)
            except Exception:
                pass
            return True
        except Exception as e:
            print(f"Error en cancelarReservaCaducada: {e}")
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

    def marcarReservaEspera(self, isbn):
        cursor = self.getCursor()
        try:
            hoy = datetime.date.today().strftime('%Y-%m-%d')
            cursor.execute(self.SQL_MARCAR_ESPERA, (hoy, isbn))
            self.conexion.commit()
            # marcar el libro como reservado para que no pueda prestarse a otros
            try:
                LibroDaoJDBC().actualizarDisponibilidad(isbn, 'Reservado')
            except Exception:
                pass
            return True
        except Exception as e:
            print(f"Error en marcarReservaEspera: {e}")
            return False

    def cumplirReservaEspera(self, isbn):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_CUMPLIR_ESPERA, (isbn,))
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error en cumplirReservaEspera: {e}")
            return False

    def caducarReservaPendiente(self, isbn):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_CADUCAR_PENDIENTE, (isbn,))
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error en caducarReservaPendiente: {e}")
            return False

    def caducarReservaEspera(self, isbn):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_CADUCAR_ESPERA, (isbn,))
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error en caducarReservaEspera: {e}")
            return False

    def obtenerReservaEnEspera(self, isbn):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_RESERVA_EN_ESPERA, (isbn,))
            row = cursor.fetchone()
            if row is None:
                return None
            correo, fecha_reserva = row
            return ReservaVO(isbn, correo, fecha_reserva, 'Espera')
        except Exception as e:
            print(f"Error en obtenerReservaEnEspera: {e}")
            return None

    def esperaExpirada(self, isbn):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_ESPERA_EXPIRADA, (isbn,))
            return cursor.fetchone()[0] > 0
        except Exception as e:
            print(f"Error en esperaExpirada: {e}")
            return False

    def obtenerTodasReservas(self):
        cursor = self.getCursor()
        reservas = []
        try:
            cursor.execute(self.SQL_TODAS_RESERVAS)
            for row in cursor.fetchall():
                isbn, titulo, autor, tema, descripcion, fecha_reserva, estado, correo = row
                vo = ReservaVO(isbn, correo, fecha_reserva, estado)
                vo._titulo      = titulo
                vo._autor       = autor
                vo._nombre_tema = tema
                vo._descripcion = descripcion
                reservas.append(vo)
        except Exception as e:
            print(f"Error en obtenerTodasReservas: {e}")
        return reservas

    def marcarReservaDisponible(self, isbn):
        cursor = self.getCursor()
        try:
            hoy = datetime.date.today().strftime('%Y-%m-%d')
            cursor.execute(self.SQL_MARCAR_DISPONIBLE, (hoy, isbn))
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error en marcarReservaDisponible: {e}")
            return False