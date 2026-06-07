import os
import json
from datetime import datetime
from src.modelo.conexion.Conexion import Conexion

class CopiaSeguridadDaoJDBC(Conexion):

    TABLAS = [
        "Tema", "Usuarios", "Estudiantes", "Libros",
        "Prestamos", "Reservas", "Sanciones", "Retirados"
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

    IDENTITY_TABLES = ["Sanciones", "Reservas", "Prestamos"]

    def restaurarCopia(self, ruta: str) -> None:
        """
        Restaura la BD a partir del JSON en 'ruta'.
        Lanza excepción si algo falla (el caller hace rollback).
        """
        # Cargar JSON
        with open(ruta, "r", encoding="utf-8") as f:
            datos = json.load(f)

        cursor = self.getCursor()
        try:
            self.conexion.jconn.setAutoCommit(False)
        except Exception:
            pass

        try:
            # Borrar en orden inverso
            for tabla in reversed(self.TABLAS):
                cursor.execute(f"DELETE FROM {tabla}")

            # Insertar
            for tabla in self.TABLAS:
                filas = datos.get(tabla, [])
                identidad_completa = f"dbo.{tabla}" if tabla in self.IDENTITY_TABLES else tabla
                if tabla in self.IDENTITY_TABLES and filas:
                    cursor.execute(f"SET IDENTITY_INSERT {identidad_completa} ON")
                    identity_on = True
                else:
                    identity_on = False

                try:
                    for fila in filas:
                        if not fila:
                            continue
                        columnas = list(fila.keys())
                        valores = list(fila.values())
                        placeholders = ", ".join(["?" for _ in columnas])
                        cols_str = ", ".join(columnas)
                        destino = identidad_completa if tabla in self.IDENTITY_TABLES else tabla
                        sql = f"INSERT INTO {destino} ({cols_str}) VALUES ({placeholders})"
                        cursor.execute(sql, valores)
                finally:
                    if identity_on:
                        cursor.execute(f"SET IDENTITY_INSERT {identidad_completa} OFF")

            # Commit en el conector JDBC
            try:
                self.conexion.jconn.commit()
            except Exception:
                self.conexion.commit()
        except Exception as e:
            try:
                self.conexion.jconn.rollback()
            except Exception:
                try:
                    self.conexion.rollback()
                except Exception:
                    pass
            raise e
        finally:
            try:
                self.conexion.jconn.setAutoCommit(True)
            except Exception:
                pass
