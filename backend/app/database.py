# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import DevelopmentConfig  # ou outro arquivo de configuração

# URL do banco de dados
DATABASE_URL = DevelopmentConfig.SQLALCHEMY_DATABASE_URI

# Criação do engine para se conectar ao banco de dados
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Sessão do banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos (todas as classes de modelo herdam de 'Base')
Base = declarative_base()

# Função para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db  # Isso é usado no FastAPI para passar a sessão para as dependências
    finally:
        db.close()
