import os
from datetime import datetime

# ── Decorador Singleton (variante 1 del PDF) ─────────────────────────────────
def singleton(cls):
    """
    Hace que `cls` tenga como máximo una instancia única.
    _instances: diccionario que almacena las instancias únicas creadas.
    cls(*args): forma de instanciar la clase recibida como parámetro.
    """
    _instances = {}

    def get_instance(*args):
        if cls not in _instances:
            _instances[cls] = cls(*args)
        return _instances[cls]

    return get_instance

# ── Clase Logger decorada con @singleton ─────────────────────────────────────
@singleton
class Logger:
    """
    Logger centralizado de la aplicación Biblioteca.
    Al estar decorado con @singleton, solo existe una instancia en toda
    la ejecución: cualquier llamada a Logger() devuelve la misma.
    """

    def __init__(self):
        carpeta = os.path.join(os.getcwd(), "logs")
        os.makedirs(carpeta, exist_ok=True)
        nombre = f"log_{datetime.now().strftime('%Y%m%d')}.txt"
        self._ruta = os.path.join(carpeta, nombre)

    # ── Método interno de escritura ───────────────────────────────────────────
    def _escribir(self, nivel: str, accion: str, detalle: str = ""):
        marca = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linea = f"[{marca}] [{nivel}] {accion}"
        if detalle:
            linea += f" | {detalle}"
        linea += "\n"
        try:
            with open(self._ruta, "a", encoding="utf-8") as f:
                f.write(linea)
        except Exception as e:
            print(f"[Logger] Error escribiendo log: {e}")

    # ── API pública ───────────────────────────────────────────────────────────
    def info(self, accion: str, detalle: str = ""):
        self._escribir("INFO ", accion, detalle)

    def error(self, accion: str, detalle: str = ""):
        self._escribir("ERROR", accion, detalle)

    # ── Métodos semánticos para cada evento de la app ─────────────────────────

    def login_ok(self, correo: str, tipo: str):
        self.info("INICIO_SESION", f"usuario={correo} tipo={tipo}")

    def login_error(self, correo: str):
        self.error("INICIO_SESION_FALLIDO", f"usuario={correo}")

    def cierre_sesion(self, correo: str):
        self.info("CIERRE_SESION", f"usuario={correo}")

    def prestamo_ok(self, isbn: str, correo_estudiante: str, fecha_devolucion):
        self.info("PRESTAMO", f"isbn={isbn} estudiante={correo_estudiante} devolucion={fecha_devolucion}")

    def prestamo_error(self, isbn: str, correo_estudiante: str, motivo: str):
        self.error("PRESTAMO_FALLIDO", f"isbn={isbn} estudiante={correo_estudiante} motivo={motivo}")

    def devolucion_ok(self, isbn: str, correo_estudiante: str, semanas_retraso: int = 0):
        detalle = f"isbn={isbn} estudiante={correo_estudiante}"
        if semanas_retraso > 0:
            detalle += f" retraso={semanas_retraso}sem"
        self.info("DEVOLUCION", detalle)

    def devolucion_error(self, isbn: str):
        self.error("DEVOLUCION_FALLIDA", f"isbn={isbn}")

    def reserva_ok(self, isbn: str, correo_estudiante: str):
        self.info("RESERVA", f"isbn={isbn} estudiante={correo_estudiante}")

    def reserva_error(self, isbn: str, correo_estudiante: str, motivo: str):
        self.error("RESERVA_FALLIDA", f"isbn={isbn} estudiante={correo_estudiante} motivo={motivo}")

    def sancion_aplicada(self, correo: str, tipo: str, detalle: str = ""):
        self.info("SANCION_APLICADA", f"estudiante={correo} tipo={tipo} {detalle}".strip())

    def sancion_eliminada(self, correo: str, tipo: str):
        self.info("SANCION_ELIMINADA", f"estudiante={correo} tipo={tipo}")

    def alta_libro(self, isbn: str, titulo: str, actor: str):
        self.info("ALTA_LIBRO", f"isbn={isbn} titulo='{titulo}' por={actor}")

    def alta_libro_error(self, isbn: str, titulo: str):
        self.error("ALTA_LIBRO_FALLIDA", f"isbn={isbn} titulo='{titulo}'")

    def baja_libro(self, isbn: str, motivo: str, actor: str):
        self.info("BAJA_LIBRO", f"isbn={isbn} motivo='{motivo}' por={actor}")

    def baja_libro_error(self, isbn: str):
        self.error("BAJA_LIBRO_FALLIDA", f"isbn={isbn}")

    def restaurar_libro(self, isbn: str, actor: str):
        self.info("RESTAURAR_LIBRO", f"isbn={isbn} por={actor}")

    def copia_seguridad_ok(self, ruta: str, actor: str):
        self.info("COPIA_SEGURIDAD", f"ruta={ruta} por={actor}")

    def copia_seguridad_error(self, motivo: str, actor: str):
        self.error("COPIA_SEGURIDAD_FALLIDA", f"motivo={motivo} por={actor}")

    def registro_cuenta_ok(self, correo: str, tipo: str, actor: str):
        self.info("REGISTRO_CUENTA", f"nuevo={correo} tipo={tipo} por={actor}")

    def registro_cuenta_error(self, correo: str, actor: str):
        self.error("REGISTRO_CUENTA_FALLIDO", f"correo={correo} por={actor}")

    def eliminacion_cuenta_ok(self, correo: str, actor: str):
        self.info("ELIMINACION_CUENTA", f"eliminado={correo} por={actor}")

    def eliminacion_cuenta_error(self, correo: str, actor: str):
        self.error("ELIMINACION_CUENTA_FALLIDA", f"correo={correo} por={actor}")
