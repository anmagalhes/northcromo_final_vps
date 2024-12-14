import asyncio
from app import app  # Importa a instância do Flask
from models import db  # Importa a instância do banco de dados (SQLAlchemy)
from models.user import User # Importa os modelos (como o User)
from models.grupo_produto import Grupo_Produto
from models.componente import Componente
from models.defeito import Defeito
from models.funcionario import Funcionario
from models.operacao import Operacao
from models.tarefa_produto import TarefaProduto
from models.PostoTrabalho import PostoTrabalho
from models.cliente import Cliente
from models.produto import Produto
from models.recebimento import Recebimento
##from models.foto_recebimento import FotoRecebimento
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