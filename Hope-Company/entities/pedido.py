from entities.cliente import Cliente
class Pedido(Cliente):

    def __init__(self, nome, sexo, nascimento, telefone, endereco, email, preco, quantidade, datahora, status):
        super().__init__(nome, sexo, nascimento, telefone, endereco, email)
        self.preco = preco
        self.quantidade = quantidade
        self.datahora = datahora
        self.status = status
    

    def realiza_pedido(self, items):
        pedidos = []
        pedidos.append(items)
        for pedido in pedidos:
            return pedido
    