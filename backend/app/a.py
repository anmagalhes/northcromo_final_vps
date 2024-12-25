import sys
import os

# Ajuste do Python Path para garantir que o diretório correto seja encontrado
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import asyncpg
import asyncio
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()


async def test_connection():
    try:
        # Recuperando as variáveis de ambiente
        host = os.getenv('DATABASE_HOST')
        user = os.getenv('DATABASE_USER')
        password = os.getenv('DATABASE_PASSWORD')
        db_name = os.getenv('DATABASE_NAME')
        port = os.getenv('DATABASE_PORT')

        # Verificar se a porta é um número válido
        if port is None:
            print("Erro: A porta do banco de dados não foi configurada.")
            return

        # Garantir que a porta seja um número inteiro
        try:
            port = int(port)
        except ValueError:
            print(f"Erro: Porta '{port}' não é válida.")
            return

        # Conectando ao banco de dados com a string de conexão
        conn = await asyncpg.connect(
            f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
        )
        print("Conexão bem-sucedida!")
        await conn.close()
    except Exception as e:
        print(f"Erro ao testar a conexão: {e}")

# Rodando o teste de conexão
asyncio.run(test_connection())
