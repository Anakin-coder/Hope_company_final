from flask import Flask, request, render_template, session
from dao import pydb.*
#_______PEDIDO________#
produto = Flask(__name__)

@produto.route("/produto/")
def listar_produtos_api():
    return render_template("lista_produtos.html", produtos = listar_produtos())

@produto.route("/produto/novo/", methods = ["GET"])
def form_criar_produto_api():
    return render_template("form_produto.html", id_produto = "novo", descricao = "", quantidade = "", preco_unitario = "")

@produto.route("/produto/novo/", methods = ["POST"])
def criar_produto_api():
    descricao = request.form["descricao"]
    quantidade = request.form["quantidade"]
    preco_unitario = request.form["preco_unitario"]
    id_produto = criar_produto(descricao, quantidade, preco_unitario)
    return render_template("menu.html", mensagem = f"Novo produto criado: {id_produto}.")

@produto.route("/produto/<int:id_produto>/", methods = ["GET"])
def form_alterar_produto_api(id_produto):
    produto = consultar_produto(id_produto)
    if produto == None:
        return render_template("menu.html", mensagem = f"Esse produto não existe."), 404
    return render_template("form_produto.html", id_produto = id_produto, descricao = produto['descricao'], quantidade = produto['quantidade'], preco_unitario = produto['preco_unitario'])

@produto.route("/produto/<int:id_produto>/", methods = ["POST"])
def alterar_produto_api(id_produto):
    descricao = request.form["descricao"]
    quantidade = request.form["quantidade"]
    preco_unitario = request.form["preco_unitario"]
    produto = consultar_produto(id_produto)
    if produto == None:
        return render_template("menu.html", mensagem = f"Esse produto não existe."), 404
    editar_produto(id_produto, descricao, quantidade, preco_unitario)
    return render_template("menu.html", mensagem = f"O produto {id_produto} foi editado com sucesso!")

@produto.route("/produto/<int:id_produto>", methods = ["DELETE"])
def deletar_produto_api(id_produto):
    produto = consultar_produto(id_produto)
    if produto == None:
        return render_template("menu.html", mensagem = "Esse produto nem mesmo existia mais."), 404
    deletar_produto(id_produto)
    return render_template("menu.html", mensagem = f"O produto {produto['descricao']} com o id {id_produto} foi excluído.")
