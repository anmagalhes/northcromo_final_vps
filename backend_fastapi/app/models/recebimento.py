# app/models/recebiemnto.py
from datetime import datetime
import pytz

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Numeric,
    Float,
    DECIMAL,
    Text,
    Enum,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ARRAY

from app.core.config import settings

from typing import Optional, List

from enum import Enum as PyEnum
from app.models import User, Cliente, Produto, Funcionario, ChecklistRecebimento, ImpressaoChecklistRecebimento, FotoRecebimento


# Criando um timezone para São Paulo (UTC-3)
SP_TZ = pytz.timezone("America/Sao_Paulo")

# Definir a enumeração para os status da ordem
class StatusOrdem(PyEnum):
    EM_ANDAMENTO = "Em andamento"
    CONCLUIDO = "Concluído"
    CANCELADO = "Cancelado"


class Recebimento(settings.Base):  # Substituímos db.Model por Base
    __tablename__: str = "recebimentos"
    __table_args__ = {"extend_existing": True}  # Permite redefinir a tabela

    # Usando Mapped e mapped_column para definir as colunas
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_ordem: Mapped[int] = mapped_column(String(9), nullable=False)  # Número da ordem
    tipo_ordem: Mapped[int] = mapped_column(
        String(4), nullable=False, index=True
    )  # Tipo da ordem
    id_cliente: Mapped[int] = mapped_column(
        Integer, ForeignKey("clientes.id"), nullable=False
    )  # Chave estrangeira para Cliente
    qtd_produto: Mapped[float] = mapped_column(
        DECIMAL(10, 2), nullable=False
    )  # Quantidade do produto
    cod_produto: Mapped[int] = mapped_column(
        Integer, ForeignKey("produtos.id"), nullable=False
    )  # Chave estrangeira para Produto
    referencia_produto: Mapped[int] = mapped_column(
        String(50), nullable=False, index=True
    )  # Referência do produto
    nota_interna: Mapped[int] = mapped_column(
        String(50), nullable=False
    )  # Nota interna (opcional)
    vendedor_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("funcionarios.id")
    )  # Chave estrangeira para Funcionario
    queixa_cliente: Mapped[Text] = mapped_column(
        Text, nullable=False
    )  # Queixa do cliente (opcional)
    status_ordem: Mapped[StatusOrdem] = mapped_column(
        Enum(StatusOrdem), nullable=False, default=StatusOrdem.EM_ANDAMENTO
    )  # Usando Enum
    
    #usuario_id: Mapped[int] = mapped_column(
    #    Integer, ForeignKey("usuario.id"), nullable=False
    #)  # Chave estrangeira para Usuario

    # Colunas de data e hora
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(SP_TZ)
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(SP_TZ),
        onupdate=lambda: datetime.now(SP_TZ),
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True
    )  # Permite que seja None

    # Relacionamentos
    usuario: Mapped["User"] = relationship(
        "User",  # A classe 'User'
        back_populates="recebimentos",  # Ajuste do relacionamento no back_populates
        lazy="joined",
    )

    # Relacionamentos
    cliente: Mapped["Cliente"] = relationship(
        "Cliente", back_populates="recebimentos", lazy="joined"
    )
    produto: Mapped["Produto"] = relationship(
        "Produto",
        back_populates="recebimentos",
        foreign_keys=[cod_produto],
        lazy="joined",
    )
    
    #usuario: Mapped["User"] = relationship(
    #    "User",  # A classe 'User' está referenciada como uma string para evitar problemas de importação circular
    #    back_populates="grupos_produto",  # Relacionamento bidirecional
    #    lazy="joined",
    #)

    funcionario: Mapped["Funcionario"] = relationship(
        "Funcionario", back_populates="recebimentos_cadastrados", lazy="joined"
    )
    checklists: Mapped["ChecklistRecebimento"] = relationship(
        "ChecklistRecebimento", back_populates="recebimento", lazy="joined"
    )
    impressao_checklists: Mapped["ImpressaoChecklistRecebimento"] = relationship(
        "ImpressaoChecklistRecebimento", back_populates="recebimento", lazy="joined"
    )
    fotos: Mapped["FotoRecebimento"] = relationship(
        "FotoRecebimento", back_populates="ordem", lazy="joined"
    )

    # Representação string do modelo
    def __repr__(self) -> str:
        return f"<Recebimento(id={self.id}, id_ordem={self.id_ordem}, tipo_ordem={self.tipo_ordem})>"
