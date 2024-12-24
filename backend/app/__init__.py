# app/__init__.pypip install flask-cors
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS  # Importando o CORS
from app.config import DevelopmentConfig

# Inicializando as instâncias de db e migrate globalmente
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)  # Carrega as configurações do arquivo de configuração

    db.init_app(app)  # Inicializa o banco de dados com a configuração
    migrate.init_app(app, db)  # Inicializa o Flask-Migrate

    # Configurar o CORS
    CORS(app)  # Isso vai permitir CORS para toda a aplicação

    return app

