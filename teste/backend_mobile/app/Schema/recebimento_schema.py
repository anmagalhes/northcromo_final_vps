from pydantic import BaseModel
from typing import List
from typing import Optional
from pydantic import HttpUrl


class LinksFotos(BaseModel):
    cliente: Optional[str]
    numero_ordem: str
    quantidade: Optional[str]
    referencia: Optional[str]
    nfRemessa: Optional[str]
    observacao: Optional[str]
    dataRecebimento: Optional[str]
    horaRecebimento: Optional[str]
    foto1: Optional[str]
    foto2: Optional[str]
    foto3: Optional[str]
    foto4: Optional[str]
