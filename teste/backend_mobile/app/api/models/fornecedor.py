#app/api/models/fornecedor.py
from __future__ import annotations
from sqlalchemy import Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.utils.datetime import utcnow
from app.api.models.mixins import TimestampMixin
from app.api.models.base import Base

class Fornecedor(Base, TimestampMixin):
    __tablename__ = "fornecedores"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Identificador único do fornecedor"
    )

    nome: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Nome do fornecedor"
    )

    cnpj: Mapped[str] = mapped_column(
        String(18),
        nullable=True,
        comment="CNPJ do fornecedor"
    )

    endereco: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
        comment="Endereço do fornecedor"
    )

    telefone: Mapped[str] = mapped_column(
        String(20),
        nullable=True,
        comment="Telefone do fornecedor"
    )

    email: Mapped[str] = mapped_column(
        String(100),
        nullable=True,
        comment="Email do fornecedor"
    )

    data_cadastro: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utcnow,
        nullable=False,
        server_default=func.now(),
        comment="Data de cadastro do fornecedor"
    )

    # Relacionamento com Produto (um fornecedor pode ter vários produtos)
    produtos: Mapped[list[Produto]] = relationship(
        "Produto",
        secondary="produto_fornecedor",  # tabela intermediária
        back_populates="fornecedores"
    )


 # Relacionamento inverso com Cliente
    clientes: Mapped[list[Cliente]] = relationship("Cliente", back_populates="fornecedor_cliente")


    def __repr__(self):
        return f"<Fornecedor(id={self.id}, nome={self.nome}, cnpj={self.cnpj})>"
