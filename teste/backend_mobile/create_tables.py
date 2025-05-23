import asyncio
from sqlalchemy import MetaData, text
from app.core.database import engine
from app.api.models import *  # importa todos os modelos e registra no metadata
from app.api.models import Base  # <- importa Base do mesmo local onde os modelos são registrados

async def reset_and_create_tables():
    print("🧹 Deletando todas as tabelas do banco de dados...")

    async with engine.begin() as conn:
        metadata = MetaData()
        # reflect e drop_all sem passar bind
        await conn.run_sync(lambda sync_conn: metadata.reflect(sync_conn))
        await conn.run_sync(lambda sync_conn: metadata.drop_all(sync_conn))

    print("✅ Todas as tabelas deletadas com sucesso.")

    print("🔧 Criando tabelas no banco de dados...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("✅ Tabelas criadas com sucesso.")

    print("🔍 Verificando tabelas no banco de dados...")
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
        tables = result.fetchall()
        if tables:
            print("📋 Tabelas encontradas:")
            for table in tables:
                print(f"  🔹 {table[0]}")
        else:
            print("⚠️ Nenhuma tabela encontrada.")

if __name__ == "__main__":
    asyncio.run(reset_and_create_tables())
