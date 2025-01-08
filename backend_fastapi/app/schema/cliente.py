# app/schemas/cliente.py
from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime
from pydantic import ConfigDict, EmailStr

from app.models.cliente import Cliente


# Esquema básico para Cliente
class ClienteSchema(BaseModel):
    tipo_cliente: Optional[str] = None  # Tipo de Cliente (opcional)
    nome_cliente: str  # Nome do Cliente
    doc_cliente: Optional[str] = None  # Documento do Cliente (CPF ou CNPJ)
    endereco_cliente: Optional[str] = None  # Endereço do Cliente
    num_cliente: Optional[str] = None  # Número do endereço
    bairro_cliente: Optional[str] = None  # Bairro
    cidade_cliente: Optional[str] = None  # Cidade
    uf_cliente: Optional[str] = None  # UF
    cep_cliente: Optional[str] = None  # CEP
    telefone_cliente: Optional[str] = None  # Telefone do Cliente
    telefone_rec_cliente: Optional[str] = None  # Telefone de recado
    whatsapp_cliente: Optional[str] = None  # WhatsApp
    email_funcionario: Optional[EmailStr] = None  # E-mail do Funcionário responsável
    acao: Optional[str] = None  # Ação/observações adicionais
    fornecedor_cliente: Optional[str] = None  # Fornecedor associado ao cliente

     # Validar tipo_cliente para garantir que seja em maiúsculas
    @validator('tipo_cliente', pre=True, always=True)
    def ensure_tipo_cliente_uppercase(cls, v):
        if v is not None:
            return v.upper()  # Converte o valor para maiúsculas
        return v


# Esquema de Cliente para exibição pública (com relacionamentos)
class ClientePublic(ClienteSchema):
    id: int  # ID do cliente


# Exibição de múltiplos clientes (com paginação)
class ClienteList(BaseModel):
    clientes: List[ClientePublic]  # Lista de clientes
    offset: int  # Offset da paginação
    limit: int  # Limite da paginação


# Esquema para atualização de Cliente
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
    email_funcionario: Optional[str] = None
    acao: Optional[str] = None
    fornecedor_cliente: Optional[str] = None

    # Validar tipo_cliente para garantir que seja em maiúsculas
    @validator('tipo_cliente', pre=True, always=True)
    def ensure_tipo_cliente_uppercase(cls, v):
        if v is not None:
            return v.upper()  # Converte o valor para maiúsculas
        return v

