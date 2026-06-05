import jaydebeapi

class Conexion:
    def __init__(self, host='localhost', database='BibliotecaDB', user='biblioteca_user', password='pruebaISD2024'):
        self._host = host
        self._database = database
        self._user = user
        self._password = password
        self.conexion = self.createConnection()

    def createConnection(self):
        try:
            jdbc_driver = "com.microsoft.sqlserver.jdbc.SQLServerDriver"
            jar_file = "lib/mssql-jdbc-13.4.0.jre11.jar"
            connection_url = (
                f"jdbc:sqlserver://{self._host};"
                f"databaseName={self._database};"
                f"encrypt=true;"
                f"trustServerCertificate=true;"
            )
            self.conexion = jaydebeapi.connect(
                jdbc_driver,
                connection_url,
                [self._user, self._password],
                jar_file
            )
            return self.conexion
        except Exception as e:
            print("Error creando conexión:", e)
            return None

    def getCursor(self):
        if self.conexion is None:
            self.createConnection()
        return self.conexion.cursor()
