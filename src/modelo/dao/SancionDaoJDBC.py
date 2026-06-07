import datetime
from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.SancionVO import SancionVO

_TABLA_RETRASO = {1: 1, 2: 3, 3: 6, 4: 10}
_SANCION_MAX_RETRASO = 15

class SancionDaoJDBC(Conexion):
    SQL_INSERT     = "INSERT INTO Sanciones (email, tipo, estado, fecha_inicio, duracion) VALUES (?, ?, ?, ?, ?)"
    SQL_SELECT_EST = "SELECT email, tipo, estado, fecha_inicio, duracion FROM Sanciones WHERE email = ? ORDER BY fecha_inicio ASC"
    SQL_ACTIVA     = "SELECT COUNT(*) FROM Sanciones WHERE email = ? AND estado = 'Activa'"
    SQL_DELETE     = "DELETE FROM Sanciones WHERE email = ? AND tipo = ? AND fecha_inicio = ? AND duracion = ?"
    SQL_PROMOVER   = ("SELECT TOP 1 ID_sancion, tipo, fecha_inicio, duracion FROM Sanciones "
                      "WHERE email = ? AND estado = 'Pendiente' ORDER BY fecha_inicio ASC")
    SQL_ACTIVAR    = ("UPDATE Sanciones SET estado = 'Activa', fecha_inicio = ? "
                      "WHERE ID_sancion = ?")
    SQL_CUMPLIR    = ("UPDATE Sanciones SET estado = 'Cumplida' "
                      "WHERE email = ? AND estado = 'Activa' "
                      "AND DATEADD(day, duracion, fecha_inicio) <= ?")

    def aplicarSancionRetraso(self, correo_estudiante, semanas_retraso):
        dias = _TABLA_RETRASO.get(semanas_retraso, _SANCION_MAX_RETRASO)
        return self._insertarSancion(correo_estudiante, "retraso", dias)

    def aplicarSancionDanio(self, correo_estudiante, tipo, dias_sancion=7):
        return self._insertarSancion(correo_estudiante, tipo, dias_sancion)

    def actualizarEstadoSanciones(self, correo_estudiante):
        try:
            hoy_str = datetime.date.today().strftime('%Y-%m-%d')

            # 1. Marcar activas vencidas como Cumplidas
            cursor_cumplir = self.getCursor()
            cursor_cumplir.execute(self.SQL_CUMPLIR, (correo_estudiante, hoy_str))
            vencidas = cursor_cumplir.rowcount
            self.conexion.commit()
            cursor_cumplir.close()

            # 2. Intentar promover la siguiente pendiente siempre (promoverSiguientePendiente comprueba si ya hay activa)
            self.promoverSiguientePendiente(correo_estudiante)

        except Exception as e:
            print(f"Error en actualizarEstadoSanciones: {e}")

    def _insertarSancion(self, correo_estudiante, tipo, cantidad):
        try:
            self.actualizarEstadoSanciones(correo_estudiante)

            hoy = datetime.date.today()
            hoy_str = hoy.strftime('%Y-%m-%d')

            cursor_check = self.getCursor()
            cursor_check.execute(self.SQL_ACTIVA, (correo_estudiante,))
            tiene_activa = cursor_check.fetchone()[0] > 0
            cursor_check.close()

            estado = 'Pendiente' if tiene_activa else 'Activa'

            cursor_insert = self.getCursor()
            cursor_insert.execute(self.SQL_INSERT, (correo_estudiante, tipo, estado, hoy_str, cantidad))
            self.conexion.commit()
            cursor_insert.close()

            return SancionVO(correo_estudiante, tipo, cantidad, hoy, estado)
        except Exception as e:
            print(f"Error en _insertarSancion: {e}")
            return None

    def obtenerSancionesEstudiante(self, correo_estudiante):
        self.actualizarEstadoSanciones(correo_estudiante)
        sanciones = []
        try:
            cursor = self.getCursor()
            cursor.execute(self.SQL_SELECT_EST, (correo_estudiante,))
            for row in cursor.fetchall():
                correo, tipo, estado, fecha_inicio, duracion = row
                sanciones.append(SancionVO(correo, tipo, duracion, fecha_inicio, estado))
            cursor.close()
        except Exception as e:
            print(f"Error en obtenerSancionesEstudiante: {e}")
        return sanciones

    def eliminarSancion(self, correo_estudiante, tipo, fecha_inicio, duracion):
        try:
            sql_estado = ("SELECT estado FROM Sanciones WHERE email = ? AND tipo = ? "
                          "AND fecha_inicio = ? AND duracion = ?")
            cursor_check = self.getCursor()
            cursor_check.execute(sql_estado, (correo_estudiante, tipo, fecha_inicio, duracion))
            row = cursor_check.fetchone()
            era_activa = row and row[0] == 'Activa'
            cursor_check.close()

            cursor_del = self.getCursor()
            cursor_del.execute(self.SQL_DELETE, (correo_estudiante, tipo, fecha_inicio, duracion))
            self.conexion.commit()
            eliminado = cursor_del.rowcount > 0
            cursor_del.close()

            if eliminado and era_activa:
                self.promoverSiguientePendiente(correo_estudiante)

            return eliminado
        except Exception as e:
            print(f"Error en eliminarSancion: {e}")
            return False

    def promoverSiguientePendiente(self, correo_estudiante):
        try:
            # Verificar que no haya activa
            cursor_check = self.getCursor()
            cursor_check.execute(self.SQL_ACTIVA, (correo_estudiante,))
            hay_activa = cursor_check.fetchone()[0] > 0
            cursor_check.close()

            if hay_activa:
                return

            # Buscar la siguiente pendiente
            cursor_prom = self.getCursor()
            cursor_prom.execute(self.SQL_PROMOVER, (correo_estudiante,))
            row = cursor_prom.fetchone()
            cursor_prom.close()

            if row is None:
                return

            id_p, tipo_p, fecha_inicio_p, duracion_p = row

            # Calcular fecha_inicio encadenada desde la última cumplida
            sql_ultima_cumplida = ("SELECT TOP 1 fecha_inicio, duracion FROM Sanciones "
                                   "WHERE email = ? AND estado = 'Cumplida' "
                                   "ORDER BY DATEADD(day, duracion, fecha_inicio) DESC")
            cursor_ult = self.getCursor()
            cursor_ult.execute(sql_ultima_cumplida, (correo_estudiante,))
            ult = cursor_ult.fetchone()
            cursor_ult.close()

            if ult:
                fi, dur = ult
                if isinstance(fi, str):
                    fi = datetime.date.fromisoformat(fi[:10])
                elif hasattr(fi, 'toordinal'):
                    # Por si jaydebeapi devuelve un objeto fecha Java
                    fi = datetime.date.fromisoformat(str(fi)[:10])
                nueva_fecha_inicio = fi + datetime.timedelta(days=int(dur))
            else:
                nueva_fecha_inicio = datetime.date.today()

            nueva_fecha_str = nueva_fecha_inicio.strftime('%Y-%m-%d')

            cursor_act = self.getCursor()
            cursor_act.execute(self.SQL_ACTIVAR,
                               (nueva_fecha_str, id_p))
            self.conexion.commit()
            cursor_act.close()

            # Recursivo: si la recién activada también ya venció, repetir
            hoy_str = datetime.date.today().strftime('%Y-%m-%d')
            cursor_cumplir = self.getCursor()
            cursor_cumplir.execute(self.SQL_CUMPLIR, (correo_estudiante, hoy_str))
            hubo_vencidas = cursor_cumplir.rowcount > 0
            self.conexion.commit()
            cursor_cumplir.close()

            if hubo_vencidas:
                self.promoverSiguientePendiente(correo_estudiante)

        except Exception as e:
            print(f"Error en promoverSiguientePendiente: {e}")

    def tieneSancionActiva(self, correo_estudiante):
        self.actualizarEstadoSanciones(correo_estudiante)
        try:
            cursor = self.getCursor()
            cursor.execute(self.SQL_ACTIVA, (correo_estudiante,))
            resultado = cursor.fetchone()[0] > 0
            cursor.close()
            return resultado
        except Exception as e:
            print(f"Error en tieneSancionActiva: {e}")
            return False