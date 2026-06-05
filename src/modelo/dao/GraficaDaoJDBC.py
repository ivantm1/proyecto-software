from src.modelo.conexion.Conexion import Conexion


class GraficaDaoJDBC(Conexion):
    def obtener_top_temas_ultimo_mes(self, top=10):
        cursor = self.getCursor()
        try:
            sql = f"""
                SELECT TOP {top} l.nombre_tema, COUNT(*) as num_prestamos
                FROM Prestamos p
                JOIN Libros l ON p.ISBN = l.ISBN
                WHERE p.fecha_prestamo >= DATEADD(month, -1, GETDATE())
                GROUP BY l.nombre_tema
                ORDER BY num_prestamos DESC
            """
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error en obtener_top_temas_ultimo_mes: {e}")
            return []
