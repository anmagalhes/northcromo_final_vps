import asyncio
import asyncpg

async def fetch_data():
    # Conectando ao banco de dados
    conn = await asyncpg.connect(
        user='flask_user',
        password='tonyteste',
        database='northcromo',
        host='147.93.12.171',
        port='5432'
    )

    # Substituindo 'sua_tabela' por 'cliente'
    rows = await conn.fetch('SELECT * FROM Producao LIMIT 5')  # A consulta à tabela 'cliente'
    
    # Imprimindo as linhas retornadas pela consulta
    for row in rows:
        print(row)  # Exibe cada linha retornada pela consulta

    # Fechar a conexão com o banco de dados
    await conn.close()

# Rodar a função assíncrona
asyncio.run(fetch_data())
