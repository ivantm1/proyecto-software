from src.modelo.dao.EstadisticasDaoJDBC import EstadisticasDaoJDBC
from matplotlib.figure import Figure


class LogicaEstadisticas:
    def __init__(self):
        self._dao = EstadisticasDaoJDBC()

    def crear_grafica_top_temas(self, periodo, figura=None):
        """Genera la gráfica para el periodo indicado y la devuelve en una Figure.

        Si figura es None, crea una nueva. Devuelve (Figure, titulo) o (None, mensaje) si no hay datos.
        """
        rows = self._dao.obtener_top_temas(periodo)
        if not rows:
            return None, "No hay datos de préstamos en el periodo seleccionado."

        temas = [r[0] for r in rows]
        counts = [r[1] for r in rows]
        periodo_texto = '1 semana' if periodo == '1w' else '1 mes' if periodo == '1m' else '3 meses'
        titulo = f'Top 10 temas con más préstamos ({periodo_texto})'

        # Crear figura si no se proporcionó
        if figura is None:
            figura = Figure(figsize=(8, 6))

        # Dibujar en la figura
        figura.clear()
        ax = figura.add_subplot(111)
        bars = ax.barh(temas[::-1], counts[::-1], color='skyblue')
        ax.set_xlabel('Número de préstamos')
        ax.set_title(titulo)
        for bar in bars:
            w = bar.get_width()
            ax.text(w + 0.1, bar.get_y() + bar.get_height() / 2, str(int(w)), va='center')
        figura.tight_layout()

        return figura, titulo
