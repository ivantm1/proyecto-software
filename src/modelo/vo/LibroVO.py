class LibroVO:
    def __init__(self, isbn, titulo, autores, tema, fecha_llegada, descripcion, estado="disponible"):
        self._isbn = isbn
        self._titulo = titulo
        self._autores = autores
        self._tema = tema
        self._fecha_llegada = fecha_llegada
        self._descripcion = descripcion
        self._estado = estado

    @property
    def isbn(self): return self._isbn
    @property
    def titulo(self): return self._titulo
    @property
    def autores(self): return self._autores
    @property
    def tema(self): return self._tema
    @property
    def fecha_llegada(self): return self._fecha_llegada
    @property
    def descripcion(self): return self._descripcion
    @property
    def estado(self): return self._estado
    @estado.setter
    def estado(self, nuevo_estado): self._estado = nuevo_estado
