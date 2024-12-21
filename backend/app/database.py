#database.py
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # Importando o Migrate
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Carregar variáveis do arquivo .env
load_dotenv()

# Criação da instância do SQLAlchemy
db = SQLAlchemy()

# Instância do Migrate
migrate = Migrate()

# Função para obter a URI do banco de dados a partir do .env
def get_database_uri():
    DATABASE_USER = os.getenv('DATABASE_USER')
    DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
    DATABASE_HOST = os.getenv('DATABASE_HOST')
    DATABASE_PORT = os.getenv('DATABASE_PORT')
    DATABASE_NAME = os.getenv('DATABASE_NAME')

    if not all([DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_PORT, DATABASE_NAME]):
        raise ValueError("Uma ou mais variáveis de ambiente do banco de dados não foram configuradas corretamente.")
    
    if os.environ.get('FLASK_ENV') == 'production':
        return f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'  # PostgreSQL
    else:
        return 'sqlite:///northcromo.db'  # SQLite para desenvolvimento

# Função para inicializar o banco de dados
def init_db(app):
    # Obtenha a URI do banco de dados
    app.config['SQLALCHEMY_DATABASE_URI'] = get_database_uri()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desabilita modificações de objetos para desempenho

    # Inicializa o db com a configuração do Flask
    db.init_app(app)

     # Inicializa o Flask-Migrate
    migrate.init_app(app, db)

    # Testando a conexão com o banco de dados
    try:
        with app.app_context():  # Necessário para executar a consulta dentro do contexto do Flask
            with db.engine.connect() as conn:
                conn.execute(text('SELECT 1'))  # Query simples para testar a conexão
        print("Conexão com o banco de dados bem-sucedida!")
    except Exception as e:
        print(f"Erro ao conectar com o banco de dados: {e}")
        raise e

    return db  # Retorna o objeto db para uso

