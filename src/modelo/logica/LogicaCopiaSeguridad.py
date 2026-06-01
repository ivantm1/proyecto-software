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
