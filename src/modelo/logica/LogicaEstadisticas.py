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
        figura.patch.set_facecolor('#F7F9FC')   # fondo de la figura ligeramente azulado

        ax = figura.add_subplot(111)
        ax.set_facecolor('#F7F9FC')             # fondo del área de trazado igual

        # --- Paleta de color degradada según el valor (más préstamos → más oscuro) ---
        max_count = max(counts) if counts else 1
        colores = [
            (0.18 + 0.42 * (v / max_count),    # R
             0.44 + 0.20 * (v / max_count),    # G
             0.80 - 0.30 * (v / max_count))    # B
            for v in counts[::-1]
        ]

        bars = ax.barh(
            temas[::-1],
            counts[::-1],
            color=colores,
            edgecolor='white',
            linewidth=0.8,
            height=0.6,
        )

        # --- Etiquetas de valor al final de cada barra ---
        for bar in bars:
            w = bar.get_width()
            ax.text(
                w + max_count * 0.01,
                bar.get_y() + bar.get_height() / 2,
                str(int(w)),
                va='center',
                ha='left',
                fontsize=9,
                fontweight='bold',
                color='#333333',
            )

        # --- Grid vertical suave solo en el eje X ---
        ax.xaxis.grid(True, linestyle='--', linewidth=0.5, color='#CCCCCC', alpha=0.7)
        ax.set_axisbelow(True)

        # --- Quitar bordes sobrantes ---
        for spine in ['top', 'right', 'left']:
            ax.spines[spine].set_visible(False)
        ax.spines['bottom'].set_color('#CCCCCC')

        # --- Etiquetas de ejes y título ---
        ax.set_xlabel('Número de préstamos', fontsize=10, color='#555555', labelpad=8)
        ax.tick_params(axis='y', labelsize=9, colors='#333333', length=0)
        ax.tick_params(axis='x', labelsize=8, colors='#777777', length=0)

        ax.set_title(titulo, fontsize=13, fontweight='bold', color='#1A2E4A', pad=14)

        # --- Ajuste de márgenes para que las etiquetas de valor no queden cortadas ---
        ax.set_xlim(0, max_count * 1.15)

        figura.tight_layout(pad=1.5)

        return figura, titulo
