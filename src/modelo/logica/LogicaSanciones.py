from src.modelo.dao.SancionDaoJDBC import SancionDaoJDBC

class LogicaSanciones:
                                                                      

    def aplicarSancionRetraso(self, correo_estudiante, semanas_retraso):
        return SancionDaoJDBC().aplicarSancionRetraso(correo_estudiante, semanas_retraso)

    def aplicarSancionDanio(self, correo_estudiante, estado_libro):
        if estado_libro == "Dañado":
            return SancionDaoJDBC().aplicarSancionDanio(correo_estudiante, "Dañado", 10)
        elif estado_libro == "Roto":
            return SancionDaoJDBC().aplicarSancionDanio(correo_estudiante, "Roto", 30)
        return None

    def aplicarSancionManual(self, correo_estudiante, motivo, dias):
        return SancionDaoJDBC().aplicarSancionDanio(correo_estudiante, motivo, dias)

    def eliminarSancion(self, correo_estudiante, tipo, fecha_inicio, duracion):
        return SancionDaoJDBC().eliminarSancion(correo_estudiante, tipo, fecha_inicio, duracion)

    def obtenerSancionesEstudiante(self, correo_estudiante):
        return SancionDaoJDBC().obtenerSancionesEstudiante(correo_estudiante)

    def tieneSancionActiva(self, correo_estudiante):
        return SancionDaoJDBC().tieneSancionActiva(correo_estudiante)

    def calcularDiasSancionActiva(self, correo_estudiante):
        sanciones = self.obtenerSancionesEstudiante(correo_estudiante)
        total_dias = 0
        for sancion in sanciones:
            if sancion.estado == "Activa":
                total_dias += int(sancion.duracion_sancion)
        return total_dias
