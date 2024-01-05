from FakePinterest import database, app
# para rodar o comando do database, precisa rodar o app dentro de um contexto
from FakePinterest.models import Usuario, Foto

# também tenho que importar as classes criadas que irão gerar a minha tabela do banco de dados


with app.app_context():
    database.create_all()
