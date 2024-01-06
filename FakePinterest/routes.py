# nesse arquivos vamos colocar todos os códigos usados para direcionar nosso site
# geralmente chamado routes, mas também pode ser encontrado como views
# onde vamos criar os links para conectar as páginas dentro do site
import os.path

from flask import Flask, render_template, url_for, redirect, request
from FakePinterest import app, database, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from FakePinterest.forms import FormLogin, FormCriarConta, FormFoto
from FakePinterest.models import Usuario, Foto
import os
from werkzeug.utils import secure_filename


# url_for é uma função que permite que o @app.route use o nome da função para direcionar os botoes e não necessariamente o link criado no
# app.route. Por exemplo, para a homepage é /, mas se alterarmos a / perdemos todos os links, então podemos usar o url_for para usar o nome da função
# que é homepage

# render_template vai buscar e carregar os templates html, por isso a pasta precisa ser templates
## primeira coisa a se fazer é crir o app, que nada mais é que o site/application

# abaixo é um decorator, atribui uma funcionalidade na função que estamos criando abaixo
@app.route("/", methods = ['GET', 'POST']) # criando a rota que irá ativar o site, colocá-lo on-line, a / diz que é a raiz, o GET E POST é para permir acesso aos formulários no hmtl
def homepage():
    formlogin = FormLogin() # aqui estamos criando um link entre os formulários de login e a homepage
    if formlogin.validate_on_submit(): # validando o login
        usuario = Usuario.query.filter_by(email = formlogin.email.data).first() # aqui buscamos no banco de dados
        if usuario and bcrypt.check_password_hash(usuario.senha.encode('utf-8'), formlogin.senha.data):
            login_user(usuario)
            return redirect(url_for("perfil", id_usuario = usuario.id))
    return render_template("homepage.html", form = formlogin)
# ai cada nova página dentro do site usamos uma função


@app.route('/criarconta', methods = ['GET', 'POST'])
def criar_conta():
    formcriarconta = FormCriarConta()
    if formcriarconta.validate_on_submit(): # isso aqui só vai rodar se o usuario clicou em submeter a conta
        senha = bcrypt.generate_password_hash(formcriarconta.senha.data).decode('utf-8') # aqui estamos criptografando a senha, para que seja armazenada no banco algo criptografado
        usuario = Usuario(username = formcriarconta.username.data,
                          email = formcriarconta.email.data,
                          senha = senha)
        database.session.add(usuario) # aqui estamos fazendo uma conexao com o banco de dados para salvar esse novo usuário no banco
        database.session.commit() # comita todas as alterações no banco durante essa rodada
        login_user(usuario, remember=True)
        return redirect(url_for("perfil", id_usuario = usuario.id)) # redirecionamento para a página do perfil de usuário abaixo
    return render_template("criarconta.html", form = formcriarconta) # o form é o que será usado no html, e o formcriarconta vem do forms.py


@app.route('/perfil/<id_usuario>', methods = ['GET', 'POST']) # ao colocar o usuario entre tags <> tornamos isso dinamico, então é de boa  agora ter vários usuarios, onde o link mudará de forma dinâmica, tornando o usuário uma variável
@login_required  # mais um decorator que exige o login para que entre nessa route
def perfil(id_usuario): # notar que aqui chamo o usuario novamente
    if int(id_usuario) == int(current_user.id): # aqui o usuário está vendo o perfil dele
        form_foto = FormFoto()
        if form_foto.validate_on_submit(): # se tudo acima foi validado
            arquivo = form_foto.foto.data
            nome_seguro = secure_filename(arquivo.filename)
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                              app.config['UPLOAD_FOLDER'],  nome_seguro) # os.path.abspath(os.path.dirname(__file__)) aqui está o caminho do proprio arquivo route, nào usamos route pois se mudamos o nome ele ainda é fu cional
            arquivo.save(caminho)
            # registrar esse arquivo no banco de dados
            foto = Foto(imagem = nome_seguro, id_usuario = current_user.id) # aqui cria nossa foto
            database.session.add(foto)
            database.session.commit()
        return render_template("perfil.html", usuario = current_user, form = form_foto)
    else:
        usuario = Usuario.query.get(int(id_usuario))
        return render_template("perfil.html", usuario = usuario, form = None) # ai pra acessar código python no html eu chamo por meio de {{ código pyhton }}

@app.route("/logout")
@login_required
def logout():
    login_user(current_user)
    return redirect(url_for("homepage"))


@app.route("/feed")
@login_required
def feed():
    fotos = Foto.query.order_by(Foto.data_criacao.desc()).all()[:100] # aqui podemos filtrar para otimizar o carregamento
    return render_template("feed.html", fotos = fotos)

@app.route('/delete_photo/<int:foto_id>', methods=['POST'])
def delete_foto(foto_id):
    foto_info = retrieve_foto_info(foto_id)

    if has_permission_to_delete(foto_info, current_user):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], foto_info['imagem']))
        database.session.delete(Foto.query.get(foto_id))  # Assuming you use SQLAlchemy
        database.session.commit()

        flash('Foto excluída com sucesso!')
        return redirect(url_for('perfil', id_usuario=current_user.id))
    else:
        flash('Acesso não autorizado!')
        return redirect(url_for('perfil', id_usuario=current_user.id))  # Or handle differently
