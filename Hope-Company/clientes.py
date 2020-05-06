from flask import Flask, request, render_template
from contextlib import closing
import sqlite3

############################
#### Definições da API. ####
############################

app = Flask(__name__)


#_______LOGIN________#

@app.route("/")
def login():
    return render_template("login.html", mensagem = "")

@app.route("/menu/")
def menu():
    return render_template("menu.html", mensagem = "")


#_______CLIENTES________#

@app.route("/cliente/")
def listar_clientes_api():
    return render_template("lista_clientes.html", clientes = listar_clientes())

@app.route("/cliente/novo/", methods = ["GET"])
def form_criar_cliente_api():
<<<<<<< HEAD
    return render_template("form_cliente.html", id_cliente = "novo", nome = "", sexo = "", telefone = "", endereco = "", email ="",)
=======
    return render_template("form_cliente.html", id_cliente = "novo", nome = "", sexo = "", telefone = "", endereco = "", email = "")
>>>>>>> e194429e570e9255bcb03511a0e708b5677bb314

@app.route("/cliente/novo/", methods = ["POST"])
def criar_cliente_api():    
    nome = request.form["nome"]
    sexo = request.form["sexo"]
    telefone = request.form["telefone"]
    endereco = request.form["endereco"]
<<<<<<< HEAD
    endereco = request.form["email"]
    id_cliente = criar_cliente(nome, sexo, telefone, endereco, email)
    return render_template("menu.html", mensagem = f"{'O' if sexo == 'M' else 'A'} cliente {nome} foi criad{'o' if sexo == 'M' else 'a'} com o id {id_cliente}.")
=======
    email = request.form["email"]
    id_cliente = criar_cliente(nome, sexo, telefone, endereco, email)
    cliente = consultar_cliente(id_cliente)
    if cliente == None:
        return render_template("menu.html", mensagem = f"Cliente já cadastrado!"), 404
    return render_template("menu.html", mensagem = f"Novo cliente criado: {id_cliente}.")
>>>>>>> e194429e570e9255bcb03511a0e708b5677bb314

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


#_______PRODUTOS________#

@app.route("/produto/")
def listar_produtos_api():
    return render_template("lista_produtos.html", produtos = listar_produtos())

@app.route("/produto/novo/", methods = ["GET"])
def form_criar_produto_api():
    return render_template("form_produto.html", id_produto = "novo", descricao = "", quantidade = "", preco = "", cores = "")

@app.route("/produto/novo/", methods = ["POST"])
def criar_produto_api():
    descricao = request.form["descricao"]
    quantidade = request.form["quantidade"]
    preco = request.form["preco"]
    cores = request.form["cores"]
    id_produto = criar_produto(descricao, quantidade, preco, cores)
    return render_template("menu.html", mensagem = f"Novo produto criado: {id_produto}.")

@app.route("/produto/<int:id_produto>/", methods = ["GET"])
def form_alterar_produto_api(id_produto):
    produto = consultar_produto(id_produto)
    if produto == None:
        return render_template("menu.html", mensagem = f"Esse produto não existe."), 404
    return render_template("form_produto.html", id_produto = id_produto, descricao = produto['descricao'], quantidade = produto['quantidade'], preco = produto['preco'], cores = produto['cores'])

@app.route("/produto/<int:id_produto>/", methods = ["POST"])
def alterar_produto_api(id_produto):
    descricao = request.form["descricao"]
    quantidade = request.form["quantidade"]
    preco = request.form["preco"]
    cores = request.form["cores"]
    produto = consultar_produto(id_produto)
    if produto == None:
        return render_template("menu.html", mensagem = f"Esse produto não existe."), 404
    editar_produto(id_produto, descricao, quantidade, preco, cores)
    return render_template("menu.html", mensagem = f"O produto {id_produto} foi editado com sucesso!")

@app.route("/produto/<int:id_produto>/", methods = ["DELETE"])
def deletar_produto_api(id_produto):
    produto = consultar_produto(id_produto)
    if produto == None:
        return render_template("menu.html", mensagem = "Esse produto nem mesmo existia mais."), 404
    deletar_produto(id_produto)
    return render_template("menu.html", mensagem = f"O produto {id_produto} foi excluído com sucesso!")


#_______PEDIDO________#


@app.route("/pedido/")
def listar_pedidos_api():
    return render_template("lista_pedidos.html", pedidos = listar_pedidos())

@app.route("/pedido/novo/", methods = ["GET"])
def form_criar_pedido_api():
    return render_template("form_pedidos.html", id_pedido = "novo", id_cliente = "", cpf_cliente = "", descricao = "",  quantidade = "", cores = "", datahora = "", status = "")

@app.route("/pedido/novo/", methods = ["POST"])
def criar_pedido_api():
    cpf_cliente = request.form["cpf"]
    descricao = request.form["descricao"]
    quantidade = request.form["quantidade"]
    cores = request.form["cores"]
    datahora = request.form["datahora"]
    status = request.form["status"]
    id_pedido = criar_pedido(cpf_cliente, descricao, quantidade, cores, datahora, status)
    return render_template("menu.html", mensagem = f"Novo pedido gerado: {id_pedido}!")

@app.route("/pedido/<int:id_pedido>/", methods = ["GET"])
def form_alterar_pedido_api(id_pedido):
    pedido = consultar_pedido(id_pedido)
    if pedido == None:
        return render_template("menu.html", mensagem = f"Esse pedido não existe."), 404
    return render_template("form_pedido.html", id_pedido = id_pedido, cpf_cliente = pedido['cpf_cliente'], descricao = pedido['descricao'], quantidade = pedido['quantidade'], cores = pedido['preco'], datahora = pedido['datahora'], status = pedido['status'])

@app.route("/pedido/<int:id_pedido>/", methods = ["POST"])
def alterar_pedido_api(id_pedido):
    #cpf_cliente = request.form["cpf"]
    descricao = request.form["descricao"]
    quantidade = request.form["quantidade"]
    cores = request.form["cores"]
    status = request.form["status"]
    pedido = consultar_pedido(id_pedido)
    if pedido == None:
        return render_template("menu.html", mensagem = f"Esse pedido não existe."), 404
    editar_pedido(id_pedido, descricao, quantidade, cores, status)
    return render_template("menu.html", mensagem = f"O pedido {id_pedido} foi editado com sucesso!")

@app.route("/pedido/<int:id_pedido>/", methods = ["DELETE"])
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
<<<<<<< HEAD
#  IF NOT EXISTS
'''

CREATE TABLE IF NOT EXISTS pedido (
    id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER NOT NULL,
    datahora DATETIME NOT NULL,
    pago TINYINT(1),
    FOREIGN KEY(id_cliente) REFERENCES cliente(id_cliente)
);
CREATE TABLE  IF NOT EXISTS produto_pedido (
    id_produto INTEGER PRIMARY KEY,
    id_pedido INTEGER PRIMARY KEY,
    preco_unitario REAL NOT NULL,
    quantidade INTEGER NOT NULL,
    FOREIGN KEY(id_produto) REFERENCES produto(id_produto),
    FOREIGN KEY(id_pedido) REFERENCES pedido(id_pedido)
);

'''

sql_create = """
CREATE TABLE  IF NOT EXISTS cliente (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(50) NOT NULL,
    sexo VARCHAR(1) NOT NULL,
    telefone CHAR(11) NULL,
    endereco CHAR(100) NULL,
    email CHAR(100) NULL
=======
#  IF NOT EXISTS  #


sql_create = """
CREATE TABLE IF NOT EXISTS cliente (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(50),
    sexo VARCHAR(1),
    telefone CHAR(11),
    endereco CHAR(100),
    email CHAR(100) 
>>>>>>> e194429e570e9255bcb03511a0e708b5677bb314
);

CREATE TABLE IF NOT EXISTS produto (
    id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
    descricao VARCHAR(50) NOT NULL,
<<<<<<< HEAD
    preco REAl NOT NULL
=======
    quantidade INT,
    preco REAL,
    cores VARCHAR(50) NOT NULL

);
CREATE TABLE IF NOT EXISTS pedido (
    id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER NOT NULL,
    cpf_cliente INTERGER NOT NULL,
    descricao_produto VARCHAR NOT NULL,
    quantidade  INTERGER NOT NULL,
    cores VARCHAR(50) NOT NULL
    datahora DATETIME NOT NULL,
    status TINYINT(1),
    FOREIGN KEY(id_cliente) REFERENCES cliente(id_cliente)
>>>>>>> e194429e570e9255bcb03511a0e708b5677bb314
);
CREATE TABLE IF NOT EXISTS produto_pedido (
    id_produto INTEGER PRIMARY KEY,
    id_pedido INTEGER,
    preco_unitario REAL NOT NULL,
    quantidade INTEGER NOT NULL,
    FOREIGN KEY(id_produto) REFERENCES produto(id_produto),
    FOREIGN KEY(id_pedido) REFERENCES pedido(id_pedido)
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

#def listar_clientes_ordem():
#    with closing(conectar()) as con, closing(con.cursor()) as cur:
#        cur.execute("SELECT id_cliente, nome, sexo, telefone, endereco, email FROM cliente ORDER BY nome")
#        return rows_to_dict(cur.description, cur.fetchall())

def editar_cliente(id_cliente, nome, sexo, telefone, endereco, email):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
<<<<<<< HEAD
        cur.execute("SELECT id_cliente, nome, sexo, telefone, endereco, email FROM cliente ORDER BY nome")
        return rows_to_dict(cur.description, cur.fetchall())
=======
        cur.execute("UPDATE cliente SET nome = ?, sexo = ?, telefone = ?, endereco = ?, email = ? WHERE id_cliente = ?", (nome, sexo, telefone, endereco, email, id_cliente))
        con.commit()
>>>>>>> e194429e570e9255bcb03511a0e708b5677bb314

def deletar_cliente(id_cliente):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("DELETE FROM cliente WHERE id_cliente = ?", (id_cliente, ))
        con.commit()


    
#_________PRODUTOS__________#

def criar_produto(descricao, quantidade, preco, cores):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
<<<<<<< HEAD
        cur.execute("SELECT id_cliente, nome, sexo, telefone, endereco, email FROM cliente WHERE id_cliente = ?", (id_cliente, ))
        return row_to_dict(cur.description, cur.fetchone())

def consultar_produto(id_produto):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT p.id_produto, p.descricao, p.preco FROM produto p INNER JOIN cliente c ON p.id_cliente = c.id_cliente WHERE id_produto = ?", (id_produto, ))
=======
        cur.execute("INSERT INTO produto (descricao, quantidade, preco, cores) VALUES (?, ?, ?, ?)", (descricao, quantidade, preco, cores))
        id_produto = cur.lastrowid
        con.commit()
        return id_produto

def consultar_produto(id_produto):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_produto, descricao, quantidade, preco, cores FROM produto WHERE id_produto = ?", (id_produto, ))
>>>>>>> e194429e570e9255bcb03511a0e708b5677bb314
        return row_to_dict(cur.description, cur.fetchone())

def listar_produtos():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
<<<<<<< HEAD
        cur.execute("SELECT p.id_produto, p.descricao, p.preco FROM produto p INNER JOIN cliente c ON p.id_cliente = c.id_cliente ORDER BY p.id_produto")
        return rows_to_dict(cur.description, cur.fetchall())
        

def criar_cliente(nome, sexo, telefone, endereco, email):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO cliente (nome, sexo, telefone, endereco, email) VALUES (?, ?, ?, ?, ?)", (nome, sexo, telefone, endereco, email))
        id_cliente = cur.lastrowid
=======
        cur.execute("SELECT id_produto, descricao, quantidade, preco, cores FROM produto ORDER BY id_produto")
        return rows_to_dict(cur.description, cur.fetchall())    

#def listar_produtos_ordem():
#    with closing(conectar()) as con, closing(con.cursor()) as cur:
#        cur.execute("SELECT id_produto, descricao, quantidade, preco, cores FROM produto ORDER BY descrição")
#        return rows_to_dict(cur.description, cur.fetchall())

def editar_produto(id_produto, descricao, quantidade, preco, cores):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("UPDATE produto SET descricao = ?, quantidade = ?, preco = ?, cores = ? WHERE id_produto = ?", (descricao, quantidade, preco, cores, id_produto))
>>>>>>> e194429e570e9255bcb03511a0e708b5677bb314
        con.commit()

<<<<<<< HEAD
def criar_produto(descricao, id_cliente, preco):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO produto (descricao, id_cliente, preco) VALUES (?, ?, ?)", (descricao, id_cliente, preco))
        id_produto = cur.lastrowid
=======
def deletar_produto(id_produto):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("DELETE FROM produto WHERE id_produto = ?", (id_produto, ))
>>>>>>> e194429e570e9255bcb03511a0e708b5677bb314
        con.commit()

<<<<<<< HEAD
def editar_cliente(id_cliente, nome, sexo, telefone, endereco, email):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("UPDATE cliente SET nome = ?, sexo = ?, telefone = ?, endereco = ?, email = ?, WHERE id_cliente = ?", (nome, sexo, telefone, endereco, id_cliente, email))
=======
#_________PEDIDOS__________#

def criar_pedido(cpf_cliente, descricao, quantidade, cores, datahora, status):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute( "INSERT INTO p.pedido (p.descricao, p.quantidade, p.cores, p.datahora, p.status) VALUES (?, ?, ?, ?, ?,)", (descricao, quantidade, cores, datahora, status))
        id_pedido = cur.lastrowid
>>>>>>> e194429e570e9255bcb03511a0e708b5677bb314
        con.commit()
        return id_pedido

<<<<<<< HEAD
def editar_produto(id_produto, descricao, preco):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("UPDATE produto SET descricao = ?, id_cliente = ?, preco = ? WHERE id_produto = ?", (descricao, id_cliente, preco))
        con.commit()
=======
def consultar_pedido(id_pedido):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT p.id_pedido, c.nome,  p.descricao, p.quantidade, p.cores, p.datahora, p.status FROM pedido p INNER JOIN cliente c ON p.id_cliente = c.id_cliente WHERE p.id_pedido  = ?", (id_pedido, ))
        return row_to_dict(cur.description, cur.fetchone())
>>>>>>> e194429e570e9255bcb03511a0e708b5677bb314

def listar_pedidos():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT p.id_pedido, c.nome,  p.descricao, p.quantidade, p.cores, p.datahora, p.status FROM pedido p INNER JOIN cliente c ON p.id_cliente = c.id_cliente ORDER BY p.id_pedido")
        return rows_to_dict(cur.description, cur.fetchall())    

#def listar_produtos_ordem():
#    with closing(conectar()) as con, closing(con.cursor()) as cur:
#        cur.execute("SELECT id_produto, descricao, quantidade, preco, cores FROM produto ORDER BY descrição")
#        return rows_to_dict(cur.description, cur.fetchall())

def editar_pedido(id_pedido, descricao, quantidade, cores, status):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("UPDATE pedido SET descricao = ?, quantidade = ?, cores = ?, status = ? WHERE id_pedido = ?", (descricao, quantidade, cores, status, id_pedido))
        con.commit()

def deletar_pedido(id_pedido):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("DELETE FROM pedido WHERE id_pedido = ?", (id_pedido, ))
        con.commit()

########################
#### Inicialização. ####
########################

if __name__ == "__main__":
    criar_bd
    app.run()