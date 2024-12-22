#__init__
from flask import Flask
from .database import db, init_db  # Certifique-se de importar corretamente o db
from .models import *  # Importe os modelos necessários aqui, como User, Produto, etc.
from .blueprints.frontend_blueprint import frontend_bp  # Exemplo de blueprint, ajuste conforme necessário
from .auth import auth_blueprint  # Exemplo de blueprint de autenticação, ajuste conforme necessário

def create_app():
    app = Flask(__name__)

    # Configuração do banco de dados
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///northcromo.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)  # Inicializa o db com o app
    
    # Registra os blueprints
    app.register_blueprint(frontend_bp)
    app.register_blueprint(auth_blueprint, url_prefix='/api/auth')

    # Outros blueprints conforme necessário
    # app.register_blueprint(another_blueprint)

    # Inicia o banco de dados e outras configurações
    init_db(app)

    return app
