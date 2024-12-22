from app.database import db  # Importando a instância db

# Importando os modelos
from .user import User
from .grupo_produto import Grupo_Produto
from .operacao import Operacao
from .componente import Componente
from .cliente import Cliente
from .funcionario import Funcionario
from .tarefa_produto import TarefaProduto
from .PostoTrabalho import PostoTrabalho
from .defeito import Defeito
#from .produto import Produto
#from .recebimento import Recebimento
#from .foto_recebimento import FotoRecebimento
#from .checklist_Recebimento import ChecklistRecebimento
#from .impressao_checklistRecebimento import ImpressaoChecklistRecebimento


# Definindo a função some_function (se for necessária)
def some_function():
    pass  # Esta função pode ser um placeholder ou uma função vazia