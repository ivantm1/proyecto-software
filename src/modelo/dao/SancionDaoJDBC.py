import datetime
from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.SancionVO import SancionVO

# Tabla progresiva de sanciones por retraso (Apéndice 4.2 del ERS)
_TABLA_RETRASO = {1: 1, 2: 3, 3: 6, 4: 10}
_SANCION_MAX_RETRASO = 15  # 5 o más semanas de retraso

class SancionDaoJDBC(Conexion):
    SQL_INSERT          = "INSERT INTO Sanciones (correo_estudiante, tipo, semanas_sancion, fecha_inicio) VALUES (?, ?, ?, ?)"
    SQL_SELECT_EST      = "SELECT correo_estudiante, tipo, semanas_sancion, fecha_inicio FROM Sanciones WHERE correo_estudiante = ?"
    SQL_SELECT_ACTIVAS  = "SELECT correo_estudiante, tipo, semanas_sancion, fecha_inicio FROM Sanciones WHERE correo_estudiante = ? AND fecha_fin > ?"

    # RF24 — sanción automática por retraso (se llama al detectar fecha_devolucion superada)
    def aplicarSancionRetraso(self, correo_estudiante, semanas_retraso):
        semanas = _TABLA_RETRASO.get(semanas_retraso, _SANCION_MAX_RETRASO)
        return self._insertarSancion(correo_estudiante, "retraso", semanas)

    # RF25 — sanción manual por daño, el bibliotecario elige las semanas
    def aplicarSancionDanio(self, correo_estudiante, semanas_sancion=3):
        return self._insertarSancion(correo_estudiante, "danio", semanas_sancion)

    def _insertarSancion(self, correo_estudiante, tipo, semanas):
        cursor = self.getCursor()
        try:
            hoy = datetime.date.today()
            cursor.execute(self.SQL_INSERT, (correo_estudiante, tipo, semanas, hoy))
            self.conexion.commit()
            return SancionVO(correo_estudiante, tipo, semanas, hoy)
        except Exception as e:
            print(f"Error en _insertarSancion: {e}")
            return None

    # Consultar todas las sanciones de un estudiante
    def obtenerSancionesEstudiante(self, correo_estudiante):
        cursor = self.getCursor()
        sanciones = []
        try:
            cursor.execute(self.SQL_SELECT_EST, (correo_estudiante,))
            for row in cursor.fetchall():
                correo, tipo, semanas, fecha_inicio = row
                sanciones.append(SancionVO(correo, tipo, semanas, fecha_inicio))
        except Exception as e:
            print(f"Error en obtenerSancionesEstudiante: {e}")
        return sanciones

    # Comprobar si un estudiante tiene alguna sanción aún activa
    def tieneSancionActiva(self, correo_estudiante):
        hoy = datetime.date.today()
        for s in self.obtenerSancionesEstudiante(correo_estudiante):
            fecha_fin = s.fecha_inicio + datetime.timedelta(weeks=s.semanas_sancion)
            if fecha_fin > hoy:
                return True
        return False
