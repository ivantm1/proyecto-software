# 📚 BiblioULE — Sistema de Gestión de Biblioteca

Aplicación de escritorio para la gestión integral de una biblioteca universitaria, desarrollada como proyecto de la asignatura de Ingeniería del Software. Permite administrar libros, préstamos, reservas, usuarios y sanciones desde una interfaz gráfica intuitiva con tres niveles de acceso.

---

## 🗂 Estructura del proyecto

```
proyecto-software/
├── main.py                        # Punto de entrada
├── DataBase.sql                  # Script de creación de la base de datos
├── lib/
│   └── mssql-jdbc-13.4.0.jre11.jar
└── src/
    ├── controlador/               # Capa de control (MVC)
    │   ├── ControladorPrincipal.py
    │   ├── ControladorSanciones.py
    │   ├── ControladorBuscarEstudiante.py
    │   └── ...
    ├── modelo/
    │   ├── conexion/
    │   │   └── Conexion.py        # Gestión de conexión JDBC
    │   ├── dao/                   # Acceso a datos
    │   │   ├── LibroDaoJDBC.py
    │   │   ├── PrestamoDaoJDBC.py
    │   │   ├── ReservaDaoJDBC.py
    │   │   ├── SancionDaoJDBC.py
    │   │   └── ...
    │   ├── logica/                # Lógica de negocio
    │   │   ├── Logica.py          # Fachada principal
    │   │   ├── LogicaLibros.py
    │   │   ├── LogicaPrestamos.py
    │   │   ├── LogicaSanciones.py
    │   │   └── ...
    │   └── vo/                    # Value Objects (DTOs)
    │       ├── LibroVO.py
    │       ├── PrestamoVO.py
    │       ├── SancionVO.py
    │       └── ...
    └── vista/
        ├── Ui/                    # Ficheros .ui de Qt Designer
        └── *.py                   # Vistas PyQt5
```

---

## ⚙️ Requisitos previos

| Requisito | Versión recomendada |
|---|---|
| Python | 3.10 o superior |
| Java JRE/JDK | 11 o superior (necesario para JDBC) |
| SQL Server | 2019 o superior |
| Anaconda (opcional) | cualquier versión reciente |

### Dependencias Python

```bash
pip install PyQt5 jaydebeapi JPype1
```

---

## 🗄️ Configuración de la base de datos

1. Abre **SQL Server Management Studio** (SSMS) o Azure Data Studio.
2. Ejecuta el script completo `DataBase.sql`. Esto crea la base de datos `BibliotecaDB`, todas las tablas y los datos iniciales.
3. Crea el usuario de SQL Server con los siguientes credenciales (o edita `Conexion.py` con los tuyos):

## 👥 Roles de usuario

| Rol | Capacidades |
|---|---|
| **Estudiante** | Consultar catálogo, gestionar sus préstamos y reservas, ver su perfil y sanciones activas |
| **Bibliotecario** | Añadir/retirar libros, gestionar préstamos y devoluciones, buscar estudiantes, aplicar sanciones |
| **Administrador** | Todo lo anterior más gestión de cuentas de usuario y copia de seguridad |

## 🔑 Credenciales para pruebas
| Rol | Correo | Contraseña |
|---|---|---|
| **Estudiante** | 123 | 123 |
| **Bibliotecario** | 12 | 12 |
| **Administrador** | 1 | 1 |

---

## 🔧 Funcionalidades principales

### Libros
- Catálogo con búsqueda por título, autor y temática
- Alta y baja de libros con control de disponibilidad
- Estados: `Disponible`, `Prestado`, `Reservado`, `Retirado`

### Préstamos
- Máximo de 7 préstamos activos por estudiante
- Control de devolución con detección automática de retraso
- Cooldown entre préstamos del mismo libro

### Reservas
- Sistema de cola por libro
- Caducidad automática de reservas no recogidas
- Estados: `Espera`, `Recoger`, `Caducada`

### Sanciones
- Aplicación manual por motivo y días, o automática por retraso en devolución o daño al libro
- **Cola de sanciones**: solo puede haber una sanción activa al mismo tiempo; las demás quedan en `Pendiente` y se activan automáticamente en orden cuando la anterior se cumple
- **Fechas encadenadas**: la fecha de inicio de cada sanción pendiente se calcula desde el fin de la anterior, no desde el día de apertura de la app
- Los días mostrados al bibliotecario son la suma de la sanción activa más todas las pendientes
- Estados: `Activa`, `Pendiente`, `Cumplida`

### Administración
- Gestión completa de cuentas (crear, editar, eliminar)
- Copia de seguridad de la base de datos
- Panel de estadísticas

---

## 🏗️ Arquitectura

El proyecto sigue el patrón **MVC en capas**:

```
Vista (PyQt5)  ←→  Controlador  ←→  Logica (fachada)  ←→  DAO (JDBC)  ←→  SQL Server
```

- La capa **DAO** accede directamente a la base de datos mediante `jaydebeapi` con el driver JDBC de Microsoft SQL Server.
- La capa de **lógica** encapsula las reglas de negocio y es la única que instancia DAOs.
- Los **controladores** median entre la vista y la lógica, sin acceder nunca directamente a la BD.
- Las **vistas** son completamente pasivas y no contienen lógica de negocio.
- Los **Value Objects (VO)** son objetos de transferencia de datos simples entre capas.

---

## 📝 Notas técnicas

- La conexión a SQL Server se realiza vía **JDBC** (`jaydebeapi` + `JPype1`), lo que requiere Java instalado y el `.jar` del driver en la carpeta `lib/`.
- Los warnings de Java sobre acceso nativo (`java.lang.System::load`) son esperados en entornos Anaconda y no afectan al funcionamiento.
- La comprobación del tiempo transcurrido en sanciones usa `datetime.date.today()`, que toma la fecha del sistema operativo local.
