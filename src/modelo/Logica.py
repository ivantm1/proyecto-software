from src.modelo.dao.UserDaoJDBC import UserDaoJDBC
from src.modelo.dao.LibroDaoJDBC import LibroDaoJDBC

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
    
    def buscar_libros(self, linea_busqueda, tema):
        libros_dao = LibroDaoJDBC()
        lista = libros_dao.buscarLibros(linea_busqueda, tema)
        if len(lista)==0:
            return None
        else:
            return lista