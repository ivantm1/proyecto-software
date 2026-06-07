from src.modelo.dao.CopiaSeguridadDaoJDBC import CopiaSeguridadDaoJDBC

class LogicaCopiaSeguridad:

    def realizarCopiaSeguridad(self) -> tuple[bool, str]:
        """
        Retorna (True, ruta) si la copia se crea con éxito,
        o (False, mensaje_error) si falla.
        """
        try:
            dao = CopiaSeguridadDaoJDBC()
            ruta = dao.guardarCopia()
            return True, ruta
        except Exception as e:
            return False, str(e)

    def restaurarCopiaSeguridad(self, ruta: str) -> tuple[bool, str]:
        """
        Retorna (True, ruta) si la restauración tiene éxito,
        o (False, mensaje_error) si falla.
        """
        try:
            dao = CopiaSeguridadDaoJDBC()
            dao.restaurarCopia(ruta)
            return True, ruta
        except Exception as e:
            return False, str(e)
