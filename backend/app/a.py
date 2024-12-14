# criar_tabelas.py
import asyncio
from app import app
from models import db
from models.user import Usuarios
from models.grupo_produto import GrupoProduto
from database import init_db

async def criar_tabelas():
    engine, Session = await init_db(app)

    async with engine.begin() as conn:
        await conn.run_sync(db.metadata.create_all)

    print("Tabelas criadas com sucesso!")

if __name__ == "__main__":
    asyncio.run(criar_tabelas())  # Executa a criação das tabelas
