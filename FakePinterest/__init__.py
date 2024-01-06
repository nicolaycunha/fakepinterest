# para a estrutura de forms, models, routes, main funcionar, o flask
# exige que haja um arquivo __init__ para conectar tudo
# notar que ao criar esse arquivo, o pycharm muda o símbolo da pasta
# indicando que é um projeto, no caso um projeto flask

# a criação do meu app ocorre no __init__

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DATABASE_URL') # "sqlite:///comunidade.db" # aqui estamos configurando uma variável para criar o banco de dados
app.config['SECRET_KEY'] = "d611d7bf378879caedb5053790338fb0" # gerado com secrets.toke_hex(16)
app.config['UPLOAD_FOLDER'] = "static/fotos_posts"
database = SQLAlchemy(app) # para criar o banco de dados
# depois de criado o app, nós vamos importar as rotas que conectam o site
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "homepage" # aqui definimos o nome da função da página que queremos que ocorra o login

from FakePinterest import routes

