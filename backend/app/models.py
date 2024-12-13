from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Criando a instância do SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'  # Nome da tabela no banco de dados

    # Definindo os campos da tabela
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    # Função para definir a senha com hash
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)  # Gerando o hash da senha

    # Função para verificar a senha
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)  # Verificando se a senha é válida
