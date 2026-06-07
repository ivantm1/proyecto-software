import datetime
from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.SancionVO import SancionVO

_TABLA_RETRASO = {1: 1, 2: 3, 3: 6, 4: 10}
_SANCION_MAX_RETRASO = 15

class SancionDaoJDBC(Conexion):
    SQL_INSERT       = "INSERT INTO Sanciones (email, tipo, estado, fecha_inicio, duracion) VALUES (?, ?, ?, ?, ?)"
    SQL_SELECT_EST   = "SELECT email, tipo, estado, fecha_inicio, duracion FROM Sanciones WHERE email = ? ORDER BY fecha_inicio ASC"
    SQL_ACTIVA       = "SELECT COUNT(*) FROM Sanciones WHERE email = ? AND estado = 'Activa'"
    SQL_DELETE       = "DELETE FROM Sanciones WHERE email = ? AND tipo = ? AND fecha_inicio = ? AND duracion = ?"
    SQL_PROMOVER     = ("SELECT TOP 1 tipo, fecha_inicio, duracion FROM Sanciones "
                        "WHERE email = ? AND estado = 'Pendiente' ORDER BY fecha_inicio ASC")
    SQL_ACTIVAR      = ("UPDATE Sanciones SET estado = 'Activa', fecha_inicio = ? "
                        "WHERE email = ? AND tipo = ? AND fecha_inicio = ? AND duracion = ?")

    def aplicarSancionRetraso(self, correo_estudiante, semanas_retraso):
        dias = _TABLA_RETRASO.get(semanas_retraso, _SANCION_MAX_RETRASO)
        return self._insertarSancion(correo_estudiante, "retraso", dias)

    def aplicarSancionDanio(self, correo_estudiante, tipo, dias_sancion=7):
        return self._insertarSancion(correo_estudiante, tipo, dias_sancion)

    def _insertarSancion(self, correo_estudiante, tipo, cantidad):
        cursor = self.getCursor()
        try:
            hoy = datetime.date.today()
            hoy_str = hoy.strftime('%Y-%m-%d')

            # Comprobar si ya existe una sanción activa
            cursor.execute(self.SQL_ACTIVA, (correo_estudiante,))
            tiene_activa = cursor.fetchone()[0] > 0

            estado = 'Pendiente' if tiene_activa else 'Activa'

            cursor.execute(self.SQL_INSERT, (correo_estudiante, tipo, estado, hoy_str, cantidad))
            self.conexion.commit()
            return SancionVO(correo_estudiante, tipo, cantidad, hoy, estado)
        except Exception as e:
            print(f"Error en _insertarSancion: {e}")
            return None

    def obtenerSancionesEstudiante(self, correo_estudiante):
        cursor = self.getCursor()
        sanciones = []
        try:
            cursor.execute(self.SQL_SELECT_EST, (correo_estudiante,))
            for row in cursor.fetchall():
                correo, tipo, estado, fecha_inicio, duracion = row
                sanciones.append(SancionVO(correo, tipo, duracion, fecha_inicio, estado))
        except Exception as e:
            print(f"Error en obtenerSancionesEstudiante: {e}")
        return sanciones

    def eliminarSancion(self, correo_estudiante, tipo, fecha_inicio, duracion):
        cursor = self.getCursor()
        try:
            # Averiguar si la que se elimina era Activa
            sql_estado = ("SELECT estado FROM Sanciones WHERE email = ? AND tipo = ? "
                          "AND fecha_inicio = ? AND duracion = ?")
            cursor.execute(sql_estado, (correo_estudiante, tipo, fecha_inicio, duracion))
            row = cursor.fetchone()
            era_activa = row and row[0] == 'Activa'

            cursor.execute(self.SQL_DELETE, (correo_estudiante, tipo, fecha_inicio, duracion))
            self.conexion.commit()

            if cursor.rowcount > 0 and era_activa:
                self.promoverSiguientePendiente(correo_estudiante)

            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error en eliminarSancion: {e}")
            return False

    def promoverSiguientePendiente(self, correo_estudiante):
        """Activa la sanción pendiente más antigua si no hay ninguna activa."""
        cursor = self.getCursor()
        try:
            # Verificar que no haya otra activa ya
            cursor.execute(self.SQL_ACTIVA, (correo_estudiante,))
            if cursor.fetchone()[0] > 0:
                return

            cursor.execute(self.SQL_PROMOVER, (correo_estudiante,))
            row = cursor.fetchone()
            if row is None:
                return

            tipo_p, fecha_inicio_p, duracion_p = row
            hoy_str = datetime.date.today().strftime('%Y-%m-%d')

            cursor.execute(
                self.SQL_ACTIVAR,
                (hoy_str, correo_estudiante, tipo_p, fecha_inicio_p, duracion_p)
            )
            self.conexion.commit()
        except Exception as e:
            print(f"Error en promoverSiguientePendiente: {e}")

    def tieneSancionActiva(self, correo_estudiante):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_ACTIVA, (correo_estudiante,))
            return cursor.fetchone()[0] > 0
        except Exception as e:
            print(f"Error en tieneSancionActiva: {e}")
            return False
