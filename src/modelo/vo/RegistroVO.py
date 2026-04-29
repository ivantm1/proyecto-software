class RegistroVO:
    def __init__(self, nombre, apellidos, correo, contrasena):                              
        self._nombre = nombre                                                               
        self._apellidos = apellidos                                                         
        self._correo = correo                                                               
        self._contrasena = contrasena
            
    @property                                                                               
    def nombre(self): 
        return self._nombre                                                   
    
    @property                                                                               
    def apellidos(self): 
        return self._apellidos                                             
    
    @property                                                                               
    def correo(self): 
        return self._correo                                                   
    
    @property                                                                               
    def contrasena(self): 
        return self._contrasena