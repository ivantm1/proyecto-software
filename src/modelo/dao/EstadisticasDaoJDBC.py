from src.modelo.conexion.Conexion import Conexion


class EstadisticasDaoJDBC(Conexion):
    def obtener_top_temas(self, periodo):
        cursor = self.getCursor()
        try:
            # Determinar la unidad y el valor para DATEADD según periodo
            if periodo == '1w':
                dateadd = "DATEADD(week, -1, GETDATE())"
            elif periodo == '1m':
                dateadd = "DATEADD(month, -1, GETDATE())"
            elif periodo == '3m':
                dateadd = "DATEADD(month, -3, GETDATE())"

            sql = f"""
                SELECT TOP 10 l.nombre_tema, COUNT(*) as num_prestamos
                FROM Prestamos p
                JOIN Libros l ON p.ISBN = l.ISBN
                WHERE p.fecha_prestamo >= {dateadd}
                GROUP BY l.nombre_tema
                ORDER BY num_prestamos DESC
            """
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error en obtener_top_temas: {e}")
            return []
