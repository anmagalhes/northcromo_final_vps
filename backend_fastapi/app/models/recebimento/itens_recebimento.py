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
    PENDENTE = "PENDENTE"  # Status 1 - Pendente
    FINALIZADO = "FINALIZADO"  # Status 5 - Finalizado
    CANCELADO = "CANCELADO"  # Status 3 - Cancelado
    EM_ANDAMENTO = "EM_ANDAMENTO"


class ItensRecebimento(settings.Base):
    __tablename__ = "itens_recebimento"
    __table_args__ = {"extend_existing": True}

    # Definindo a chave primária do item de recebimento
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Campos adicionais para armazenar a quantidade, preço unitário e preço total
    qtd_produto: Mapped[int] = mapped_column(Integer, nullable=True)
    preco_unitario: Mapped[float] = mapped_column(Float, nullable=True)
    preco_total: Mapped[float] = mapped_column(Float, nullable=True)
    referencia_produto: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Adicionando o campo status_ordem como ENUM, mas armazenando o valor inteiro no banco
    status_ordem: Mapped[StatusOrdem] = mapped_column(
        Enum(StatusOrdem), nullable=True, default=StatusOrdem.PENDENTE
    )

    # Relacionamento com o modelo User (usando tipagem de string)
    produto_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("produtos.id"), nullable=True
    )  # Tabela Campo

    # Relacionamento MANY-TO-ONE de Grupo_Produto para User (não 'Usuario')
    produtos: Mapped["Produto"] = relationship(
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

    # Relacionamento com Fotos
    fotos: Mapped["FotoRecebimento"] = relationship(
        "FotoRecebimento", back_populates="item_recebimento"
    )

    def __repr__(self):
        # Representação amigável do objeto, para exibição no log ou debug
        return f"<ItensRecebimento id={self.id} produto={self.produto.id} quantidade={self.qtd_produto}>"

    def mudar_status(self, novo_status: StatusOrdem):
        """
        Altera o status do item de recebimento e, se o novo status for FINALIZADO ou CANCELADO,
        atualiza a data final da ordem.
        """
        if novo_status in [StatusOrdem.FINALIZADO, StatusOrdem.CANCELADO]:
            self.data_final_ordem = datetime.now(pytz.timezone("America/Sao_Paulo"))
        self.status_ordem = novo_status
