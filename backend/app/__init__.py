from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

# Inicializando o objeto db
db = SQLAlchemy()

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

def create_app():
    app = Flask(__name__)

    # Configuração do banco de dados - carregando do .env
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///default.db')  # Suporta fallback para um banco SQLite local
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializando o db com o app
    db.init_app(app)

    # Inicializando o Migrate
    migrate = Migrate(app, db)

    return app
