from pydantic import BaseModel,  Field
from typing import List
from typing import Optional
from pydantic import HttpUrl


class LinksFotos(BaseModel):
    cliente: Optional[str]
    numero_ordem: str
    quantidade: Optional[int] = Field(default=0)
    referencia: Optional[str]
    nfRemessa: Optional[str]
    observacao: Optional[str]
    dataRecebimento: Optional[str]
    horaRecebimento: Optional[str]
    foto1: Optional[str]
    foto2: Optional[str]
    foto3: Optional[str]
    foto4: Optional[str]


class RecebimentoSchema(BaseModel):
    numero_ordem: Optional[int]
    cliente: Optional[str]
    quantidade: Optional[int] = Field(default=0)
    img1_ordem: Optional[str]
    img2_ordem: Optional[str]
    img3_ordem: Optional[str]
    img4_ordem: Optional[str]

    model_config = {
        "from_attributes": True  # Permite conversão automática de objetos SQLAlchemy para Pydantic
    }
