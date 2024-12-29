# app/models/__init__.py
from .user import User                      #OK
from .grupo_produto_model import Grupo_Produto    #OK
from .operacaos_model import Operacao              #OK
from .componente_model import Componente          #OK
#from .cliente_model import Cliente, ChecklistRecebimento
from .cliente_model import Cliente
from .funcionario_model import Funcionario        #OK
from .tarefa_produto import TarefaProduto   #OK
from .PostoTrabalho import PostoTrabalho    #OK
from .defeito_model import Defeito                #OK
from .produto import Produto                #OK
from .recebimento import Recebimento        #OK
from .foto_recebimento_model import FotoRecebimento  #OK
from .checklist_Recebimento_model import ChecklistRecebimento #OK
from .impressao_checklistRecebimento import ImpressaoChecklistRecebimento #OK
from .teste import Teste

# Função auxiliar para carregar alguma função dos modelos sem gerar ciclos de importação
def load_some_function():
    from app.models import some_function  # Importação dentro de uma função para evitar o ciclo de importação
    some_function()  # Isso chama a função desejada (ou outra lógica necessária)
