# app/cors/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings  # Certifique-se de que o caminho para config está correto

# Criação do engine assíncrono usando a URL do banco de dados fornecida no arquivo de configuração
engine: AsyncEngine = create_async_engine(settings.DATABASE_URL, echo=True)

# Criação do sessionmaker para sessões assíncronas
Session: sessionmaker = sessionmaker(
    bind=engine,  # Associando o engine ao sessionmaker
    class_=AsyncSession,  # Definindo a classe de sessão como AsyncSession
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)
