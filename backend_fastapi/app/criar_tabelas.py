# app/criar_tabelas.py
import os
import sys

# Ajuste do Python Path para garantir que o diretório correto seja encontrado
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import asyncio

from app.core.config import settings  # Certifique-se de que Base esteja aqui
from app.core.database import engine  # Usando o engine para execução DDL
from app.models.all_models import *  # Importe os modelos de fato


# Função assíncrona para criar as tabelas
async def criar_tabelas() -> None:
    # Criação de uma sessão apenas para a transação
    async with engine.begin() as conn:  # Usando o engine para realizar DDL
        # Criação das tabelas no banco de dados se não existirem
        await conn.run_sync(settings.Base.metadata.create_all, checkfirst=True)

    print("Tabelas criadas com sucesso!")


# Chama a função para executar a criação das tabelas
if __name__ == "__main__":
    asyncio.run(criar_tabelas())
