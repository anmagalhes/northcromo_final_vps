# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.models import checklist_Recebimento

# URL de conexão do banco de dados
# O SQLite usará um arquivo chamado 'test.db' para armazenar os dados localmente.
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # SQLite armazena localmente

# Criação do motor de banco de dados
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Criando a sessão de banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarando a base das tabelas (Base é a classe base para nossos modelos)
Base = declarative_base()


def init_db():
    """ Criação das tabelas no banco de dados """
    from app.models import grupo_produto, ordem_producao, tarefa, impressao_checklist
    Base.metadata.create_all(bind=engine)


def get_db():
    """ Função para obter uma sessão de banco de dados (geralmente usada em dependências FastAPI) """
    db = SessionLocal()
    try:
        yield db  # Isso cria um gerenciador de contexto para as transações no banco de dados
    finally:
        db.close()  # Fecha a conexão após o uso
