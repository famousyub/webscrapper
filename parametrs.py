


import os 



class Configlink:
    def __init__(self,username,password) -> None:
        self.username = username
        self.password = password
    

    @property
    def getUsername(self):
        return self.username
    
    @property
    def getPaasword (self):
        return self.password


username = ""
password=""



