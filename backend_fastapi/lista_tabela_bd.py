import asyncio
import asyncpg

async def listar_tabelas():
    conn = await asyncpg.connect("postgresql://flask_user:tonyteste@147.93.12.171:5432/northcromo")
    
    # Consulta para listar todas as tabelas no banco de dados
    result = await conn.fetch('SELECT table_name FROM information_schema.tables WHERE table_schema = \'public\';')

    # Exibe todas as tabelas
    print("Tabelas no banco de dados:")
    for row in result:
        print(row['table_name'])
    
    await conn.close()

# Executa a função de listagem das tabelas
asyncio.run(listar_tabelas())
