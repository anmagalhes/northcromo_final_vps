from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class ClienteBase(BaseModel):
    tipo_cliente: str
    nome_cliente: str
    doc_cliente: str
    endereco_cliente: Optional[str] = None
    num_cliente: Optional[str] = None
    bairro_cliente: Optional[str] = None
    cidade_cliente: Optional[str] = None
    uf_cliente: Optional[str] = None
    cep_cliente: Optional[str] = None
    telefone_cliente: Optional[str] = None
    telefone_rec_cliente: Optional[str] = None
    whatsapp_cliente: Optional[str] = None
    email_cliente: Optional[str] = None
    fornecedor_cliente_id: Optional[int] = None


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    tipo_cliente: Optional[str] = None
    nome_cliente: Optional[str] = None
    doc_cliente: Optional[str] = None
    endereco_cliente: Optional[str] = None
    num_cliente: Optional[str] = None
    bairro_cliente: Optional[str] = None
    cidade_cliente: Optional[str] = None
    uf_cliente: Optional[str] = None
    cep_cliente: Optional[str] = None
    telefone_cliente: Optional[str] = None
    telefone_rec_cliente: Optional[str] = None
    whatsapp_cliente: Optional[str] = None
    email_cliente: Optional[str] = None
    fornecedor_cliente_id: Optional[int] = None


class ClienteRead(ClienteBase):
    id: int
    data_cadastro_cliente: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class PaginatedClientes(BaseModel):
    data: List[ClienteRead]
    page: int
    limit: int
    total: int
    pages: int
