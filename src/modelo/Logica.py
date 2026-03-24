from src.modelo.dao.UserDaoJDBC import UserDaoJBDC

class Logica():
    def pruebaSelect(self):
        userDao = UserDaoJBDC()
        usuarios = userDao.select()
        for user in usuarios:
            print(user.__nombre)

    def comprobarLogin(self, loginVO):
        login_dao = UserDaoJBDC()
        return login_dao.consultarLogin(loginVO)