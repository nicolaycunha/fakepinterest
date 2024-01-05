# criar a estrutura do banco de dados

from FakePinterest import database, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader # função que seleciona um usuário que tenho o id dele, notar que é sem (), pois não é um callback
def load_usuario(id_usuario): # função obrigatória para quando se tem um login
    return Usuario.query.get(int(id_usuario)) # aqui eu pego meu usuario a partir da classe Usuario abaixo

class Usuario(database.Model, UserMixin): # uma subclasse do database.model, o que é permite linkar o usuario com o database
    id = database.Column(database.Integer, primary_key = True)
    username = database.Column(database.String, nullable = False )
    email = database.Column(database.String, nullable = False, unique = True)
    senha = database.Column(database.String, nullable = False )
    fotos = database.relationship("Foto", backref = 'usuario', lazy = True) # aqui vai se relacionar com as demais instancias do banco de dados, entao aqui estou chamando a clsse Foto
# o backref permite que a relação seja mútua, tanto de Usuario para Foto quanto Foto para Usuario
# o lazy está otimizando o acesso ao banco de dados

class Foto(database.Model):
    id = database.Column(database.Integer, primary_key = True) # o primary key entende automaticamente que o usuario é único e atribui um id pra ele
    imagem = database.Column(database.String, default = "default.png" ) # a imagem é um texto pois aqui será armazenado o endereço onde essa imagem está armazenada
    data_criacao = database.Column(database.DateTime, nullable = False, default = datetime.utcnow())
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable = False)
# o id_usuario irá conectar o usuario da classe Usuario com as fotos

def retrieve_foto_info(foto_id):
    foto = Foto.query.get(foto_id)
    return {'imagem': foto.imagem, 'id_usuario': foto.id_usuario}  # Adjust fields as needed

def has_permission_to_delete(foto_info, current_user):
    return foto_info['id_usuario'] == current_user.id  # Or implement your permission logic
