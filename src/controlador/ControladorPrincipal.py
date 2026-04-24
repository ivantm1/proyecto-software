from src.modelo.vo.LoginVO import LoginVO
from src.modelo.vo.RegistroVO import RegistroVO

# Para mandar cosas de la vista se debe hacer un metodo en la vista y llamarlo desde el controlador
class ControladorPrincipal:
    def __init__(self, ref_vista, ref_modelo):
        self._vista = ref_vista
        self._modelo = ref_modelo

    def ventanaIniciarSesion(self):
        self._vistaLogin.show()

    def comprobarLogin(self, nombre, contrasena):
        if not nombre or not contrasena:
            self._vista.lanzarAviso("Por favor, introduce usuario y contraseña.")
            return
        
        login = LoginVO(nombre, contrasena)
        # Comprobar si el usuario y contraseñas son adecuados, si no lo son, no se envia nada al modelo
        resultado = self._modelo.comprobarLogin(login)
        if resultado is None:
            self._vista.lanzarAviso("Usuario o contraseña incorrecto.")
        else:
            self._vista.lanzarAviso("Inicio de sesión con éxito")
            self._vista.close()

    def ventanaRegistro(self):
        self._vistaRegistro.show()

    def registrarUsuario(self, nombre, apellidos, correo, contrasena, confirmar_contrasena):
        if not nombre or not apellidos or not correo or not contrasena or not confirmar_contrasena:
            self._vista.lanzarAviso("Por favor, rellena todos los campos.")
            return
        
        if "@estudiantes.unileon.es" not in correo:
            self._vista.lanzarAviso("Por favor, utilice un correo institucional.")
            return

        if contrasena != confirmar_contrasena:
            self._vista.lanzarAviso("Las contraseñas no coinciden.")
            return
        
        registro = RegistroVO(nombre, apellidos, correo, contrasena)
        # Comprobar si el usuario y contraseñas son adecuados, si no lo son, no se envia nada al modelo
        resultado = self._modelo.registrarUsuario(registro)
        if resultado:
            self._vista.lanzarAviso("Usuario registrado con éxito")
            self._vista.close()
        else:
            self._vista.lanzarAviso("Error al registrarse.")