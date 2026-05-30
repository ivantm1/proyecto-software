from src.modelo.dao.LibroDaoJDBC import LibroDaoJDBC
import datetime
from src.modelo.vo.LibroVO import LibroVO

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

    def validarAltaLibro(self, titulo, isbn, autor, tema, descripcion):
        """Valida que los datos para agregar un libro sean correctos."""
        if not all([titulo, isbn, autor, tema, descripcion]):
            return False, "Por favor, rellena todos los campos."
        
        libro_existente = self.buscarPorISBN(isbn)
        if libro_existente is not None:
            return False, f"Ya existe un libro con el ISBN '{isbn}'."
        
        return True, ""

    def crearLibroVO(self, titulo, isbn, autor, tema, descripcion):
        """Crea un VO de Libro con la información proporcionada."""
        hoy = datetime.date.today().strftime('%Y-%m-%d')
        return LibroVO(
            isbn=isbn,
            titulo=titulo,
            autor=autor,
            fecha_llegada=hoy,
            num_copias=1,
            disponibilidad='Disponible',
            descripcion=descripcion,
            nombre_tema=tema
        )
