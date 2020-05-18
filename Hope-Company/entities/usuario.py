from werkzeug.security import generate_password_hash, check_password_hash
from entities.cliente import Cliente

class Usuario(Cliente):

    def __init__(self, nome = "", sexo = "", nascimento = "", telefone = "", endereco = "", email = "",  senha_hash = ""):
        super().__init__(nome, sexo, nascimento, telefone, endereco, email)
        self.senha_hash = senha_hash

    @property
    def senha(self):
        raise AttributeError("Senha não pode ser lida")

    @senha.setter
    def senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def verifica_senha(self, senha):
        return check_password_hash(str(self.senha_hash), senha)


