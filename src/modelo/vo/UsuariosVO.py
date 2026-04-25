class UsuariosVO:
    def __init__(self, nombre_user, first_name, full_name, email, tipo):
        self._nombre_user = nombre_user
        self._first_name = first_name
        self._full_name = full_name
        self._email = email
        self._tipo = tipo

    @property
    def nombre_user(self): return self._nombre_user
    @property
    def first_name(self): return self._first_name
    @property
    def full_name(self): return self._full_name
    @property
    def email(self): return self._email
    @property
    def tipo(self): return self._tipo
