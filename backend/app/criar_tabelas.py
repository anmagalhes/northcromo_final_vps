import asyncio
from app import app  # Importa a instância do Flask
from models import db  # Importa a instância do banco de dados (SQLAlchemy)
from models.user import User  # Importa os modelos (como o User)
from models.componente import Componente
from models.defeito import Defeito
from models.funcionario import Funcionario
from models.grupo_produto import GrupoProduto
from models.operacao import Operacao
from models.posto_trabalho import PostoTrabalho
from models.tarefa_produto import TarefaProduto
from database import init_db  # Importa a função de inicialização do banco de dados

# Função assíncrona para criar as tabelas no banco de dados
async def criar_tabelas():
    # Inicializa o banco de dados
    engine, Session = await init_db(app)  # Obtém a engine e session do banco assíncrono

    # Cria todas as tabelas definidas nos modelos
    async with engine.begin() as conn:
        await conn.run_sync(db.metadata.create_all)  # Cria as tabelas

    print("Tabelas criadas com sucesso!")

# Função para rodar a criação das tabelas antes de iniciar o app
async def run():
    await criar_tabelas()  # Cria as tabelas
    # Agora roda o servidor Flask de forma síncrona
    app.run(debug=True, host="0.0.0.0")  # Rodando Flask

# Ponto de entrada principal para rodar o código
if __name__ == "__main__":
    asyncio.run(run())  # Inicializa a criação das tabelas e depois o Flask