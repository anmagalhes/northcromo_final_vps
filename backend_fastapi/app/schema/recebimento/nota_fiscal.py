# app/schemas/notafiscal/notaFiscal.py

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class NotaRecebimentoPublic(BaseModel):
    id_nota: int
    recebimento_ordem: int

class NotaFiscalPublic(BaseModel):
    id_nota: int
    numero: str
    data_emissao: datetime
    valor_total: float
    notas_recebimento: List[NotaRecebimentoPublic]  # Lista de Notas de Recebimento associadas


# Se você quiser um modelo que seja mais genérico, como para mostrar apenas informações básicas:
class NotaFiscalSimplePublic(BaseModel):
    id_nota: int
    numero: str
    data_emissao: datetime
    valor_total: float
