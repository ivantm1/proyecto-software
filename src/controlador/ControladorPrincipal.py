from src.modelo.vo.LoginVO import LoginVO
from src.modelo.vo.RegistroVO import RegistroVO
from src.controlador.CatalogoControlador import CatalogoControlador
from src.controlador.MisPrestamosControlador import MisPrestamosControlador
from src.controlador.SancionesControlador import SancionesControlador
from src.controlador.DevolucionControlador import DevolucionControlador
from src.controlador.PrestamoControlador import PrestamoControlador


class ControladorPrincipal:
    def __init__(self, ref_modelo, ref_login,
                 ref_vista_registro=None,
                 ref_vista_estudiante=None,
                 ref_vista_bibliotecario=None,
                 ref_vista_catalogo=None,
                 ref_vista_mis_prestamos=None,
                 ref_vista_perfil=None,
                 ref_vista_prestamo=None,
                 ref_vista_sanciones=None,
                 ref_vista_devolucion=None):
        

        self._modelo             = ref_modelo
        self._vistaLogin         = ref_login
        self._vistaRegistro      = ref_vista_registro
        self._vistaEstudiante    = ref_vista_estudiante
        self._vistaBibliotecario = ref_vista_bibliotecario
        self._vistaCatalogo      = ref_vista_catalogo
        self._vistaMisPrestamos  = ref_vista_mis_prestamos
        self._vistaPerfil        = ref_vista_perfil
        self._vistaPrestamo      = ref_vista_prestamo
        self._vistaSanciones     = ref_vista_sanciones
        self._vistaDevolucion    = ref_vista_devolucion

        self._usuario_activo = None  

    def ventanaIniciarSesion(self):
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
            self.ventanaBibliotecario()

    def ventanaRegistro(self):
        if self._vistaRegistro:
            self._vistaLogin.close()
            self._vistaRegistro.showMaximized()

    def registrarUsuario(self, nombre, apellidos, correo, contrasena, confirmar):
        if not all([nombre, apellidos, correo, contrasena, confirmar]):
            self._vistaRegistro.lanzarAviso("Rellena todos los campos.")
            return

        if "@estudiantes.unileon.es" not in correo:
            self._vistaRegistro.lanzarAviso("Usa un correo institucional.")
            return

        if contrasena != confirmar:
            self._vistaRegistro.lanzarAviso("Las contraseñas no coinciden.")
            return

        registro = RegistroVO(nombre, apellidos, correo, contrasena)
        if self._modelo.registrarUsuario(registro):
            self._vistaRegistro.lanzarAviso("Usuario registrado con éxito.")
            self._vistaRegistro.close()
            self.ventanaIniciarSesion()
        else:
            self._vistaRegistro.lanzarAviso("Error al registrarse.")

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
        self._vistaPerfil.mostrarUsuario(
            correo=self._usuario_activo.correo,
            tipo=self._usuario_activo.tipo,
            nombre=self._usuario_activo.nombre,
            apellidos=self._usuario_activo.apellidos,
        )
        self._vistaPerfil.show()

    def ventanaCatalogo(self):
        if not self._vistaCatalogo or not self._usuario_activo:
            return
        ctrl = CatalogoControlador(
            self._modelo,
            self._vistaCatalogo,
            correo_usuario=self._usuario_activo.correo,
            tipo_usuario=self._usuario_activo.tipo,
        )
        self._vistaCatalogo.controlador = ctrl
        self._vistaEstudiante.close()
        self._vistaCatalogo.showMaximized()
    
        libros = self._modelo.buscarLibro("", "Ninguno")
        if self._usuario_activo.tipo == "Estudiante":
            self._vistaCatalogo.cargar_lista_libros_estudiante(libros)
        else:
            self._vistaCatalogo.cargar_lista_libros_bibliotecario(libros)

    def ventanaMisPrestamos(self):
        if not self._vistaMisPrestamos or not self._usuario_activo:
            return
        ctrl = MisPrestamosControlador(
            self._modelo,
            self._vistaMisPrestamos,
            self._usuario_activo.correo,
        )
        self._vistaMisPrestamos.controlador = ctrl
        ctrl.actualizarPrestamos()
        self._vistaMisPrestamos.show()

    def ventanaPrestamo(self):
        if not self._vistaPrestamo:
            return
        ctrl = PrestamoControlador(self._vistaPrestamo)
        self._vistaPrestamo.controlador = ctrl
        self._vistaPrestamo.show()

    def ventanaDevolucion(self):
        if not self._vistaDevolucion:
            return
        ctrl = DevolucionControlador(self._modelo, self._vistaDevolucion)
        self._vistaDevolucion.controlador = ctrl
        self._vistaDevolucion.show()

    def ventanaSanciones(self):
        if not self._vistaSanciones or not self._usuario_activo:
            return
        ctrl = SancionesControlador(self._modelo, self._vistaSanciones)
        self._vistaSanciones.controlador = ctrl
        self._vistaSanciones.show()
