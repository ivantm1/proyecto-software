import matplotlib.pyplot as plt
from src.modelo.dao.GraficaDaoJDBC import GraficaDaoJDBC


class LogicaGrafica:
    def __init__(self):
        self._dao = GraficaDaoJDBC()

    def generar_grafica_top_temas_ultimo_mes(self, top=10):
        rows = self._dao.obtener_top_temas_ultimo_mes(top)
        if not rows:
            return False, "No hay datos de préstamos en el último mes."

        temas = [r[0] for r in rows]
        counts = [r[1] for r in rows]

        plt.figure(figsize=(10, 6))
        bars = plt.barh(temas[::-1], counts[::-1], color='skyblue')
        plt.xlabel('Número de préstamos')
        plt.title(f'Top {top} temas con más préstamos (último mes)')

        for bar in bars:
            w = bar.get_width()
            plt.text(w + 0.1, bar.get_y() + bar.get_height() / 2, str(int(w)), va='center')

        plt.tight_layout()
        plt.show()
        return True, None
