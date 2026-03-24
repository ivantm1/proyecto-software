from src.modelo.dao.UserDaoJDBC import UserDaoJBDC

class Logica():
    def ejemploSelect(self):
        userDao = UserDaoJBDC()
        usuarios = userDao.select()
        for user in usuarios:
            print(user.__nombre)