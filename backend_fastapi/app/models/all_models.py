# app/models/all_models.py
from app.models import (
    user,
    produto,
    cliente,
    todo,
    componente,
    postotrabalho,
    posto_tarefa,
    defeito,
    funcionario,
)


from app.models.grupo_produto import Grupo_Produto
from app.models.recebimento.recebimento import Recebimento
from app.models.recebimento.itens_recebimento import ItensRecebimento
from app.models.notafiscal.notafiscal import NotaFiscal
from app.models.notafiscal.notaRecebimento import NotaRecebimento
from app.models.checklist_recebimento.checklist_recebimento import Checklist_Recebimento
