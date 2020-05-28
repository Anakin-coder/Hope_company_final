from flask import Flask, request, render_template, session
from dao import pydb.*
#---------------------------------LOGIN-----------------------------------------------#
login = Flask(__name__)

@login_api.route("/", methods = ["GET"])
def form_login():
    return render_template("login.html", usuario = "", senha = "")

@login.route("/", methods = ["POST"])
def login_api():
    print('oi cheguei aqui')
    nome = request.form['usuario']
    senha = request.form['senha']
    u = consultar_usuario(nome)
    if u is None:
        return render_template('login.html', mensagem = 'Usuário não está cadastrado')
    if u.verifica_senha(senha):
        return render_template("menu.html", mensagem = f"Bem vindo, {nome}")
    return render_template('login.html', mensagem = 'Senha incorreta')

#---------------------------------CADASTRO DE NOVO USUARIO-----------------------------------------------#

@login.route("/registrar/novo/", methods = ["GET"])
def form_registrar_novo_usu_api():
    return render_template("form_registrar_usu.html", id_usuario = "novo", email = "", usuario = "", senha = "")

@login.route("/registrar/novo/", methods = ["POST"])
def criar_usuario_api():
    email = request.form["email"]
    nome = request.form["usuario"]
    senha = request.form["senha"]
    inserir_novo_usuario(email, nome, senha)
    return render_template("menu.html", mensagem = "Cadastro efetuado com sucesso")
