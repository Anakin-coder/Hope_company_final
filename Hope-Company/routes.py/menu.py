from flask import Flask, request, render_template, session

#---------------------------------MENU-----------------------------------------------#
menu = Flask(__name__)

@menu.route("/menu/")
def menu_api():
    return render_template("menu.html", mensagem = "")