from src.modelo.dao.UserDaoJDBC import UserDaoJDBC

class Logica():
    def pruebaSelect(self):
        userDao = UserDaoJDBC()
        usuarios = userDao.select()
        for user in usuarios:
            print(user.nombre_user)

    def comprobarLogin(self, loginVO):                                               
        login_dao = UserDaoJDBC()                                                    
        return login_dao.comprobarLogin(loginVO)                                     
                                                                               
    def registrarUsuario(self, registroVO):                                          
        registro_dao = UserDaoJDBC()                                                 
        return registro_dao.registrarUsuario(registroVO) 
