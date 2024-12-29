# app/schema/cliente.py
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime

# Função de validação para verificar se o usuário existe
def validate_usuario_id(value: int):
    from app.models import User
    # Verifica se o usuário com esse id existe
    user = User.query.get(value)
    if not user:
        raise ValueError(f"Usuário com ID {value} não encontrado.")
    return value


# Schema base para o Cliente, comum para criar, atualizar e retornar cliente
class ClienteBaseSchema(BaseModel):
    tipo_cliente: Optional[str] = None
    nome_cliente: str =  Field(..., title="Nome do cliente")
    doc_cliente: str = Field(..., title="Documento do cliente (CPF/CNPJ)")
    endereco_cliente: Optional[str] = None
    num_cliente: Optional[str] = None
    bairro_cliente: Optional[str] = None
    cidade_cliente: Optional[str] = None
    uf_cliente: Optional[str] = None
    cep_cliente: Optional[str] = None
    telefone_cliente: Optional[str] = None
    telefone_rec_cliente: Optional[str] = None
    whatsapp_cliente: Optional[str] = None
    fornecedor_cliente: Optional[str] = None
    email_funcionario: Optional[str] = None
    acao: Optional[str] = None
    usuario_id: int  # O campo 'usuario_id' é obrigatório

# Schema para criar cliente
class ClienteCreateSchema(ClienteBaseSchema):
    pass  # Para criação, podemos usar o schema base, sem modificações

# Schema para atualizar cliente
class ClienteUpdateSchema(ClienteBaseSchema):
    pass  # Para atualização, também usamos o schema base

# Schema para retornar cliente com todos os campos (inclusão de ID, datas e relacionamentos)
class ClienteSchema(ClienteBaseSchema):
    id: int
    data_cadastro_cliente: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True  # Essencial para trabalhar com objetos SQLAlchemy

# Schema para listagem de clientes (sem detalhes completos)
class ClienteListSchema(BaseModel):
    id: int
    nome_cliente: str
    tipo_cliente: Optional[str] = None
    cidade_cliente: Optional[str] = None
    telefone_cliente: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True  # Essencial para trabalhar com objetos SQLAlchemy
