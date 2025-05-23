from sqlalchemy import inspect
from app.core.database import Session
import asyncio


async def check_tables():
    # Abrindo uma sessão assíncrona
    async with Session() as session:
        # Usando run_sync para garantir que a inspeção seja feita de forma síncrona
        result = await session.run_sync(
            lambda sync_session: inspect(sync_session.bind).get_table_names()
        )
        print("Tabelas no banco de dados:", result)


if __name__ == "__main__":
    asyncio.run(check_tables())
