import os
import json
from datetime import datetime
from src.modelo.conexion.Conexion import Conexion

class CopiaSeguridadDaoJDBC(Conexion):

    TABLAS = [
        "Tema", "Usuarios", "Estudiantes", "Libros",
        "Prestamos", "Reservas", "Sanciones", "TemasFavoritos", "Retirados"
    ]

    def exportarDatos(self) -> dict:
        """Devuelve un dict {tabla: [filas como dicts]} con todos los datos."""
        cursor = self.getCursor()
        resultado = {}
        for tabla in self.TABLAS:
            try:
                cursor.execute(f"SELECT * FROM {tabla}")
                columnas = [desc[0] for desc in cursor.description]
                filas = cursor.fetchall()
                resultado[tabla] = [
                    dict(zip(columnas, [str(v) if v is not None else None for v in fila]))
                    for fila in filas
                ]
            except Exception as e:
                print(f"[Backup] Error exportando tabla {tabla}: {e}")
                resultado[tabla] = []
        return resultado

    def guardarCopia(self) -> str:
        """
        Genera el fichero de backup y lo guarda en copias_seguridad/.
        Devuelve la ruta absoluta del fichero creado, o lanza excepción.
        """
        datos = self.exportarDatos()
        carpeta = os.path.join(os.getcwd(), "copias_seguridad")
        os.makedirs(carpeta, exist_ok=True)
        nombre = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        ruta = os.path.join(carpeta, nombre)
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
        return ruta
