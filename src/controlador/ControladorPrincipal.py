from src.controlador.ControladorPrincipal import ControladorPrincipal
from src.controlador.CatalogoControlador import CatalogoControlador


class ControladorPrincipalExtension(ControladorPrincipal):
    def __init__(self, ref_modelo, ref_login,
                 ref_vista_registro=None,
                 ref_vista_estudiante=None,
                 ref_vista_bibliotecario=None,
                 ref_vista_catalogo=None,
                 ref_vista_mis_prestamos=None,
                 ref_vista_perfil=None,
                 ref_vista_sanciones=None,
                 ref_vista_devolucion=None):

        super().__init__(
            ref_modelo, ref_login,
            ref_vista_registro,
            ref_vista_estudiante,
            ref_vista_bibliotecario,
        )
        self._vistaCatalogo     = ref_vista_catalogo
        self._vistaMisPrestamos = ref_vista_mis_prestamos
        self._vistaPerfil       = ref_vista_perfil
        self._vistaSanciones    = ref_vista_sanciones
        self._vistaDevolucion   = ref_vista_devolucion

        # correo y tipo del usuario logueado — se rellenan en comprobarLogin
        self._correo_activo = None
        self._tipo_activo   = None

    # ------------------------------------------------------------------
    # Navegación — métodos que invocaban las vistas y no existían
    # ------------------------------------------------------------------

    def ventanaVerCatalogo(self):
        if not self._vistaCatalogo:
            return
        catalogo_ctrl = CatalogoControlador(
            self._modelo,
            self._vistaCatalogo,
            correo_usuario=self._correo_activo,
            tipo_usuario=self._tipo_activo,
        )
        self._vistaCatalogo.controlador = catalogo_ctrl
        self._vistaCatalogo.mostrarParaTipo(self._tipo_activo)
        catalogo_ctrl.cargarCatalogo()
        self._vistaCatalogo.show()

    def ventanaVerPerfil(self):
        if self._vistaPerfil:
            self._vistaPerfil.mostrarUsuario(
                self._correo_activo, self._tipo_activo
            )
            self._vistaPerfil.show()

    def ventanaMisPrestamos(self):
        if self._vistaMisPrestamos:
            self._vistaMisPrestamos.cargarPrestamos(
                self._modelo, self._correo_activo
            )
            self._vistaMisPrestamos.show()

    def ventanaPrestamo(self):
        # Reutiliza la vista Prestamo existente
        if self._vistaBibliotecario:
            from src.vista.Prestamo import Prestamo
            from src.controlador.PrestamoControlador import PrestamoControlador
            vista_prestamo = Prestamo(parent=None)
            ctrl = PrestamoControlador(vista_prestamo)
            vista_prestamo.controlador = ctrl
            vista_prestamo.show()

    def ventanaDevolucion(self):
        if self._vistaDevolucion:
            self._vistaDevolucion.show()

    def ventanaSanciones(self):
        if self._vistaSanciones:
            self._vistaSanciones.cargarSanciones(
                self._modelo, self._correo_activo
            )
            self._vistaSanciones.show()
