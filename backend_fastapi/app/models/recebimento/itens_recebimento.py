# app/models/recebimento/itens_recebimento.py
from datetime import datetime
import pytz
from sqlalchemy import (
    Enum,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Boolean,
    Text,
    Date,
    Float,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.config import settings
from typing import Optional, List
import enum


# Importe explicitamente a classe Funcionario aqui
from app.models.produto import Produto
from app.models.funcionario import Funcionario
from app.models.recebimento.recebimento import Recebimento

# Definindo o Enum de StatusOrdem
class StatusOrdem(enum.Enum):
    PENDENTE = 1  # Status 1 - Pendente
    FINALIZADO = 5  # Status 5 - Finalizado
    CANCELADO = 3  # Status 3 - Cancelado
    EM_ANDAMENTO = 2  # Status 2 - Em Andamento


class ItensRecebimento(settings.Base):
    __tablename__ = "itens_recebimento"
    __table_args__ = {"extend_existing": True}

    # Definindo a chave primária do item de recebimento
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Relacionamento com o modelo User (usando tipagem de string)
    produto_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("produtos.id"), nullable=True
    )  # Tabela Campo

    # Relacionamento MANY-TO-ONE de Grupo_Produto para User (não 'Usuario')
    produto: Mapped["Produto"] = relationship(
        "Produto",  # Referência correta à classe 'User'
        back_populates="itens_recebimento",  # Nome do campo de volta no User
        cascade="all, delete", 
    )

    # Relacionamento com o modelo User (usando tipagem de string)
    recebimento_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("recebimentos.id"), nullable=True
    )  # Tabela Campo

    # Relacionamento MANY-TO-ONE de Grupo_Produto para User (não 'Usuario')
    recebimento: Mapped["Recebimento"] = relationship(
        "Recebimento",  # Referência correta à classe 'User'
        back_populates="itens",  # Nome do campo de volta no User
    )

    # Relacionamento com o modelo User (usando tipagem de string)
    funcionario_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("funcionarios.id"), nullable=True
    )  # Tabela Campo

    # Relacionamento MANY-TO-ONE de Grupo_Produto para User (não 'Usuario')
    funcionario: Mapped["Funcionario"] = relationship(
        "Funcionario",  # Referência correta à classe 'User'
        back_populates="itens_recebimento",  # Nome do campo de volta no User
        cascade="all, delete", 
    )

    # Campos adicionais para armazenar a quantidade, preço unitário e preço total
    qtd_produto: Mapped[int] = mapped_column(Integer, nullable=False)
    preco_unitario: Mapped[float] = mapped_column(Float, nullable=False)
    preco_total: Mapped[float] = mapped_column(Float, nullable=False)
    referencia_produto: Mapped[str | None] = mapped_column(Text, nullable=False)

    # Adicionando o campo status_ordem como ENUM, mas armazenando o valor inteiro no banco
    status_ordem: Mapped[StatusOrdem] = mapped_column(
        Enum(StatusOrdem), nullable=False, default=StatusOrdem.PENDENTE
    )

    def __repr__(self):
        # Representação amigável do objeto, para exibição no log ou debug
        return f"<ItensRecebimento id={self.id} produto={self.produto.nome_produto} quantidade={self.quantidade}>"
