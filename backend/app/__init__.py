# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Inicializando o objeto db
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configuração do banco de dados
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sua-uri-do-banco'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializando o db com o app
    db.init_app(app)

    return app
