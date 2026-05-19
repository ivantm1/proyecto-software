from src.modelo.dao.LibroDaoJDBC import LibroDaoJDBC

class LogicaLibros:
                                                                  

    def buscarLibro(self, linea_busqueda, tema):
        lista = LibroDaoJDBC().buscarLibros(linea_busqueda, tema)
        return None if len(lista) == 0 else lista

    def obtenerCatalogo(self):
        return LibroDaoJDBC().obtenerCatalogo()

    def buscarPorTitulo(self, titulo):
        return LibroDaoJDBC().buscarPorTitulo(titulo)

    def buscarPorTema(self, tema):
        return LibroDaoJDBC().buscarPorTema(tema)

    def altaLibro(self, libroVO):
        return LibroDaoJDBC().altaLibro(libroVO)

    def bajaLibro(self, isbn, motivo="Retirado por el bibliotecario"):
        return LibroDaoJDBC().bajaLibro(isbn, motivo)

    def restaurarLibro(self, isbn):
        return LibroDaoJDBC().restaurarLibro(isbn)

    def obtenerReservados(self):
        return LibroDaoJDBC().obtenerReservados()

    def buscarPorISBN(self, isbn):
        return LibroDaoJDBC().buscarPorISBN(isbn)

    def buscarRetiradoPorISBN(self, isbn):
        return LibroDaoJDBC().buscarRetiradoPorISBN(isbn)
