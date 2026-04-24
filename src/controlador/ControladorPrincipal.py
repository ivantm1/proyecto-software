from src.modelo.vo.LoginVO import LoginVO

# Para mandar cosas de la vista se debe hacer un metodo en la vista y llamarlo desde el controlador
class ControladorPrincipal:
    def __init__(self, ref_vista, ref_modelo):
        self._vista = ref_vista
        self._modelo = ref_modelo

    def ventanaIniciarSesion(self):
        self._vistaLogin.show()

    def comprobarLogin(self, nombre, passw):
        if not nombre or not passw:
            self._vista.lanzarAviso("Por favor, introduce usuario y contraseña.")
            return
        
        login = LoginVO(nombre, passw)
        # Comprobar si el usuario y contraseñas son adecuados, si no lo son, no se envia nada al modelo
        resultado = self._modelo.consultarLogin(login)
        if resultado is None:
            self._vista.lanzarAviso("Usuario o contraseña incorrecto.")
        else:
            self._vista.lanzarAviso("Inicio de sesión con éxito")
            self._vista.close()

    def ventanaRegistro(self):
        self._vista.show()