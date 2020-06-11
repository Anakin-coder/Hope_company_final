from flask import Flask, request, render_template, session, redirect
from entities.usuario import Usuario
from entities.produtos import Produto
from entities.pedido import Pedido
from contextlib import closing
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

############################
#### Definições da API. ####
############################
app = Flask(__name__)
#---------------------------------LOGIN-----------------------------------------------#

@app.route("/", methods = ["GET"])
def form_login():
    return render_template("login.html", usuario = "", senha = "")

@app.route("/", methods = ["POST"])
def login_api():
    nome = request.form['usuario']
    senha = request.form['senha']
    u = consultar_usuario(nome)
    if u is None:
        return render_template('login.html', mensagem = 'Usuário não está cadastrado')
    if u.verifica_senha(senha):
        return render_template("menu.html", mensagem = "Bem vindo, {}".format(str(nome).capitalize()))
    return render_template('login.html', mensagem = 'Senha incorreta')

#---------------------------------CADASTRO DE NOVO USUARIO-----------------------------------------------#

@app.route("/registrar/novo/", methods = ["GET"])
def form_registrar_novo_usu_api():
    return render_template("form_registrar_usu.html", id_usuario = "novo", email = "", usuario = "", senha = "")

@app.route("/registrar/novo/", methods = ["POST"])
def criar_usuario_api():
    email = request.form["email"]
    nome = request.form["usuario"]
    senha = request.form["senha"]
    inserir_novo_usuario(email, nome, senha)
    return render_template("menu.html", mensagem = "Cadastro efetuado com sucesso")
   
#---------------------------------MENU-----------------------------------------------#
@app.route("/menu/")
def menu():
    return render_template("menu.html", mensagem = "")

#---------------------------------CLIENTES-----------------------------------------------#
@app.route("/cliente/")
def listar_clientes_api():
    return render_template("lista_clientes.html", clientes = listar_clientes())

@app.route("/cliente/novo/", methods = ["GET"])
def form_criar_cliente_api():
    return render_template("form_cliente.html", id_cliente = "novo", nome = "", sexo = "", telefone = "", endereco = "", email ="",)

@app.route("/cliente/novo/", methods = ["POST"])
def criar_cliente_api():
    nome = request.form["nome"]
    sexo = request.form["sexo"]
    telefone = request.form["telefone"]
    endereco = request.form["endereco"]
    email = request.form["email"]
    id_cliente = criar_cliente(nome, sexo, telefone, endereco, email)
    return render_template("menu.html", mensagem = f"{'O' if sexo == 'M' else 'A'} cliente {nome} foi criad{'o' if sexo == 'M' else 'a'} com o id {id_cliente}.")

@app.route("/cliente/<int:id_cliente>/", methods = ["GET"])
def form_alterar_cliente_api(id_cliente):
    cliente = consultar_cliente(id_cliente)
    if cliente == None:
        return render_template("menu.html", mensagem = f"Esse cliente não existe."), 404
    return render_template("form_cliente.html", id_cliente = id_cliente, nome = cliente['nome'], sexo = cliente['sexo'], telefone = cliente['telefone'], endereco = cliente['endereco'], email = cliente['email'])

@app.route("/cliente/<int:id_cliente>/", methods = ["POST"])
def alterar_cliente_api(id_cliente):
    nome = request.form["nome"]
    sexo = request.form["sexo"]
    telefone = request.form["telefone"]
    endereco = request.form["endereco"]
    email = request.form["email"]
    cliente = consultar_cliente(id_cliente)
    if cliente == None:
        return render_template("menu.html", mensagem = f"Esse cliente não existe!"), 404
    editar_cliente(id_cliente, nome, sexo, telefone, endereco, email)
    return render_template("menu.html", mensagem = f"O  cliente {id_cliente} foi editado com sucesso!")


#---------------------------------PRODUTO-----------------------------------------------#

@app.route("/produto/")
def listar_produtos_api():
    return render_template("lista_produtos.html", produtos = listar_produtos())

@app.route("/produto/novo/", methods = ["GET"])
def form_criar_produto_api():
    return render_template("form_produto.html", id_produto = "novo", descricao = "", quantidade = "", preco_unitario = "")

@app.route("/produto/novo/", methods = ["POST"])
def criar_produto_api():
    descricao = request.form["descricao"]
    quantidade = request.form["quantidade"]
    preco_unitario = request.form["preco_unitario"]
    id_produto = criar_produto(descricao, preco_unitario)
    cadastra_prod_estoque(id_produto, quantidade)
    return render_template("menu.html", mensagem = f"Novo produto criado: {id_produto}.")

@app.route("/produto/<int:id_produto>/", methods = ["GET"])
def form_alterar_produto_api(id_produto):
    produto = consultar_produto(id_produto)
    if produto == None:
        return render_template("menu.html", mensagem = f"Esse produto não existe."), 404
    return render_template("form_produto.html", id_produto = id_produto, descricao = produto['descricao'], quantidade = produto['quantidade'], preco_unitario = produto['preco_unitario'])

@app.route("/produto/<int:id_produto>/", methods = ["POST"])
def alterar_produto_api(id_produto):
    descricao = request.form["descricao"]
    quantidade = request.form["quantidade"]
    preco_unitario = request.form["preco_unitario"]
    produto = consultar_produto(id_produto)
    if produto == None:
        return render_template("menu.html", mensagem = f"Esse produto não existe."), 404
    editar_produto(id_produto, descricao, quantidade, preco_unitario)
    return render_template("menu.html", mensagem = f"O produto {id_produto} foi editado com sucesso!")

@app.route("/produto/<int:id_produto>", methods = ["DELETE"])
def deletar_produto_api(id_produto):
    produto = consultar_produto(id_produto)
    if produto == None:
        return render_template("menu.html", mensagem = "Esse produto nem mesmo existia mais."), 404
    deletar_produto(id_produto)
    #deletar_produto_estoque(id_produto)
    return render_template("menu.html", mensagem = f"O produto {produto['descricao']} com o id {id_produto} foi excluído.")

#---------------------------------PEDIDO-----------------------------------------------#

@app.route("/pedido/")
def listar_pedidos_api():
    return render_template("lista_pedidos.html", pedidos = listar_pedidos())

@app.route("/pedido/novo/", methods = ["GET"])
def form_criar_pedido_api():
    return render_template("form_pedido.html", id_pedido = "novo", clientes = listar_clientes())

@app.route("/pedido/novo/", methods = ["POST"])
def realiza_pedido_api():
    cliente = request.form["cliente"]
    pedido = "{}".format(request.form["pedido"])
    lista_ped = separaPedido(pedido)
    prod_id = retorna_id_produto(lista_ped)
    produto = consultar_produto_pedido(prod_id)
    quantidade = retorna_quant_produto(lista_ped)
    res = add_quantidade(produto, quantidade)
    total = preco_venda(soma_total(res))
    return render_template("confirma_pedido.html", id_pedido = "novo", cliente = cliente,  produtos = res, quantidade = quantidade, total = total, prod_id = prod_id)


@app.route("/pedido/confirmar/novo", methods = ["POST"])
def confirma_pedido_api():
    id_pedido = request.form["cliente"]
    cliente = request.form ["cliente"]
    produto = request.form.getlist("produto")
    quantidade_estoque = request.form.getlist("quantidade_estoque")
    quantidade_pedida = request.form.getlist("quantidade")
    status = request.form["pagamento"]
    total = request.form["total"]
    preco_un = request.form["valor"]
    id_produto = request.form["id_produto"]
    id_pedido = criar_pedido(cliente, total, status)
    id_produto = int(id_produto[2])
    x = 0
    while x < len(produto):
        atualiza_quantidade(id_produto, quantidade_pedida[x])
        x += 1
    return render_template("menu.html", mensagem = "")


@app.route("/pedido/<int:id_pedido>/", methods = ["GET"])
def form_alterar_pedido_api(id_pedido):
    pedido = consultar_pedido(id_pedido)
    if pedido == None:
        return render_template("menu.html", mensagem = f"Esse pedido não existe."), 404
    return render_template("form_pedido.html", id_pedido = id_pedido, id_produto = pedido['id_produto'], quantidade = pedido['quantidade'], status = pedido['status'], preco = pedido['preco'], clientes = listar_clientes(), produtos = listar_produtos())

@app.route("/pedido/<int:id_pedido>/", methods = ["POST"])
def alterar_pedido_api(id_pedido):
    pedido = consultar_pedido(id_pedido)
    status = request.form['status']
    if pedido == None:
        return render_template("menu.html", mensagem = f"Esse pedido não existe."), 404
    editar_pedido(status, id_pedido)
    return render_template("menu.html", mensagem = f"O pedido {id_pedido} foi editado com sucesso!")

@app.route("/pedido/<int:id_pedido>", methods = ["DELETE"])
def deletar_pedido_api(id_pedido):
    pedido = consultar_pedido(id_pedido)
    if pedido == None:
        return render_template("menu.html", mensagem = "Esse pedido nem mesmo existia mais."), 404
    deletar_pedido(id_pedido)
    return render_template("menu.html", mensagem = f"O pedido {id_pedido} foi excluído com sucesso!")
#------------------FUNÇÕES AUXILIARES----------------#
def separaPedido(texto):
    lista = []
    for linha in texto.split("' '"):
        lista.append(linha)
        for i in range(len(lista)):
            novalista = lista[i].split("\r\n")
    x = 0
    dic = {}
    outralista = []
    while x < len(novalista):
        dic["id"] = novalista[x][0:1]
        dic["quantidade"] = novalista[x][2:]
        outralista.append(dic.copy())
        x += 1
    return outralista

def retorna_id_produto(lista_ped):
    x = 0
    id = []
    while x < len(lista_ped):
        id.append(lista_ped[x]["id"])
        x+=1
    return id

def retorna_quant_produto(lista_ped):
    x = 0
    quantidade = []
    while x < len(lista_ped):
        quantidade.append(lista_ped[x]["quantidade"])
        x+=1
    return quantidade

def add_quantidade(produto, quantidade):
    x = 0
    lista_prod = []
    res = []
    while x < len(produto):
        lista_prod = list(produto[x]).copy()
        lista_quat = int(quantidade[x])
        lista_prod.append(lista_quat)
        res.append(lista_prod)
        x += 1
    return res

def soma_total(res):
    soma = 0
    for total in res:
        soma += total[3] * total[4]
    return soma

def preco_venda(preco_unitario):
    preco_venda = preco_unitario * 1
    return preco_venda
#---------------------------------ITENS PEDIDO-----------------------------------------------#
@app.route("/produto/pedido/", methods = ["GET"])
def form_prod_pedido_api():
    return render_template("form_produto_pedido.html", preco = "", quantidade = "", descrica = "", id_pedido = "", preco_unitario = "", produtos = listar_produtos(), pedidos = listar_pedidos())
 
@app.route("/produto/pedido/", methods = ["POST"])
def criar_prod_pedido_api():
    preco = request.form['preco']
    quantidade = request.form['quantidade']
    descricao = request.form['descricao']
    id_pedido = request.form['id_pedido']
    preco_unitario = request.form['preco_unitario']
    descricao = request.form['descricao']
    criar_prod_pedido(preco, quantidade, descricao, id_pedido, preco_unitario, descricao)
    return render_template('menu.html', mensagem = 'Pedido realizado com sucesso')

###############################################
#### Funções auxiliares de banco de dados. ####
###############################################

# Converte uma linha em um dicionário.
def row_to_dict(description, row):
    if row == None:
        return None
    d = {}
    for i in range(0, len(row)):
        d[description[i][0]] = row[i]
    return d

# Converte uma lista de linhas em um lista de dicionários.
def rows_to_dict(description, rows):
    result = []
    for row in rows:
        result.append(row_to_dict(description, row))
    return result


####################################
#### Definições básicas de DAO. ####
####################################
#  IF NOT EXISTS
sql_create = """
CREATE TABLE IF NOT EXISTS cliente (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(50) NOT NULL,
    sexo VARCHAR(1) NOT NULL,
    telefone CHAR(11) NULL,
    endereco CHAR(100) NULL,
    email CHAR(100) NULL
);

CREATE TABLE IF NOT EXISTS pedido (
    id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER NOT NULL,
    datahora DEFAULT CURRENT_DATE,
    ped_valor INTEGER,
    status VARCHAR(20),
    FOREIGN KEY(id_cliente) REFERENCES cliente(id_cliente)
);

CREATE TABLE IF NOT EXISTS itens_pedido (
    id_produto INTEGER NOT NULL,
    id_pedido INTEGER NOT NULL,
    preco REAL NOT NULL,
    preco_unitario REAL NOT NULL,
    quantidade INTEGER NOT NULL,
    FOREIGN KEY(id_produto) REFERENCES produto(id_produto),
    FOREIGN KEY(id_pedido) REFERENCES pedido(id_pedido)
);

CREATE TABLE IF NOT EXISTS produto (
    id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
    descricao VARCHAR(50) NOT NULL,
    preco_unitario REAl NOT NULL
);

CREATE TABLE IF NOT EXISTS estoque (
    id_estoque INTEGER PRIMARY KEY AUTOINCREMENT,
    id_produto VARCHAR(50) NOT NULL,
    quantidade INTEGER,
    FOREIGN KEY(id_produto) REFERENCES produto(id_produto)
);

CREATE TABLE IF NOT EXISTS usuario (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(50),
    usuario VARCHAR(50),
    senha  VARCHAR2(100)
);
"""

def conectar():
    return sqlite3.connect('clientes.db')

def criar_bd():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        criar_bd
        cur.executescript(sql_create)
        con.commit()

#------------------------CLIENTES---------------------#
def criar_cliente(nome, sexo, telefone, endereco, email):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO cliente (nome, sexo, telefone, endereco, email) VALUES (?, ?, ?, ?, ?)", (nome, sexo, telefone, endereco, email))
        id_cliente = cur.lastrowid
        con.commit()
        return id_cliente

def consultar_cliente(id_cliente):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_cliente, nome, sexo, telefone, endereco, email FROM cliente WHERE id_cliente = ?", (id_cliente, ))
        return row_to_dict(cur.description, cur.fetchone())

def listar_clientes():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_cliente, nome, sexo, telefone, endereco, email FROM cliente ORDER BY id_cliente")
        return rows_to_dict(cur.description, cur.fetchall())


def editar_cliente(id_cliente, nome, sexo, telefone, endereco, email):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("UPDATE cliente SET nome = ?, sexo = ?, telefone = ?, endereco = ?, email = ? WHERE id_cliente = ?", (nome, sexo, telefone, endereco, email, id_cliente))
        con.commit()

def deletar_cliente(id_cliente):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("DELETE FROM cliente WHERE id_cliente = ?", (id_cliente, ))
        con.commit()

#--------------------PRODUTO------------------------#    

def criar_produto(descricao, preco_unitario):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO produto (descricao, preco_unitario) values(?, ?)", (descricao, preco_unitario))
        id_produto = cur.lastrowid
        con.commit()
        return id_produto

def consultar_produto(id_produto):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_produto, descricao, quantidade, preco_unitario FROM produto WHERE id_produto = ?", (id_produto, ))
        return row_to_dict(cur.description, cur.fetchone())

def listar_produtos():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT p.id_produto, p.descricao, p.preco_unitario, e.quantidade FROM produto p INNER JOIN estoque e ON p.id_produto = e.id_produto ORDER BY p.id_produto")
        return rows_to_dict(cur.description, cur.fetchall())
        
def editar_produto(id_produto, descricao, quantidade, preco_unitario):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("UPDATE produto SET descricao = ?, quantidade = ?, preco_unitario = ? WHERE id_produto = ?", (descricao, quantidade, preco_unitario, id_produto))
        con.commit()

def deletar_produto(id_produto):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("DELETE FROM produto WHERE id_produto = ?", (id_produto, ))
        con.commit()
#--------------------ESTOQUE------------------------#    
def cadastra_prod_estoque(id_produto, quantidade):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute(f"INSERT INTO estoque (id_produto, quantidade) SELECT {id_produto}, {quantidade} FROM produto p WHERE NOT EXISTS (SELECT 1 FROM estoque e WHERE p.id_produto = e.id_produto)")
        id_estoque = cur.lastrowid
        con.commit()
        return id_estoque

def verifica_quantidade(id_produto):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute(f"SELECT quantidade FROM estoque WHERE id_produto = {id_produto}")
        return row_to_dict(cur.description, cur.fetchone())

def atualiza_quantidade(id_produto, quantidade_pedida):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("UPDATE estoque SET quantidade = quantidade - ? WHERE id_produto = ?", (quantidade_pedida, id_produto, ))
        con.commit()
#--------------------PEDIDOS-----------------------#

def criar_pedido(id_cliente, total, status): 
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO pedido (id_cliente, ped_valor, status) VALUES (?, ?, ?)", (id_cliente, total, status))
        id_pedido = cur.lastrowid
        con.commit()
        return id_pedido

def consultar_pedido(id_pedido):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_pedido, id_cliente, datahora, status FROM pedido p WHERE id_pedido = ?", (id_pedido, ))
        return row_to_dict(cur.description, cur.fetchone())

def listar_pedidos():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT p.id_pedido, p.id_cliente, p.datahora, p.status, c.nome FROM pedido p INNER JOIN cliente c ON p.id_cliente = c.id_cliente ORDER BY p.id_cliente")
        return rows_to_dict(cur.description, cur.fetchall())

def consultar_produto_pedido(id_produto):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        query = f"SELECT p.id_produto, p.descricao, e.quantidade, p.preco_unitario FROM produto p INNER JOIN estoque e ON e.id_produto = p.id_produto WHERE p.id_produto in ({','.join(['?']*len(id_produto))})"
        cur.execute(query, id_produto)
        return cur.fetchall()

def editar_pedido(status, id_pedido):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("UPDATE pedido SET status = ? WHERE id_pedido = ?", (status, id_pedido, ))
        con.commit()    

def deletar_pedido(id_pedido):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("DELETE FROM pedido WHERE id_pedido = ?", (id_pedido, ))
        con.commit()

#--------------------LOGIN------------------#

def inserir_novo_usuario(email, usuario, senha):
    senha_hash = generate_password_hash(senha)
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO usuario (email, usuario, senha) values (?, ?, ?)", (email, usuario, senha_hash, ))
        id_usuario = cur.lastrowid
        con.commit()
        return id_usuario

def consultar_usuario(usuario):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_usuario, usuario, email, senha FROM usuario WHERE usuario = ?", (usuario, ))
        u = row_to_dict(cur.description, cur.fetchone())
        if u is None:
            return None
        return Usuario(u['id_usuario'], u['usuario'], u['email'], u['senha'])

#--------------------ITENS PEDIDO------------------#
'''preco, quantidade, descricao, id_pedido, preco_unitario'''
def criar_prod_pedido(preco, quantidade, descricao, id_pedido, preco_unitario, id_produto): 
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO itens_pedido (i.preco, i.quantidade, p.descricao, i.id_pedido, i.id_produto) SELECT (?, ?, ?, ?, ?) FROM itens_pedido i LEFT JOIN produto p WHERE p.id_produto = i.id_produto", ())
        con.commit()

def consultar_prod_pedido(id_pedido):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT preco, quantidade, id_produto, id_pedido FROM itens_pedido p WHERE id_pedido = ?", (id_pedido, ))
        return row_to_dict(cur.description, cur.fetchone())

def listar_itens_pedido():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT i.preco, i.quantidade, i.id_produto, i.id_pedido, i.preco_unitario, p.descricao from itens_pedido i INNER JOIN produto p ON i.id_produto= p.id_produto")
        return row_to_dict(cur.description, cur.fetchone())


########################
#### Inicialização. ####
########################

if __name__ == "__main__":
    criar_bd()
    app.run()
    
