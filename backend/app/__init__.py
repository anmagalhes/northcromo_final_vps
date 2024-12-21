# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

# Inicializar o objeto db
db = SQLAlchemy()

# Carregar variáveis de ambiente
load_dotenv()

def create_app():
    app = Flask(__name__)

    # Configuração do banco de dados - carregando do .env
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///default.db')  # Fallback para SQLite local
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializa o db com o app
    db.init_app(app)

    # Inicializa o Migrate
    migrate = Migrate(app, db)

    return app
