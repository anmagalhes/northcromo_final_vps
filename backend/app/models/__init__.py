# app/models/__init__.py
from .user import User                      #OK
from .grupo_produto import Grupo_Produto    #OK
from .operacao import Operacao              #OK
from .componente import Componente          #OK
from .cliente import Cliente                #OK
from .funcionario import Funcionario        #OK
from .tarefa_produto import TarefaProduto   #OK
from .PostoTrabalho import PostoTrabalho    #OK
from .defeito import Defeito                #OK
from .produto import Produto                #OK
from .recebimento import Recebimento        #OK
from .foto_recebimento import FotoRecebimento  #OK
from .checklist_Recebimento import ChecklistRecebimento #OK
from .impressao_checklistRecebimento import ImpressaoChecklistRecebimento #OK

# Função auxiliar para carregar alguma função dos modelos sem gerar ciclos de importação
def load_some_function():
    from app.models import some_function  # Importação dentro de uma função para evitar o ciclo de importação
    some_function()  # Isso chama a função desejada (ou outra lógica necessária)
