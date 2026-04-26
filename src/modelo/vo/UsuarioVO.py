class UsuarioVO:
    def __init__(self, nombre, apellidos, correo, contrasena,tipo):
        self._nombre = nombre
        self._apellidos = apellidos
        self._correo = correo
        self._contrasena = contrasena
        self._tipo = tipo

    @property
    def nombre(self):
        return self._nombre

    @property
    def apellidos(self):
        return self._apellidos
    
    @property
    def correo(self):
        return self._correo
    
    @property
    def contrasena(self):
        return self._contrasena
    
    @property
    def tipo(self):
        return self._tipo