# from flask import Flask, render_template, url_for
#
# # url_for é uma função que permite que o @app.route use o nome da função para direcionar os botoes e não necessariamente o link criado no
# # app.route. Por exemplo, para a homepage é /, mas se alterarmos a / perdemos todos os links, então podemos usar o url_for para usar o nome da função
# # que é homepage
#
# # render_template vai buscar e carregar os templates html, por isso a pasta precisa ser templates
# app = Flask(__name__) # primeira coisa a se fazer é crir o app, que nada mais é que o site/application
#
# # abaixo é um decorator, atribui uma funcionalidade na função que estamos criando abaixo
# @app.route("/") # criando a rota que irá ativar o site, colocá-lo on-line, a / diz que é a raiz
# def homepage():
#     return render_template("homepage.html")
# # ai cada nova página dentro do site usamos uma função
#
# @app.route('/perfil/<usuario>') # ao colocar o usuario entre tags <> tornamos isso dinamico, então é de boa
#                                 # agora ter vários usuarios, onde o link mudará de forma dinâmica, tornando o usuário uma variável
# def perfil(usuario): # notar que aqui chamo o usuario novamente
#     return render_template("perfil.html", usuario = usuario) # ai pra acessar código python no html eu chamo por meio de {{ código pyhton }}
from FakePinterest import app # isso aqui está dizendo pegue do arquivo __init__ o app


if __name__ == "__main__":
    app.run(debug=True)
