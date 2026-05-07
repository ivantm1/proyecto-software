from src.modelo.vo.LoginVO import LoginVO
from src.modelo.vo.RegistroVO import RegistroVO
from PyQt5.QtWidgets import QApplication, QMessageBox
from src.controlador.CatalogoControlador import CatalogoControlador
from src.controlador.CatalogoMisPrestamosControlador import CatalogoMisPrestamosControlador
from src.controlador.CatalogoMisReservasControlador import CatalogoMisReservasControlador
from src.controlador.CatalogoSancionesControlador import CatalogoSancionesControlador
from src.controlador.CatalogoDevolucionControlador import CatalogoDevolucionControlador
from src.controlador.CatalogoPrestamoControlador import CatalogoPrestamoControlador
from src.controlador.CatalogoPerfilControlador import CatalogoPerfilControlador
from src.controlador.CatalogoBuscarEstudianteControlador import CatalogoBuscarEstudianteControlador
from src.controlador.CatalogoAnadirLibroControlador import CatalogoAnadirLibroControlador


class CatalogoPrincipalControlador:
    def __init__(self, ref_modelo, ref_login,
                 ref_vista_registro=None,
                 ref_vista_estudiante=None,
                 ref_vista_bibliotecario=None,
                 ref_vista_catalogo=None,
                 ref_vista_mis_prestamos=None,
                 ref_vista_mis_reservas=None,
                 ref_vista_perfil=None,
                 ref_vista_prestamo=None,
                 ref_vista_sanciones=None,
                 ref_vista_devolucion=None,
                 ref_vista_buscar_estudiante=None,
                 ref_vista_anadir_libro=None):

        self._modelo                = ref_modelo
        self._vistaLogin            = ref_login
        self._vistaRegistro         = ref_vista_registro
        self._vistaEstudiante       = ref_vista_estudiante
        self._vistaBibliotecario    = ref_vista_bibliotecario
        self._vistaCatalogo         = ref_vista_catalogo
        self._vistaMisPrestamos     = ref_vista_mis_prestamos
        self._vistaMisReservas      = ref_vista_mis_reservas
        self._vistaPerfil           = ref_vista_perfil
        self._vistaPrestamo         = ref_vista_prestamo
        self._vistaSanciones        = ref_vista_sanciones
        self._vistaDevolucion       = ref_vista_devolucion
        self._vistaBuscarEstudiante = ref_vista_buscar_estudiante
        self._vistaAnadirLibro      = ref_vista_anadir_libro
        self._usuario_activo = None

    def ventanaIniciarSesion(self):
        self._vistaLogin.Linea_usuario.clear()
        self._vistaLogin.Linea_contrasena.clear()
        self._vistaLogin.showMaximized()

    def comprobarLogin(self, loginVO):
        if not loginVO.nombre or not loginVO.contrasena:
            self._vistaLogin.lanzarAviso("Introduce usuario y contraseña.")
            return
        usuario = self._modelo.comprobarLogin(loginVO)
        if usuario is None:
            self._vistaLogin.lanzarAviso("Usuario o contraseña incorrectos.")
            return
        self._usuario_activo = usuario
        self._vistaLogin.close()
        if usuario.tipo == "Estudiante":
            self.ventanaEstudiante()
        elif usuario.tipo == "Bibliotecario":
            self.ventanaVistaBibliotecario()

    def ventanaRegistro(self):
        if self._vistaRegistro:
            self._vistaRegistro.controlador = self
            self._vistaLogin.close()
            self._vistaRegistro.showMaximized()

    def registrarUsuario(self, nombre, apellidos, correo, contrasena, confirmar):
        print("hola")
        if not all([nombre, apellidos, correo, contrasena, confirmar]):
            self._vistaRegistro.lanzarAviso("Rellena todos los campos.")
            return
        if "@estudiantes.unileon.es" not in correo:
            self._vistaRegistro.lanzarAviso("Usa un correo institucional @estudiantes.unileon.es")
            return
        if contrasena != confirmar:
            self._vistaRegistro.lanzarAviso("Las contraseñas no coinciden.")
            return
        registro = RegistroVO(nombre, apellidos, correo, contrasena)
        if self._modelo.registrarUsuario(registro):
            self._vistaRegistro.lanzarAviso("Usuario registrado con éxito. Vuelve al login.")
            self._vistaRegistro.close()
            self.ventanaIniciarSesion()
        else:
            self._vistaRegistro.lanzarAviso("Error al registrarse. El email ya puede estar registrado.")

    def registroAtras(self):
        self._vistaRegistro.close()
        self.ventanaIniciarSesion()

    def ventanaEstudiante(self):
        if self._vistaEstudiante:
            self._vistaEstudiante.controlador = self
            self._vistaEstudiante.showMaximized()

    def ventanaBibliotecario(self):
        if self._vistaBibliotecario:
            self._vistaBibliotecario.controlador = self
            self._vistaBibliotecario.showMaximized()

    def ventanaVerPerfil(self):
        if not self._vistaPerfil or not self._usuario_activo:
            return
        if self._usuario_activo.tipo == "Estudiante":
            vista_anterior = self._vistaEstudiante
        else:
            vista_anterior = self._vistaBibliotecario
        ctrl = CatalogoPerfilControlador(self._modelo, self._vistaPerfil, vista_anterior, self._usuario_activo)
        self._vistaPerfil.controlador = ctrl

        sancion_texto = None
        if self._usuario_activo.tipo == "Estudiante":
            sanciones = self._modelo.obtenerSancionesEstudiante(self._usuario_activo.correo)
            activas = [s for s in sanciones if s.estado == "Activa"]
            if activas:
                sancion_texto = str(activas[0].fecha_fin)
                
        self._vistaPerfil.mostrarUsuario(
            nombre=self._usuario_activo.nombre,
            apellidos=self._usuario_activo.apellidos,
            correo=self._usuario_activo.correo,
            tipo=self._usuario_activo.tipo,
        )
        vista_anterior.close()
        self._vistaPerfil.showMaximized()

    def ventanaCatalogo(self):
        if not self._vistaCatalogo or not self._usuario_activo:
            return
        ctrl = CatalogoControlador(
            self._modelo, self._vistaCatalogo,
            self._vistaEstudiante, self._vistaBibliotecario,
            correo_usuario=self._usuario_activo.correo,
            tipo_usuario=self._usuario_activo.tipo,
        )
        self._vistaCatalogo.controlador = ctrl
        self._vistaEstudiante.close()
        self._vistaBibliotecario.close()
        self._vistaCatalogo.showMaximized()
        ctrl.cargarCatalogo()
        libros = self._modelo.buscarLibro("", "Ninguno")
        if self._usuario_activo.tipo == "Estudiante":
            self._vistaCatalogo.cargar_lista_libros_estudiante(libros)
        else:
            self._vistaCatalogo.cargar_lista_libros_bibliotecario(libros)

    def ventanaMisPrestamos(self):
        if not self._vistaMisPrestamos or not self._usuario_activo:
            return
        ctrl = CatalogoMisPrestamosControlador(
            self._modelo, self._vistaMisPrestamos,
            self._vistaEstudiante, self._vistaBibliotecario,
            self._usuario_activo.correo, self._usuario_activo.tipo
        )
        self._vistaMisPrestamos.controlador = ctrl
        ctrl.actualizarPrestamos()
        self._vistaEstudiante.close()
        self._vistaMisPrestamos.showMaximized()

    def ventanaMisReservas(self):
        if not self._vistaMisReservas or not self._usuario_activo:
            return
        ctrl = CatalogoMisReservasControlador(
            self._modelo, self._vistaMisReservas,
            self._vistaEstudiante, self._vistaBibliotecario,
            self._usuario_activo.correo, self._usuario_activo.tipo
        )
        self._vistaMisReservas.controlador = ctrl
        ctrl.actualizarReservas()
        self._vistaEstudiante.close()
        self._vistaMisReservas.showMaximized()

    def ventanaPrestamo(self):
        if not self._vistaPrestamo:
            return
        ctrl = CatalogoPrestamoControlador(self._vistaPrestamo)
        self._vistaPrestamo.controlador = ctrl
        self._vistaPrestamo.show()

    def ventanaDevolucion(self):
        if not self._vistaDevolucion:
            return
        ctrl = CatalogoDevolucionControlador(self._modelo, self._vistaDevolucion, self._vistaBibliotecario)
        self._vistaDevolucion.controlador = ctrl
        self._vistaBibliotecario.close()
        self._vistaDevolucion.showMaximized()

    def ventanaAnadirLibro(self):
        if not self._vistaAnadirLibro:
            return
        ctrl = CatalogoAnadirLibroControlador(self._modelo, self._vistaAnadirLibro, self._vistaBibliotecario)
        self._vistaAnadirLibro.controlador = ctrl
        self._vistaBibliotecario.close()
        self._vistaAnadirLibro.showMaximized()

    def ventanaSanciones(self):
        if not self._vistaSanciones or not self._usuario_activo:
            return
        ctrl = CatalogoSancionesControlador(self._modelo, self._vistaSanciones)
        self._vistaSanciones.controlador = ctrl
        self._vistaSanciones.show()

    def cerrarSesion(self):
        respuesta = QMessageBox.question(
            self._vistaLogin, "Cerrar sesión",
            "¿Estás seguro de que quieres cerrar sesión?",
            QMessageBox.Yes | QMessageBox.No
        )
        if respuesta == QMessageBox.Yes:
            if self._vistaRegistro:
                QApplication.closeAllWindows()
                self.ventanaIniciarSesion()

    def ventanaBuscarEstudiante(self):
        if not self._vistaBuscarEstudiante:
            return
        self._vistaBuscarEstudiante.linea_busqueda.clear()
        ctrl = CatalogoBuscarEstudianteControlador(self._modelo, self._vistaBuscarEstudiante, self._vistaBibliotecario)
        self._vistaBuscarEstudiante.controlador = ctrl
        self._vistaBibliotecario.close()
        self._vistaBuscarEstudiante.showMaximized()

    def volverBuscarEstudiante(self):
        if self._vistaBuscarEstudiante and self._vistaBibliotecario:
            self._vistaBuscarEstudiante.close()
            self._vistaBibliotecario.showMaximized()