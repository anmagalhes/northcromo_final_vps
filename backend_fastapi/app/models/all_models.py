# app/models/all_models.py
from app.models import (
    user,
    produto,
    grupo_produto,
    cliente,
    todo,
    componente,
    postotrabalho,
    posto_tarefa,
    defeito,
)

from app.models.recebimento.recebimento import Recebimento
from app.models.recebimento.itens_recebimento import ItensRecebimento

