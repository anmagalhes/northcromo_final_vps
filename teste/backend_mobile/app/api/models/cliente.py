# app/models/cliente.py
from __future__ import annotations
from sqlalchemy import Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import ForeignKey

from app.utils.datetime import utcnow
from app.api.models.mixins import TimestampMixin
from app.api.models.base import Base
from typing import Optional, List

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.api.models.fornecedor import Fornecedor
    from app.api.models.recebimento import Recebimento

class Cliente(Base, TimestampMixin):
    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Identificador único do cliente"
    )

    tipo_cliente: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        comment="Tipo de cliente: CPF ou CNPJ"
    )

    nome_cliente: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Nome do cliente"
    )

    doc_cliente: Mapped[str] = mapped_column(
        String(18),  # 11 caracteres para CPF e 18 para CNPJ
        nullable=False,
        unique=True,
        comment="Documento do cliente (CPF ou CNPJ)"
    )

    endereco_cliente: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
        comment="Endereço do cliente"
    )

    num_cliente: Mapped[str] = mapped_column(
        String(20),
        nullable=True,
        comment="Número do endereço do cliente"
    )

    bairro_cliente: Mapped[str] = mapped_column(
        String(100),
        nullable=True,
        comment="Bairro do cliente"
    )

    cidade_cliente: Mapped[str] = mapped_column(
        String(100),
        nullable=True,
        comment="Cidade do cliente"
    )

    uf_cliente: Mapped[str] = mapped_column(
        String(2),
        nullable=True,
        comment="Estado (UF) do cliente"
    )

    cep_cliente: Mapped[str] = mapped_column(
        String(10),
        nullable=True,
        comment="CEP do cliente"
    )

    telefone_cliente: Mapped[str] = mapped_column(
        String(20),
        nullable=True,
        comment="Telefone do cliente"
    )

    telefone_rec_cliente: Mapped[str] = mapped_column(
        String(20),
        nullable=True,
        comment="Telefone de referência do cliente"
    )

    whatsapp_cliente: Mapped[str] = mapped_column(
        String(20),
        nullable=True,
        comment="WhatsApp do cliente"
    )

    email_cliente: Mapped[str] = mapped_column(
        String(100),
        nullable=True,
        comment="Email do cliente"
    )

    data_cadastro_cliente: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utcnow,
        nullable=False,
        server_default=func.now(),
        comment="Data de cadastro do cliente"
    )

    fornecedor_cliente_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("fornecedores.id", ondelete="CASCADE"),
        nullable=True,
        comment="ID do fornecedor associado ao cliente, caso aplicável"
    )

    # Relacionamento com Fornecedor
    fornecedor_cliente: Mapped[Fornecedor] = relationship("Fornecedor", back_populates="clientes")

    recebimentos: Mapped[List["Recebimento"]] = relationship(
    "Recebimento",
    back_populates="cliente",  # deve ser exatamente o mesmo nome usado no relacionamento inverso
    cascade="all, delete-orphan"
)


    def __repr__(self):
        return f"<Cliente(id={self.id}, nome={self.nome_cliente}, doc={self.doc_cliente})>"

