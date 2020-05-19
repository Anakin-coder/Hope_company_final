from werkzeug.security import generate_password_hash, check_password_hash
from entities.cliente import Cliente

class Usuario():

    def __init__(self, id_usuario, usuario, email, senha):
        self.id_usuario = id_usuario
        self.usuario = usuario
        self.email = email
        self.senha = senha
  
    def verifica_senha(self, senha):
        return check_password_hash(str(self.senha), senha)


