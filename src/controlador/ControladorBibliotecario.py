from src.modelo.vo.LoginVO import LoginVO
from src.modelo.vo.RegistroVO import RegistroVO
from src.controlador.ControladorCatalogo import ControladorCatalogo
from src.controlador.ControladorMisPrestamos import ControladorMisPrestamos
from src.controlador.ControladorSanciones import ControladorSanciones
from src.controlador.ControladorDevolucion import ControladorDevolucion
from src.controlador.ControladorPrestamo import ControladorPrestamo


class ControladorBibliotecario:
    def __init__(self, 
                 ref_modelo=None,
                 ref_vista_bibliotecario=None,
                 ref_vista_catalogo=None,
                 ref_vista_perfil=None,
                 ref_vista_prestamo=None,
                 ref_vista_sanciones=None,
                 ref_vista_devolucion=None):

        self._modelo             = ref_modelo
        self._vistaBibliotecario = ref_vista_bibliotecario
        self._vistaCatalogo      = ref_vista_catalogo
        self._vistaPrestamo      = ref_vista_prestamo
        self._vistaDevolucion    = ref_vista_devolucion
        self._vistaSanciones     = ref_vista_sanciones
        self._vistaPerfil        = ref_vista_perfil

        self._usuario_activo = None

    def ventanaCatalogo(self):
        if not self._vistaCatalogo or not self._usuario_activo:
            return
        ctrl = ControladorCatalogo(
            self._modelo,
            self._vistaCatalogo,
            correo_usuario=self._usuario_activo.correo,
            tipo_usuario=self._usuario_activo.tipo,
        )
        self._vistaCatalogo.controlador = ctrl
        self._vistaCatalogo.opcion_disponibilidad.setCurrentIndex(0)
        self._vistaCatalogo.opcion_buscador.setCurrentIndex(-1)
        self._vistaCatalogo.show()
