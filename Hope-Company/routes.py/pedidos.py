from flask import Flask, request, render_template, session
from dao import pydb.*
#_______PEDIDO________#
pedido = Flask(__name__)

@pedido.route("/pedido/")
def listar_pedidos_api():
    return render_template("lista_pedidos.html", pedidos = listar_pedidos())

@pedido.route("/pedido/novo/", methods = ["GET"])
def form_criar_pedido_api():
    return render_template("form_pedido.html", id_pedido = "novo", quantidade = "", status = "", preco = "", clientes = listar_clientes(), produtos = listar_produtos())

@pedido.route("/pedido/novo/", methods = ["POST"])
def criar_pedido_api():
    quantidade = request.form["quantidade"]
    status = request.form["status"]
    preco = request.form["preco"]
    id_cliente = request.form["id_cliente"]
    id_produto = request.form["id_produto"]
    id_pedido = criar_pedido(quantidade, status, preco, id_cliente, id_produto)
    return render_template("menu.html", mensagem = f"Novo pedido gerado: {id_pedido}!")

@pedido.route("/pedido/<int:id_pedido>/", methods = ["GET"])
def form_alterar_pedido_api(id_pedido):
    pedido = consultar_pedido(id_pedido)
    if pedido == None:
        return render_template("menu.html", mensagem = f"Esse pedido não existe."), 404
    return render_template("form_pedido.html", id_pedido = id_pedido, id_produto = pedido['id_produto'], quantidade = pedido['quantidade'], status = pedido['status'], preco = pedido['preco'], clientes = listar_clientes(), produtos = listar_produtos())

@pedido.route("/pedido/<int:id_pedido>/", methods = ["POST"])
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

@pedido.route("/pedido/<int:id_pedido>", methods = ["DELETE"])
def deletar_pedido_api(id_pedido):
    pedido = consultar_pedido(id_pedido)
    if pedido == None:
        return render_template("menu.html", mensagem = "Esse pedido nem mesmo existia mais."), 404
    deletar_pedido(id_pedido)
    return render_template("menu.html", mensagem = f"O pedido {id_pedido} foi excluído com sucesso!")
