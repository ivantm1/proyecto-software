import datetime
from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.SancionVO import SancionVO

_TABLA_RETRASO = {1: 1, 2: 3, 3: 6, 4: 10}
_SANCION_MAX_RETRASO = 15

class SancionDaoJDBC(Conexion):
    SQL_INSERT     = "INSERT INTO Sanciones (email, tipo, estado, fecha_inicio, duracion) VALUES (?, ?, 'Activa', ?, ?)"
    SQL_SELECT_EST = "SELECT email, tipo, estado, fecha_inicio, duracion FROM Sanciones WHERE email = ?"
    SQL_ACTIVA     = "SELECT COUNT(*) FROM Sanciones WHERE email = ? AND estado = 'Activa' AND DATEADD(day, duracion, fecha_inicio) > ?"

    def aplicarSancionRetraso(self, correo_estudiante, semanas_retraso):
        semanas = _TABLA_RETRASO.get(semanas_retraso, _SANCION_MAX_RETRASO)
        return self._insertarSancion(correo_estudiante, "retraso", semanas, unidad='weeks')

    def aplicarSancionDanio(self, correo_estudiante, tipo, dias_sancion=7):
        return self._insertarSancion(correo_estudiante, tipo, dias_sancion, unidad='days')

    def _insertarSancion(self, correo_estudiante, tipo, cantidad, unidad='weeks'):
        cursor = self.getCursor()
        try:
            hoy = datetime.date.today()
            if unidad == 'days':
                fecha_fin = hoy + datetime.timedelta(days=cantidad)
            else:
                fecha_fin = hoy + datetime.timedelta(weeks=cantidad)
            hoy_str      = hoy.strftime('%Y-%m-%d')
            fecha_fin_str = fecha_fin.strftime('%Y-%m-%d')
            cursor.execute(self.SQL_INSERT, (correo_estudiante, tipo, hoy_str, cantidad))
            self.conexion.commit()
            return SancionVO(correo_estudiante, tipo, cantidad, hoy, "Activa")
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

    def tieneSancionActiva(self, correo_estudiante):
        cursor = self.getCursor()
        try:
            hoy_str = datetime.date.today().strftime('%Y-%m-%d')
            cursor.execute(self.SQL_ACTIVA, (correo_estudiante, hoy_str))
            return cursor.fetchone()[0] > 0
        except Exception as e:
            print(f"Error en tieneSancionActiva: {e}")
            return False