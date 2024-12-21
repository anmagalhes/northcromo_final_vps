#import asyncio
#from app import app  # Importa a instância do Flask
#from models import db  # Importa a instância do banco de dados (SQLAlchemy)
#from models.user import User  # Importa os modelos (como o User)
#from models.grupo_produto import Grupo_Produto
#from models.componente import Componente
#from models.defeito import Defeito
#from models.funcionario import Funcionario
#from models.operacao import Operacao
#from models.tarefa_produto import TarefaProduto
#from models.PostoTrabalho import PostoTrabalho
#from models.cliente import Cliente
#from models.produto import Produto
#from models.recebimento import Recebimento
#from models.foto_recebimento import FotoRecebimento
#from models.checklist_Recebimento import ChecklistRecebimento
#from models.impressao_checklistRecebimento import ImpressaoChecklistRecebimento
#from database import init_db  # Importa a função de inicialização do banco de dados
import os
from app import app  # Importa a instância do Flask
from models import db  # Importa a instância do banco de dados (SQLAlchemy)
from database import init_db  # Importa a função de inicialização do banco de dados

# Função para verificar se a tabela já existe
def tabela_existe(nome_tabela):
    # Verifica se a tabela já existe no banco de dados
    return db.engine.dialect.has_table(db.session.bind, nome_tabela)

# Função para criar as tabelas
def criar_tabelas():
    # Verifica o ambiente de execução
    if os.getenv('FLASK_ENV') == 'development':  # Só cria as tabelas no ambiente de desenvolvimento
        with app.app_context():  # Garante que o contexto do Flask esteja ativo
            # Verifica se as tabelas já existem, caso contrário, cria
            for tabela in db.metadata.sorted_tables:
                if not tabela_existe(tabela.name):  # Verifica se a tabela já existe
                    print(f"Criando a tabela {tabela.name}")
                    db.create_all()  # Cria todas as tabelas definidas nos modelos
                else:
                    print(f"Tabela {tabela.name} já existe.")
        print("Tabelas verificadas/criadas com sucesso!")
    else:
        print("Ambiente de Produção detectado, criação de tabelas ignorada.")

# Função assíncrona para inicializar o banco de dados (se necessário)
async def run():
    criar_tabelas()  # Chama a função para criar as tabelas

    # Agora roda o servidor Flask
    app.run(debug=True, host="0.0.0.0")  # Inicia o Flask

# Ponto de entrada principal para rodar o código
if __name__ == "__main__":
    run()  # Executa o código
