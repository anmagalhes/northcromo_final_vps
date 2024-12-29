# app/criar_tabelas.py
import sys
import os

import asyncio
from sqlmodel import SQLModel, create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

# Ajustando o caminho de importação para garantir que o diretório raiz seja incluído
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.config import settings
from app.core.database import engine

# Configuração do banco de dados (ajuste conforme sua configuração)
DATABASE_URL = "postgresql+asyncpg://flask_user:tonyteste@147.93.12.171:5432/northcromo"

# Criação do engine assíncrono
engine = create_async_engine(DATABASE_URL, echo=True)

# Função assíncrona para criar as tabelas
async def criar_tabelas() -> None:
    # Importa os modelos para garantir que eles sejam registrados
    import models  # Isso importa todos os modelos definidos no arquivo __init__.py

    # Criação das tabelas no banco de dados
    async with engine.begin() as conn:
        await conn.run_sync(settings.Base.metadata.create_all, checkfirst=True)
        
        # Cria as tabelas no banco de dados se não existirem
         # await conn.run_sync(SQLModel.metadata.create_all, checkfirst=True)

    print("Tabelas criadas com sucesso!")

if __name__ == "__main__":
    # Executa a função de criação das tabelas de forma assíncrona
    asyncio.run(criar_tabelas())