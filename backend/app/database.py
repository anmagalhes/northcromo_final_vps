import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
load_dotenv()

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
        return f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'  # PostgreSQL síncrono
    else:
        return 'sqlite:///northcromo.db'  # SQLite síncrono

# Função para inicializar o banco de dados
def init_db(app):
    # Obtenha a URI do banco de dados
    app.config['SQLALCHEMY_DATABASE_URI'] = get_database_uri()

    # Inicializa o engine e o sessionmaker
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True)

    Session = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )

    # Testando a conexão com o banco de dados
    try:
        with engine.connect() as conn:
            conn.execute(text('SELECT 1'))  # Query simples para testar a conexão
        print("Conexão com o banco de dados bem-sucedida!")
    except Exception as e:
        print(f"Erro ao conectar com o banco de dados: {e}")
        raise e  # Levanta o erro caso a conexão falhe

    return engine, Session

# Função para obter a sessão do banco
def get_db_session(engine, Session):
    return Session()  # Retorna a sessão do banco de dados

# Função para fechar a sessão do banco
def close_db_session(session):
    session.close()  # Fecha a sessão após a requisição
