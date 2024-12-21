# database.py
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Inicializar o objeto db do SQLAlchemy
db = SQLAlchemy()

# Função para obter a URI do banco de dados
def get_database_uri():
    DATABASE_USER = os.getenv('DATABASE_USER')
    DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
    DATABASE_HOST = os.getenv('DATABASE_HOST')
    DATABASE_PORT = os.getenv('DATABASE_PORT')
    DATABASE_NAME = os.getenv('DATABASE_NAME')

    if not all([DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_PORT, DATABASE_NAME]):
        raise ValueError("Uma ou mais variáveis de ambiente do banco de dados não foram configuradas corretamente.")
    
    if os.environ.get('FLASK_ENV') == 'production':
        return f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'
    else:
        return f'sqlite:///{DATABASE_NAME}.db'  # SQLite para desenvolvimento

# Função para inicializar o banco de dados
def init_db(app):
    # Configurações de banco de dados
    app.config['SQLALCHEMY_DATABASE_URI'] = get_database_uri()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desabilita o rastreamento de modificações de objetos (para desempenho)

    # Inicializa o db com a aplicação
    db.init_app(app)

    # Inicializa o Migrate
    migrate = Migrate(app, db)

    return db

