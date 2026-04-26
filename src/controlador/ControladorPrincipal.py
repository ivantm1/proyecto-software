from src.modelo.vo.LoginVO import LoginVO
from src.modelo.vo.RegistroVO import RegistroVO

# Para mandar cosas de la vista se debe hacer un metodo en la vista y llamarlo desde el controlador
class ControladorPrincipal:
    def __init__(self, ref_modelo, ref_login, ref_vista_registro=None,ref_vista_estudiante=None):
        self._vistaLogin = ref_login
        self._modelo = ref_modelo
        self._vistaRegistro = ref_vista_registro
        self._vistaEstudiante = ref_vista_estudiante

    def ventanaIniciarSesion(self):
        self._vistaLogin.show()

    def comprobarLogin(self, login):
        if not login.nombre or not login.contrasena:
            self._vistaLogin.lanzarAviso("Por favor, introduce usuario y contraseña.")
            return False
        
        # Comprobar si el usuario y contraseñas son adecuados, si no lo son, no se envia nada al modelo
        resultado = self._modelo.comprobarLogin(login)
        if resultado is None:
            self._vista.lanzarAviso("Usuario o contraseña incorrecto.")
        else:
            self._vistaLogin.close()
            if resultado.tipo == "Estudiante":
                self.ventanaEstudiante()
            elif resultado.tipo == "Bibliotecario":
                self.ventanaBibliotecario()
            elif resultado.tipo == "Admin":
                self.ventanaAdmin()

    def ventanaRegistro(self):
        if self._vistaRegistro:
            self._vistaLogin.close()
            self._vistaRegistro.show()

    def ventanaEstudiante(self):
        print(f"_vistaEstudiante vale: {self._vistaEstudiante}")
        if self._vistaEstudiante:
            print("Abriendo vista estudiante")
            self._vistaEstudiante.show()
            print("Abriendo vista estudiante222")

    def ventanaBibliotecario(self):
        if self._vistaBibliotecario:

            self._vistaBibliotecario.show()

    def ventanaAdmin(self):
        if self._vistaAdmin:

            self._vistaAdmin.show()

    def registrarUsuario(self, nombre, apellidos, correo, contrasena, confirmar_contrasena):
        if not nombre or not apellidos or not correo or not contrasena or not confirmar_contrasena:
            self._vistaLogin.lanzarAviso("Por favor, rellena todos los campos.")
            return
        
        if "@estudiantes.unileon.es" not in correo:
            self._vistaLogin.lanzarAviso("Por favor, utilice un correo institucional.")
            return

        if contrasena != confirmar_contrasena:
            self._vistaLogin.lanzarAviso("Las contraseñas no coinciden.")
            return
        
        registro = RegistroVO(nombre, apellidos, correo, contrasena)
        # Comprobar si el usuario y contraseñas son adecuados, si no lo son, no se envia nada al modelo
        resultado = self._modelo.registrarUsuario(registro)
        if resultado:
            self._vistaLogin.lanzarAviso("Usuario registrado con éxito")
            self._vistaLogin.close()
        else:
            self._vistaLogin.lanzarAviso("Error al registrarse.")
