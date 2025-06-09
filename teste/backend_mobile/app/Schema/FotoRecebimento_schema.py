from pydantic import BaseModel, Field, validator
from typing import Optional
from enum import Enum

class TipoOrdemEnum(str, Enum):
    NOVO = "NOVO"
    NAO = "NAO"

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
        elif val == "NOVO":  # <-- esse bloco nunca será alcançado porque já foi testado antes
            return TipoOrdemEnum.SIM
        else:
            raise ValueError(f"tipoOrdem inválido: {v}. Use 'NOVO', 'NAO' ou 'NOVO'")

    class Config:
        extra = "ignore"  # Ignora campos não definidos no model
        from_attributes = True
