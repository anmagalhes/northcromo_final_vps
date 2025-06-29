from pydantic import BaseModel,  Field, validator
from typing import List
from typing import Optional
from pydantic import HttpUrl
from enum import Enum
from datetime import datetime


#from app.Schema.cliente_schema import ClienteRead
class TipoOrdemEnum(str, Enum):
    NOVO = "NOVO"
    NAO = "NAO"
    SIM = "SIM"

from pydantic import BaseModel, Field, validator
from typing import Optional
from enum import Enum

class LinksFotos(BaseModel):
    numero_ordem: str
    os_formatado: str
    foto1: Optional[str]
    foto2: Optional[str]
    foto3: Optional[str]
    foto4: Optional[str]
    cliente: Optional[str]
    quantidade: Optional[int] = Field(default=0)
    tipoOrdem: Optional[TipoOrdemEnum]
    referencia: Optional[str]
    nfRemessa: Optional[str]
    queixa_cliente: Optional[str]
    dataRecebimento: Optional[str]
    horaRecebimento: Optional[str]

    # Campo para nota fiscal (opcional)
    nota_fiscal_id: Optional[int] = Field(
        default=None,
        description="ID da nota fiscal associada"
    )
    nota_fiscal_numero: Optional[str] = Field(
        default=None,
        description="Número da nota fiscal (apenas para exibição)"
    )


    @validator(
        "cliente", "referencia", "nfRemessa", "queixa_cliente", "dataRecebimento", "horaRecebimento",
        "foto1", "foto2", "foto3", "foto4",
        pre=True
    )
    def empty_string_to_none(cls, v):
        if v == "":
            return None
        return v

    @validator("quantidade", pre=True)
    def quantidade_str_to_int(cls, v):
        if v is None:
            return 0
        if isinstance(v, str) and v.isdigit():
            return int(v)
        if isinstance(v, int):
            return v
        raise ValueError("quantidade deve ser um número inteiro válido")

    @validator("tipoOrdem", pre=True, always=True)
    def tipo_ordem_normalize(cls, v):
        if v is None or v == "":
            return TipoOrdemEnum.NAO
        val = str(v).strip().upper()
        if val == "NOVO":
            return TipoOrdemEnum.NOVO
        elif val in ["NAO", "NÃO", "ANTIGO"]:
            return TipoOrdemEnum.NAO
        else:
            raise ValueError(f"tipoOrdem inválido: {v}. Use 'NOVO' ou 'NAO'")

class RecebimentoSchema(BaseModel):
    numero_ordem: Optional[int]
    os_formatado: str
    cliente: Optional[str]
    quantidade: Optional[int] = Field(default=1)
    img1_ordem: Optional[str]
    img2_ordem: Optional[str]
    img3_ordem: Optional[str]
    img4_ordem: Optional[str]
    tipoOrdem: Optional[TipoOrdemEnum]
    queixa_cliente: Optional[str]

    # Campo para nota fiscal (opcional)
    nota_fiscal_id: Optional[int] = Field(
        default=None,
        description="ID da nota fiscal associada"
    )
    numero_nota_fiscal: Optional[str] = Field(
        default=None,
        description="Número da nota fiscal (apenas para exibição)"
    )


    @validator("tipoOrdem", pre=True, always=True)
    def tipo_ordem_normalize(cls, v):
        if v is None or v == "":
            return TipoOrdemEnum.NAO
        val = str(v).strip().upper()
        if val == "NOVO":
            return TipoOrdemEnum.NOVO
        elif val in ["NAO", "NÃO", "ANTIGO"]:
            return TipoOrdemEnum.NAO
        else:
            raise ValueError(f"tipoOrdem inválido: {v}. Use 'NOVO', 'NAO' ou 'NOVO'")

class RecebimentoRead(BaseModel):
    id: int
    numero_ordem: Optional[int]
    os_formatado: str
    cliente: Optional[str]
    quantidade: Optional[int] = Field(default=1)
    tipoOrdem: Optional[TipoOrdemEnum] = None
    queixa_cliente: Optional[str] = None
    data_recebimento: Optional[datetime] = None
    hora_recebimento: Optional[str] = None
    referencia: Optional[str] = None
    nfRemessa: Optional[str] = None

    nota_fiscal_id: Optional[int] = None
    numero_nota_fiscal: Optional[str] = None

    # Imagens
    img1_ordem: Optional[str] = None
    img2_ordem: Optional[str] = None
    img3_ordem: Optional[str] = None
    img4_ordem: Optional[str] = None

    # LinksFotos agrupado (opcional)
    fotos: Optional[LinksFotos] = None

    # Relacionamento Cliente
    #cliente: Optional[ClienteRead]

    class Config:
        from_attributes = True
