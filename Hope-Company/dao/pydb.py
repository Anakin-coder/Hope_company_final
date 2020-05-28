from entities.usuario import Usuario
from contextlib import closing
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

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

CREATE TABLE pedido (
    id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER NOT NULL,
    datahora CURRENT_DATE NOT NULL,
    status TINYINT(1),
    FOREIGN KEY(id_cliente) REFERENCES cliente(id_cliente)
);
CREATE TABLE produto_pedido (
    id_prod_pedido INTEGER PRIMARY KEY,
    id_produto INTEGER NOT NULL,
    id_pedido INTEGER NOT NULL,
    preco REAL NOT NULL,
    quantidade INTEGER NOT NULL,
    FOREIGN KEY(id_produto) REFERENCES produto(id_produto),
    FOREIGN KEY(id_pedido) REFERENCES pedido(id_pedido)
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

def lembrar_senha(usuario, email, senha):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("UPDATE usuario SET senha = ? WHERE usuario = ? AND email = ?", (senha, usuario, email, ))
        con.commit()
########################
#### Inicialização. ####
########################

if __name__ == "__main__":
    criar_bd()
    
