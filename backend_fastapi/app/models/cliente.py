# app/models/cliente.py
from datetime import datetime
import pytz
from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    Integer,
    String,
    ForeignKey,
    Column,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.config import settings
from typing import Optional, List


# Criando um timezone para São Paulo (UTC-3)
SP_TZ = pytz.timezone("America/Sao_Paulo")

# Função auxiliar para garantir o uso correto do timezone
def get_current_time_in_sp() -> datetime:
    return datetime.now(SP_TZ).astimezone(SP_TZ)


class Cliente(settings.Base):  # Substituímos db.Model por Base
    __tablename__ = "clientes"
    __table_args__ = {"extend_existing": True}  # Permite redefinir a tabela

    # Usando Mapped e mapped_column para definir as colunas
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    tipo_cliente: Mapped[Optional[str]] = mapped_column(String(50))  # Tipo de Cliente
    nome_cliente: Mapped[Optional[str]] = mapped_column(String(100))  # Nome do Cliente
    doc_cliente: Mapped[Optional[str]] = mapped_column(String(20))  # Documento do Cliente (CPF/CNPJ)
    endereco_cliente: Mapped[Optional[str]] = mapped_column(String(255))  # Endereço do Cliente
    num_cliente: Mapped[Optional[str]] = mapped_column(String(20))  # Número do endereço
    bairro_cliente: Mapped[Optional[str]] = mapped_column(String(100))  # Bairro
    cidade_cliente: Mapped[Optional[str]] = mapped_column(String(100))  # Cidade
    uf_cliente: Mapped[Optional[str]] = mapped_column(String(16))  # UF
    cep_cliente: Mapped[Optional[str]] = mapped_column(String(16))  # CEP
    telefone_cliente: Mapped[Optional[str]] = mapped_column(String(20))  # Telefone do Cliente

    # Colunas opcionais
    telefone_rec_cliente: Mapped[Optional[str]] = mapped_column(String(20))  # Telefone de recado
    whatsapp_cliente: Mapped[Optional[str]] = mapped_column(String(20))  # WhatsApp
    email_funcionario: Mapped[Optional[str]] = mapped_column(String(100))  # E-mail do Funcionário responsável
    acao: Mapped[Optional[str]] = mapped_column(String(255))  # Ação/observações adicionais
    fornecedor_cliente: Mapped[Optional[str]] = mapped_column(String(100))  # Fornecedor associado ao cliente

    # Relacionamento com o modelo User
    usuario_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("usuario.id"))  # Tabela Campo

    # Relacionamentos com Recebimentos e Checklist_Recebimento
    usuario: Mapped["User"] = relationship(
        "User",
        back_populates="clientes",
    )

    recebimentos: Mapped[List["Recebimento"]] = relationship(
        "Recebimento",
        back_populates="cliente",
    )

    checklists: Mapped[List["Checklist_Recebimento"]] = relationship(
        "Checklist_Recebimento",
        back_populates="cliente",
    )

    # Campos de auditoria
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=get_current_time_in_sp,  # timezone=True garante que seja "aware"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=get_current_time_in_sp,
        onupdate=get_current_time_in_sp,
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)  # Permite que seja None

    def __repr__(self):
        return f"<Cliente {self.nome_cliente}, ID {self.id}>"
