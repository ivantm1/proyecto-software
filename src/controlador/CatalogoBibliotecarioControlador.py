from src.modelo.vo.LoginVO import LoginVO
from src.modelo.vo.RegistroVO import RegistroVO
from src.controlador.CatalogoControlador import CatalogoControlador
from src.controlador.CatalogoMisPrestamosControlador import CatalogoMisPrestamosControlador
from src.controlador.CatalogoSancionesControlador import CatalogoSancionesControlador
from src.controlador.CatalogoDevolucionControlador import CatalogoDevolucionControlador
from src.controlador.CatalogoPrestamoControlador import CatalogoPrestamoControlador


class CatalogoBibliotecarioControlador:
    def __init__(self, 
                 ref_vista_bibliotecario=None,
                 ref_vista_catalogo=None,
                 ref_vista_perfil=None,
                 ref_vista_prestamo=None,
                 ref_vista_sanciones=None,
                 ref_vista_devolucion=None):

        self._vistaBibliotecario = ref_vista_bibliotecario
        self._vistaCatalogo      = ref_vista_catalogo
        self._vistaPrestamo      = ref_vista_prestamo
        self._vistaDevolucion    = ref_vista_devolucion
        self._vistaSanciones     = ref_vista_sanciones
        self._vistaPerfil        = ref_vista_perfil

        self._usuario_activo = None  

    def ventanaCatalogo(self):
        if self._vistaRegistro:
            if not self._vistaCatalogo or not self._usuario_activo:
                return
        ctrl = CatalogoControlador(
            self._modelo,
            self._vistaCatalogo,
            correo_usuario=self._usuario_activo.correo,
            tipo_usuario=self._usuario_activo.tipo,
        )
        self._vistaCatalogo.controlador = ctrl
        self._vistaCatalogo.show()
    