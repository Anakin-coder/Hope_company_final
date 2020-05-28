from flask import Flask, request, render_template, session
from dao import pydb.*
#---------------------------------CLIENTES-----------------------------------------------#
cliente = Flask(__name__)

@cliente.route("/cliente/")
def listar_clientes_api():
    return render_template("lista_clientes.html", clientes = listar_clientes())

@cliente.route("/cliente/novo/", methods = ["GET"])
def form_criar_cliente_api():
    return render_template("form_cliente.html", id_cliente = "novo", nome = "", sexo = "", telefone = "", endereco = "", email ="",)

@cliente.route("/cliente/novo/", methods = ["POST"])
def criar_cliente_api():
    nome = request.form["nome"]
    sexo = request.form["sexo"]
    telefone = request.form["telefone"]
    endereco = request.form["endereco"]
    email = request.form["email"]
    id_cliente = criar_cliente(nome, sexo, telefone, endereco, email)
    return render_template("menu.html", mensagem = f"{'O' if sexo == 'M' else 'A'} cliente {nome} foi criad{'o' if sexo == 'M' else 'a'} com o id {id_cliente}.")

@cliente.route("/cliente/<int:id_cliente>/", methods = ["GET"])
def form_alterar_cliente_api(id_cliente):
    cliente = consultar_cliente(id_cliente)
    if cliente == None:
        return render_template("menu.html", mensagem = f"Esse cliente não existe."), 404
    return render_template("form_cliente.html", id_cliente = id_cliente, nome = cliente['nome'], sexo = cliente['sexo'], telefone = cliente['telefone'], endereco = cliente['endereco'], email = cliente['email'])

@cliente.route("/cliente/<int:id_cliente>/", methods = ["POST"])
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
