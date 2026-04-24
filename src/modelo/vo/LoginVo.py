class LoginVO:
    def __init__(self, nombre, contrasena):
        self._nombre = nombre
        self._contrasena = contrasena

    @property
    def nombre(self):
        return self._nombre

    @property
    def contrasena(self):
        return self._contrasena
