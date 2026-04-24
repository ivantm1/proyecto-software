from src.modelo.dao.UserDaoJDBC import UserDaoJBDC

class Logica():
    def pruebaSelect(self):
        userDao = UserDaoJBDC()
        usuarios = userDao.select()
        for user in usuarios:
            print(user.__nombre)

    def comprobarLogin(self, LoginVO):
        login_dao = UserDaoJBDC()
        return login_dao.consultarLogin(LoginVO)
    
    def registrarUsuario(self, RegistroVO):
        registro_dao = UserDaoJBDC()
        return registro_dao.registrarUsuario(RegistroVO)