from src.modelo.vo.LoginVO import LoginVO
from src.modelo.vo.RegistroVO import RegistroVO
from src.modelo.logica.LoggerSingleton import Logger
from PyQt5.QtWidgets import QApplication, QMessageBox
from src.controlador.ControladorCatalogo import ControladorCatalogo
from src.controlador.ControladorMisPrestamos import ControladorMisPrestamos
from src.controlador.ControladorMisReservas import ControladorMisReservas
from src.controlador.ControladorSanciones import ControladorSanciones
from src.controlador.ControladorDevolucion import ControladorDevolucion
from src.controlador.ControladorPrestamo import ControladorPrestamo
from src.controlador.ControladorPerfil import ControladorPerfil
from src.controlador.ControladorBuscarEstudiante import ControladorBuscarEstudiante
from src.controlador.ControladorAnadirLibro import ControladorAnadirLibro
from src.controlador.ControladorGestionarCuentas import ControladorGestionarCuentas


class ControladorPrincipal:
    def __init__(self, ref_modelo, ref_login,
                 ref_vista_registro=None,
                 ref_vista_estudiante=None,
                 ref_vista_bibliotecario=None,
                 ref_vista_admin=None,
                 ref_vista_gestionar_cuentas=None,
                 ref_vista_anadir_cuenta=None,
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
        self._vistaAdmin            = ref_vista_admin
        self._vistaGestionarCuentas = ref_vista_gestionar_cuentas
        self._vistaAnadirCuenta     = ref_vista_anadir_cuenta
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
        self._cerrando_por_cerrar_sesion = False

    def ventanaIniciarSesion(self):
        self._vistaLogin.Linea_usuario.clear()
        self._vistaLogin.Linea_contrasena.clear()
        self._vistaLogin.showMaximized()

    def comprobarLogin(self, usuario, contrasena):
        if not usuario or not contrasena:
            self._vistaLogin.lanzarAviso("Introduce usuario y contraseña.")
            return
        
        loginVO = LoginVO(usuario, contrasena)
        usuario_obj = self._modelo.comprobarLogin(loginVO)
        
        if usuario_obj is None:
            self._vistaLogin.lanzarAviso("Usuario o contraseña incorrectos.")
            Logger().login_error(usuario)
            return
        
        self._usuario_activo = usuario_obj
        Logger().login_ok(usuario_obj.correo, usuario_obj.tipo)
        self._vistaLogin.close()
        
        if usuario_obj.tipo == "Estudiante":
            self.ventanaEstudiante()
        elif usuario_obj.tipo == "Bibliotecario":
            self.ventanaBibliotecario()
        elif usuario_obj.tipo == "Admin":
            self.ventanaAdmin()

    def ventanaRegistro(self):
        if self._vistaRegistro:
            self._vistaRegistro.controlador = self
            self._vistaLogin.close()
            self._vistaRegistro.showMaximized()

    def registrarUsuario(self, nombre, apellidos, correo, contrasena, confirmar, tipo):
        valido, mensaje = self._modelo.validarRegistro(nombre, apellidos, correo, contrasena, confirmar)
        if not valido:
            self._vistaAnadirCuenta.lanzarAviso(mensaje)
            return

        registro = RegistroVO(nombre, apellidos, correo, contrasena, tipo)
        if self._modelo.registrarUsuario(registro):
            Logger().registro_cuenta_ok(correo, tipo, actor="Registro público")
            self._vistaAnadirCuenta.lanzarAviso("Usuario registrado con éxito.")
            self._vistaAnadirCuenta.close()
            self.ventanaGestionarCuentas()
        else:
            Logger().registro_cuenta_error(correo, actor="Registro público")
            self._vistaAnadirCuenta.lanzarAviso("Error al registrarse. El email ya puede estar registrado.")

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

    def ventanaAdmin(self):
        if self._vistaAdmin:
            self._vistaAdmin.controlador = self
            self._vistaAdmin.showMaximized()

    def ventanaGestionarCuentas(self):
        if not self._vistaGestionarCuentas or not self._usuario_activo:
            return
        ctrl = ControladorGestionarCuentas(
            self._modelo,
            self._vistaGestionarCuentas,
            self._vistaAdmin,
            self._vistaAnadirCuenta,
            self._usuario_activo.correo,
        )
        self._vistaGestionarCuentas.lineEdit.clear()
        self._vistaAdmin.close()
        self._vistaGestionarCuentas.showMaximized()

    def ventanaVerPerfil(self):
        if not self._vistaPerfil or not self._usuario_activo:
            return
        if self._usuario_activo.tipo == "Estudiante":
            vista_anterior = self._vistaEstudiante
        elif self._usuario_activo.tipo == "Bibliotecario":
            vista_anterior = self._vistaBibliotecario
        elif self._usuario_activo.tipo == "Admin":
            vista_anterior = self._vistaAdmin
        ctrl = ControladorPerfil(self._modelo, self._vistaPerfil, vista_anterior, self._usuario_activo)
        self._vistaPerfil.controlador = ctrl

        total_dias = 0
        if self._usuario_activo.tipo == "Estudiante":
            total_dias = self._modelo.calcularDiasSancionActiva(self._usuario_activo.correo)

        self._vistaPerfil.mostrarUsuario(
            nombre=self._usuario_activo.nombre,
            apellidos=self._usuario_activo.apellidos,
            correo=self._usuario_activo.correo,
            tipo=self._usuario_activo.tipo,
            total_dias=total_dias
        )
        vista_anterior.close()
        self._vistaPerfil.showMaximized()

    def ventanaCatalogo(self):
        if not self._vistaCatalogo or not self._usuario_activo:
            return
        ctrl = ControladorCatalogo(
            self._modelo, self._vistaCatalogo,
            self._vistaEstudiante, self._vistaBibliotecario, self._vistaAdmin,
            correo_usuario=self._usuario_activo.correo,
            tipo_usuario=self._usuario_activo.tipo,
        )
        self._vistaCatalogo.controlador = ctrl
        if self._vistaEstudiante:
            self._vistaEstudiante.close()
        if self._vistaBibliotecario:
            self._vistaBibliotecario.close()
        if self._vistaAdmin:
            self._vistaAdmin.close()
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
        ctrl = ControladorMisPrestamos(
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
        ctrl = ControladorMisReservas(
            self._modelo, self._vistaMisReservas,
            self._vistaEstudiante, self._vistaBibliotecario,
            self._usuario_activo.correo, self._usuario_activo.tipo
        )
        self._vistaMisReservas.controlador = ctrl
        ctrl.actualizarReservas()
        self._vistaEstudiante.close()
        self._vistaMisReservas.showMaximized()

    def ventanaDevolucion(self):
        if not self._vistaDevolucion:
            return
        ctrl = ControladorDevolucion(self._modelo, self._vistaDevolucion, self._vistaBibliotecario)
        self._vistaDevolucion.controlador = ctrl
        self._vistaBibliotecario.close()
        self._vistaDevolucion.showMaximized()

    def ventanaAnadirLibro(self):
        if not self._vistaAnadirLibro:
            return
        correo = self._usuario_activo.correo if self._usuario_activo else ""
        ctrl = ControladorAnadirLibro(
            self._modelo,
            self._vistaAnadirLibro,
            self._vistaBibliotecario,
            correo_actor=correo
        )
        self._vistaAnadirLibro.controlador = ctrl
        self._vistaBibliotecario.close()
        self._vistaAnadirLibro.showMaximized()

    def cerrarSesion(self):
        msg = QMessageBox()
        msg.setWindowTitle("Cerrar sesión")
        msg.setText("¿Estás seguro de que quieres cerrar sesión?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.button(QMessageBox.Yes).setText("Sí")
        msg.button(QMessageBox.No).setText("No")
        respuesta = msg.exec_()
        if respuesta == QMessageBox.Yes:
            Logger().cierre_sesion(self._usuario_activo.correo)
            self._cerrando_por_cerrar_sesion = True
            if self._vistaRegistro:
                QApplication.closeAllWindows()
                self.ventanaIniciarSesion()

    def ventanaBuscarEstudiante(self):
        if not self._vistaBuscarEstudiante:
            return
        self._vistaBuscarEstudiante.linea_busqueda.clear()
        ctrl = ControladorBuscarEstudiante(self._modelo, self._vistaBuscarEstudiante, self._vistaBibliotecario)
        self._vistaBuscarEstudiante.controlador = ctrl
        self._vistaBibliotecario.close()
        self._vistaBuscarEstudiante.showMaximized()

    def realizarCopiaSeguridad(self):
        from PyQt5.QtWidgets import QMessageBox

        exito, info = self._modelo.realizarCopiaSeguridad()
        actor = self._usuario_activo.correo if self._usuario_activo else "desconocido"
        msg = QMessageBox()
        if exito:
            Logger().copia_seguridad_ok(info, actor)
            msg.setWindowTitle("Copia de seguridad")
            msg.setIcon(QMessageBox.Information)
            msg.setText("✅ Copia de seguridad creada correctamente.")
            msg.setInformativeText(f"Guardada en:\n{info}")
        else:
            Logger().copia_seguridad_error(info, actor)
            msg.setWindowTitle("Error")
            msg.setIcon(QMessageBox.Critical)
            msg.setText("❌ No se pudo crear la copia de seguridad.")
            msg.setInformativeText(info)
        msg.exec_()