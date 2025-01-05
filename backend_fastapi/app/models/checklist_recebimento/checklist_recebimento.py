# app/models/recebimento/recebimento.py
from datetime import datetime
import pytz
from sqlalchemy import (
    Enum,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.config import settings
from typing import Optional
import enum
from sqlalchemy import Enum as SQLEnum

# Criando um timezone para São Paulo (UTC-3)
SP_TZ = pytz.timezone("America/Sao_Paulo")


# Função auxiliar para garantir o uso correto do timezone
def get_current_time_in_sp() -> datetime:
    return datetime.now(SP_TZ).astimezone(
        SP_TZ
    )  # Garante que a data e hora sejam "aware"


# Enum para Status da Tarefa
class StatusTarefaEnum(enum.Enum):
    PENDENTE = "PENDENTE"
    EM_ANDAMENTO = "EM_ANDAMENTO"
    FINALIZADO = "FINALIZADO"


class Checklist_Recebimento(settings.Base):
    __tablename__ = "checklist_recebimentos"
    __table_args__ = {"extend_existing": True}

    # Campos básicos
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Campos relacionados a dados do checklist
    datarec_ordem_servicos: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    hora_inicial_ordem: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    cod_produto: Mapped[int] = mapped_column(
        Integer, nullable=False
    )  # Relacionamento com Produto
    nota_interna: Mapped[str] = mapped_column(String(20), nullable=False)
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False)
    referencia_produto: Mapped[str] = mapped_column(String(100), nullable=False)
    link: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )  # Link opcional
    observacao_checklist: Mapped[str] = mapped_column(
        Text, nullable=False
    )  # Observação do checklist
    status_tarefa: Mapped[StatusTarefaEnum] = mapped_column(
        SQLEnum(StatusTarefaEnum), default=StatusTarefaEnum.PENDENTE
    )
    data_checklist_ordem_servicos: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    # Relacionamento com Cliente
    cliente_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("clientes.id"), nullable=False
    )  # Relacionamento com Cliente

     # Relacionamento MANY-TO-ONE de Checklist para User
    cliente: Mapped["Cliente"] = relationship(
        "Cliente",  # Referência correta à classe 'User'
        back_populates="checklists",  # Nome do campo de volta no User
        lazy="joined",
    )

    # Relacionamento com o modelo User (usando tipagem de string)
    usuario_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("usuario.id"), nullable=True
    )  # Relacionamento opcional com o usuário responsável

    # Relacionamento MANY-TO-ONE de Checklist para User
    usuario: Mapped["User"] = relationship(
        "User",  # Referência correta à classe 'User'
        back_populates="checklists",  # Nome do campo de volta no User
        lazy="joined",
    )

    ordem_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("recebimentos.id"), nullable=True
    )

    # Relacionamento com Recebimento
    recebimento: Mapped["Recebimento"] = relationship(
        "Recebimento", back_populates="checklists", lazy="joined"
    )

    def __repr__(self):
        return f"<Checklist id={self.id} id_ordem={self.id_ordem}>"
