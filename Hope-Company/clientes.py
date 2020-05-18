from flask import Flask, request, render_template
from entities.usuario import Usuario
from entities.produtos import Produto
from entities.pedido import Pedido
from contextlib import closing
import sqlite3

############################
#### Definições da API. ####
############################
u = Usuario()
app = Flask(__name__)


#---------------------------------LOGIN-----------------------------------------------#

@app.route("/", methods = ["GET"])
def form_login():
    return render_template("login.html", usuario = "", senha = "")

@app.route("/", methods = ["POST"])
def login_api():
    u.nome = request.form['usuario']
    u.email = request.form['email']
    senha = request.form['senha']
    usuarios = consultar_usuario(u.nome, u.email)
    print(u.verifica_senha(senha))
    if u.verifica_senha(senha) is True:
        if len(usuarios) > 0:
            return render_template("menu.html", mensagem = f"Bem vindo, {u.nome}")
    return render_template('login.html', mensagem = '<h1>Usuário não está cadastrado</h1>')
#---------------------------------CADASTRO DE NOVO USUARIO-----------------------------------------------#

@app.route("/registrar/novo/", methods = ["GET"])
def form_registrar_novo_usu_api():
    return render_template("form_registrar_usu.html", id_usuario = "novo", email = "", usuario = "", senha = "")

@app.route("/registrar/novo/", methods = ["POST"])
def criar_usuario_api():
    u.email = request.form["email"]
    u.nome = request.form["usuario"]
    u.senha = request.form["senha"]
    inserir_novo_usuario(u.email, u.nome, u.senha_hash)
    return render_template("menu.html", mensagem = "Cadastro efetuado com sucesso")

#---------------------------------LEMBRAR SENHA-----------------------------------------------#

@app.route("/nova/senha", methods = ["GET"])
def form_lembrar_senha_api():
    return render_template("form_lembrar_senha.html",  email = "", usuario = "", senha = "")

@app.route("/nova/senha", methods = ["POST"])
def lembrar_senha_api():
    u.email = request.form["email"]
    u.nome = request.form["usuario"]
    u.senha = request.form["senha"]
    lembrar_senha(u.email, u.nome, u.senha_hash)
    return render_template("login.html", mensagem = "Sua senha foi atualizada")
   
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
    u.nome = request.form["nome"]
    u.sexo = request.form["sexo"]
    u.telefone = request.form["telefone"]
    u.endereco = request.form["endereco"]
    u.email = request.form["email"]
    id_cliente = criar_cliente(u.nome, u.sexo, u.telefone, u.endereco, u.email)
    return render_template("menu.html", mensagem = f"{'O' if u.sexo == 'M' else 'A'} cliente {u.nome} foi criad{'o' if u.sexo == 'M' else 'a'} com o id {id_cliente}.")

@app.route("/cliente/<int:id_cliente>/", methods = ["GET"])
def form_alterar_cliente_api(id_cliente):
    cliente = consultar_cliente(id_cliente)
    if cliente == None:
        return render_template("menu.html", mensagem = f"Esse cliente não existe."), 404
    return render_template("form_cliente.html", id_cliente = id_cliente, nome = cliente['nome'], sexo = cliente['sexo'], telefone = cliente['telefone'], endereco = cliente['endereco'], email = cliente['email'])

@app.route("/cliente/<int:id_cliente>/", methods = ["POST"])
def alterar_cliente_api(id_cliente):
    u.nome = request.form["nome"]
    u.sexo = request.form["sexo"]
    u.telefone = request.form["telefone"]
    u.endereco = request.form["endereco"]
    u.email = request.form["email"]
    cliente = consultar_cliente(id_cliente)
    if cliente == None:
        return render_template("menu.html", mensagem = f"Esse cliente não existe!"), 404
    editar_cliente(id_cliente, u.nome, u.sexo, u.telefone, u.endereco, u.email)
    return render_template("menu.html", mensagem = f"O  cliente {id_cliente} foi editado com sucesso!")


#_______PRODUTOS________#

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
    id_produto = criar_produto(descricao, quantidade, preco_unitario)
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
    return render_template("menu.html", mensagem = f"O produto {produto['descricao']} com o id {id_produto} foi excluído.")


#_______PEDIDO________#

@app.route("/pedido/")
def listar_pedidos_api():
    return render_template("lista_pedidos.html", pedidos = listar_pedidos())

@app.route("/pedido/novo/", methods = ["GET"])
def form_criar_pedido_api():
    return render_template("form_pedido.html", id_pedido = "novo", quantidade = "", status = "", preco = "", clientes = listar_clientes(), produtos = listar_produtos())

@app.route("/pedido/novo/", methods = ["POST"])
def criar_pedido_api():
    quantidade = request.form["quantidade"]
    status = request.form["status"]
    preco = request.form["preco"]
    id_cliente = request.form["id_cliente"]
    id_produto = request.form["id_produto"]
    id_pedido = criar_pedido(quantidade, status, preco, id_cliente, id_produto)
    return render_template("menu.html", mensagem = f"Novo pedido gerado: {id_pedido}!")

@app.route("/pedido/<int:id_pedido>/", methods = ["GET"])
def form_alterar_pedido_api(id_pedido):
    pedido = consultar_pedido(id_pedido)
    if pedido == None:
        return render_template("menu.html", mensagem = f"Esse pedido não existe."), 404
    return render_template("form_pedido.html", id_pedido = id_pedido, id_produto = pedido['id_produto'], quantidade = pedido['quantidade'], status = pedido['status'], preco = pedido['preco'], clientes = listar_clientes(), produtos = listar_produtos())

@app.route("/pedido/<int:id_pedido>/", methods = ["POST"])
def alterar_pedido_api(id_pedido):
    pedido = consultar_pedido(id_pedido)
    quantidade = request.form['quantidade']
    status = request.form['status']
    preco = request.form['preco']
    id_produto = request.form['id_produto']
    if pedido == None:
        return render_template("menu.html", mensagem = f"Esse pedido não existe."), 404
    editar_pedido(preco, quantidade, status, id_produto, id_pedido)
    return render_template("menu.html", mensagem = f"O pedido {id_pedido} foi editado com sucesso!")

@app.route("/pedido/<int:id_pedido>", methods = ["DELETE"])
def deletar_pedido_api(id_pedido):
    pedido = consultar_pedido(id_pedido)
    if pedido == None:
        return render_template("menu.html", mensagem = "Esse pedido nem mesmo existia mais."), 404
    deletar_pedido(id_pedido)
    return render_template("menu.html", mensagem = f"O pedido {id_pedido} foi excluído com sucesso!")

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
CREATE TABLE  IF NOT EXISTS cliente (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(50) NOT NULL,
    sexo VARCHAR(1) NOT NULL,
    telefone CHAR(11) NULL,
    endereco CHAR(100) NULL,
    email CHAR(100) NULL
);

CREATE TABLE IF NOT EXISTS produto (
    id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
    descricao VARCHAR(50) NOT NULL,
    quantidade INTEGER,
    preco_unitario REAl NOT NULL
);

CREATE TABLE IF NOT EXISTS pedido (
    id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
    id_produto INTEGER NOT NULL,
    id_cliente INTEGER NOT NULL,
    preco REAL NOT NULL,
    quantidade INTEGER NOT NULL,
    datahora DATETIME DEFAULT CURRENT_TIME,
    status TINYINT(1),
    FOREIGN KEY(id_produto) REFERENCES produto(id_produto),
    FOREIGN KEY(id_cliente) REFERENCES cliente(id_cliente)
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

#_______CLIENTES________#
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
    
#_________PRODUTOS__________#

def criar_produto(descricao, quantidade, preco_unitario):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO produto (descricao, quantidade, preco_unitario) values(?, ?, ?)", (descricao, quantidade, preco_unitario))
        id_produto = cur.lastrowid
        con.commit()
        return id_produto

def consultar_produto(id_produto):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_produto, descricao, quantidade, preco_unitario FROM produto WHERE id_produto = ?", (id_produto, ))
        return row_to_dict(cur.description, cur.fetchone())

def listar_produtos():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT p.id_produto, p.descricao, p.preco_unitario, p.quantidade FROM produto p ORDER BY p.id_produto")
        return rows_to_dict(cur.description, cur.fetchall())
        
def editar_produto(id_produto, descricao, quantidade, preco_unitario):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("UPDATE produto SET descricao = ?, quantidade = ?, preco_unitario = ? WHERE id_produto = ?", (descricao, quantidade, preco_unitario, id_produto))
        con.commit()

def deletar_produto(id_produto):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("DELETE FROM produto WHERE id_produto = ?", (id_produto, ))
        con.commit()

#_________PEDIDOS__________#

def criar_pedido(quantidade, status, preco, id_cliente, id_produto): 
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO pedido (quantidade, status, preco, id_cliente, id_produto) VALUES (?, ?, ?, ?, ?)", (quantidade, status, preco, id_cliente, id_produto, ))
        id_pedido = cur.lastrowid
        con.commit()
        return id_pedido

def consultar_pedido(id_pedido):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_pedido, id_produto, id_cliente, preco, quantidade, datahora, status FROM pedido p WHERE id_pedido = ?", (id_pedido, ))
        return row_to_dict(cur.description, cur.fetchone())

def listar_pedidos():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_pedido, id_produto, id_cliente, preco, quantidade, datahora, status FROM pedido p ORDER BY p.id_cliente")
        return rows_to_dict(cur.description, cur.fetchall())

def editar_pedido(preco, quantidade, status, id_produto, id_pedido):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("UPDATE pedido SET preco = ?, quantidade = ?, status = ?, id_produto = ? WHERE id_pedido = ?", (preco, quantidade, status, id_produto, id_pedido, ))
        con.commit()    

def deletar_pedido(id_pedido):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("DELETE FROM pedido WHERE id_pedido = ?", (id_pedido, ))
        con.commit()

#_________LOGIN__________#
def inserir_novo_usuario(email, usuario, senha):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO usuario (email, usuario, senha) values (?, ?, ?)", (email, usuario, senha, ))
        id_usuario = cur.lastrowid
        con.commit()
        return id_usuario

def consultar_usuario(usuario, email):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT senha FROM usuario WHERE usuario = ? AND email = ?", (usuario, email, ))
        return cur.fetchone()

def lembrar_senha(usuario, email, senha):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("UPDATE usuario SET senha = ? WHERE usuario = ? AND email = ?", (senha, usuario, email, ))
        con.commit()
########################
#### Inicialização. ####
########################

if __name__ == "__main__":
    criar_bd()
    app.run()
    
