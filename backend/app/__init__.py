# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import DevelopmentConfig


# Inicializando as instâncias de db e migrate globalmente
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    # Cria a instância da aplicação Flask
    app = Flask(__name__)
    
    # Configura a aplicação com as variáveis do arquivo de configuração
    app.config.from_object(DevelopmentConfig)  # Carrega as configurações do arquivo de configuração

    # Inicializa o banco de dados com a aplicação Flask
    db.init_app(app)  # Inicializa o banco de dados com a configuração

    # Inicializa o Migrate com a aplicação e db
    migrate.init_app(app, db)  # Inicializa o Flask-Migrate

    # Registre os blueprints (rotas)
    from app.cliente.routes import cliente_blueprint
    app.register_blueprint(cliente_blueprint, url_prefix='/api/cliente')

    return app