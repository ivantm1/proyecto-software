import datetime
from src.modelo.vo.LibroVO import LibroVO

class CatalogoAnadirLibroControlador:
    def __init__(self, ref_modelo, ref_vista_anadir, ref_vista_bibliotecario):
        self._modelo             = ref_modelo
        self._vista              = ref_vista_anadir
        self._vista_bibliotecario = ref_vista_bibliotecario

    def anadirLibro(self, titulo, isbn, autor, tema, descripcion):
        # 1. Validar que todos los campos estén rellenos
        if not all([titulo, isbn, autor, tema, descripcion]):
            self._vista.lanzarAviso("Por favor, rellena todos los campos.")
            return

        # 2. Comprobar que el ISBN no exista ya en la BD
        libro_existente = self._modelo.buscarPorISBN(isbn)
        if libro_existente is not None:
            self._vista.lanzarAviso(f"Ya existe un libro con el ISBN '{isbn}'.")
            return

        # 3. Construir el LibroVO con fecha de hoy
        hoy = datetime.date.today().strftime('%Y-%m-%d')
        libro = LibroVO(
            isbn=isbn,
            titulo=titulo,
            autor=autor,
            fecha_llegada=hoy,
            num_copias=1,
            disponibilidad='Disponible',
            descripcion=descripcion,
            nombre_tema=tema
        )

        # 4. Llamar a la capa de lógica
        exito = self._modelo.altaLibro(libro)
        if exito:
            self._vista.mostrarResultado(f"Libro '{titulo}' añadido correctamente.")
            self._vista.lanzarAviso(f"Libro '{titulo}' añadido correctamente.")
            self._vista.limpiarFormulario()
        else:
            self._vista.lanzarAviso("Error al añadir el libro. Comprueba los datos e inténtalo de nuevo.")

    def volver(self):
        self._vista.limpiarFormulario()
        self._vista.close()
        self._vista_bibliotecario.showMaximized()