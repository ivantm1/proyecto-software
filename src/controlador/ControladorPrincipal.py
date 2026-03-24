from src.modelo.vo.LoginVO import LoginVO

# Para mandar cosas de la vista se debe hacer un metodo en la vista y llamarlo desde el controlador
class ControladorPrincipal:
    def __init__(self, ref_vista, ref_modelo):
        self._vista = ref_vista
        self._modelo = ref_modelo

    def ventanaIniciarSesion(self):
        self._vista.show()

    def comprobarLogin(self, nombre, passw):
        login = LoginVO(nombre, passw)
        # Comprobar si el usuario y contraseñas son adecuados, si no lo son, no se envia nada al modelo
        resultado = self._modelo.consultarLogin(login)
        self._vista.lanzarAviso("Usuario o contraseña incorrecto")

        if resultado == None:
            print("No existe")
        else:
            self._vista.close()