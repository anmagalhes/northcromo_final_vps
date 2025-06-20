from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

from app.Schema.componente_schema import ComponenteRead
from app.Schema.operacao_schema import OperacaoRead
from app.Schema.posto_trabalho_schema import Posto_TrabalhoRead

# Enum para Tipo de Grupo
class TipoGrupo(str, Enum):
    PRODUTO = "PRODUTO"
    SERVICO = "SERVICO"

# Base para o Produto
class ProdutoBase(BaseModel):
    cod_produto: str = Field(..., max_length=10, description="Código único do produto")
    produto_nome: str = Field(..., max_length=255, description="Nome do produto")
    componente_id: int = Field(..., description="ID do componente associado")
    operacao_id: int = Field(..., description="ID da operação associada")
    und_servicos: str = Field(..., max_length=50, description="Unidade de serviço do produto")
    grupo_id: TipoGrupo
    tipo_produto: int = Field(..., description="1 - Produto, 2 - Tarefa")
    posto_trabalho_id: int = Field(..., description="ID do posto de trabalho associado")

    data: Optional[datetime] = None  # Adicionando o campo `data` opcional

    fornecedores: Optional[List[int]] = Field(default_factory=list)

    @field_validator("cod_produto", mode="before")
    @classmethod
    def cod_produto_to_upper(cls, v):
        return v.upper()


    @field_validator("data", mode="before")
    @classmethod
    def parse_data(cls, v):
        if v is None:
            return None
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v)
            except ValueError:
                raise ValueError("data deve ser uma string ISO 8601 válida")
        return v

    class Config:
        from_attributes = True  # Substituindo 'orm_mode' para Pydantic V2


# Produto para criação (sem o ID)
class ProdutoCreate(ProdutoBase):
    pass


# Produto para leitura (inclui todos os campos, incluindo os relacionamentos)
class ProdutoRead(BaseModel):
    id: int
    cod_produto: str
    produto_nome: str
    und_servicos: str
    grupo_id: TipoGrupo
    tipo_produto: int
    data: Optional[datetime]

    # Relacionamentos carregados - agora opcionais
    componente: Optional[ComponenteRead] = None
    operacao: Optional[OperacaoRead] = None
    posto_trabalho: Optional[Posto_TrabalhoRead] = None

    class Config:
        from_attributes = True

class ProdutoResponse(BaseModel):
    id: int
    cod_produto: str
    produto_nome: str
    componente_id: int
    operacao_id: int
    posto_trabalho_id: int
    und_servicos: str
    grupo_id: TipoGrupo
    tipo_produto: int

