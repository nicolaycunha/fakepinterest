# criar os formulários do nosso site

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from FakePinterest.models import Usuario

class FormLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()]) # entre () eu coloco o texto que quero que apareça
    senha = PasswordField("Senha", validators=[DataRequired()])
    botao = SubmitField("Fazer login")

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email = email.data).first() # aqui pegamos o email.data do banco de dados e comparamos com o email aqui
        if not usuario:
            raise ValidationError('Usuário inexistente, crie uma conta para continuar')

class FormCriarConta(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    username = StringField('Nome do usuário', validators=[DataRequired()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField("Confirmação de senha", validators=[DataRequired(), EqualTo('senha')])
    botao_confirmacao = SubmitField('Criar conta')
    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email = email.data).first() # aqui pegamos o email.data do banco de dados e comparamos com o email aqui
        if usuario:
            raise ValidationError('E-mail já cadastrado, faça login para continuar')

class FormFoto(FlaskForm):
    foto = FileField('Foto', validators=[DataRequired()])
    botao_confirmacao = SubmitField('Enviar')

