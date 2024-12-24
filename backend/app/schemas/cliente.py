# app/schemas/cliente.py
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional
from app.models import Cliente


# Função de validação para o usuário (no Pydantic)
def validate_usuario_id(value: int):
    from app.models import User
    user = User.query.get(value)
    if not user:
        raise ValueError(f"Usuário com ID {value} não encontrado.")
    return value


class ClienteSchema(BaseModel):
    id: Optional[int] = Field(None, alias="id_cliente")  # Para refletir o campo id da base de dados
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
    fornecedor_cliente: Optional[str] = None
    email_funcionario: Optional[str] = None
    acao: Optional[str] = None
    usuario_id: int

    # Timestamps (não será enviado no body, será apenas para exibição)
    data_cadastro_cliente: Optional[datetime] = Field(default_factory=datetime.utcnow)
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    # Validação para o usuário
    _validate_usuario_id = validator('usuario_id', allow_reuse=True)(validate_usuario_id)

    class Config:
        orm_mode = True  # Permite que o Pydantic converta objetos do SQLAlchemy para modelos Pydantic
