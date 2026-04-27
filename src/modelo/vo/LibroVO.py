class LibroVO:
    def __init__(self, isbn, titulo, autor, fecha_llegada, num_copias, disponibilidad, descripcion, nombre_tema):
        self._isbn = isbn
        self._titulo = titulo
        self._autor = autor
        self._fecha_llegada = fecha_llegada
        self._num_copias = num_copias
        self._disponibilidad = disponibilidad
        self._descripcion = descripcion
        self._nombre_tema = nombre_tema

    @property
    def isbn(self): return self._isbn
    @property
    def titulo(self): return self._titulo
    @property
    def autor(self): return self._autor
    @property
    def fecha_llegada(self): return self._fecha_llegada
    @property
    def num_copias(self): return self._num_copias
    @property
    def disponibilidad(self): return self._disponibilidad
    @property
    def descripcion(self): return self._descripcion
    @property
    def nombre_tema(self): return self._nombre_tema
