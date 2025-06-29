from __future__ import annotations
from datetime import datetime, date
from typing import Optional, List
from sqlalchemy import ForeignKey, Integer, String, DateTime, Text, Date, Enum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.api.models.base import Base
from app.api.models.enums import StatusTarefaEnum
from app.utils.datetime import utcnow
from app.api.models.mixins import TimestampMixin


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.api.models.checklist_recebimento import ChecklistRecebimento
    from app.api.models.notafiscal import NotaFiscal
    from app.api.models.cliente import Cliente


class Tarefa(Base, TimestampMixin):
    __tablename__ = "tarefas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    recebimento_id: Mapped[int] = mapped_column(
        ForeignKey("recebimentos.id", ondelete="CASCADE"),
        nullable=False, index=True
    )

    data_rec_ordem: Mapped[datetime] = mapped_column(
            DateTime(timezone=True),
            default=utcnow,
            nullable=False,
            server_default=func.now(),
            comment="Data e hora do recebimento automático"
        )

    #id_cliente: Mapped[int]           = mapped_column(Integer, nullable=False)
    qtde_servico: Mapped[int]         = mapped_column(Integer, nullable=False)
    id_servico: Mapped[int]           = mapped_column(Integer, nullable=False)
    id_servico2: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    id_operacao: Mapped[int]          = mapped_column(Integer, nullable=False)
    desc_servico_produto: Mapped[str] = mapped_column(String(255), nullable=True)
    obs: Mapped[Optional[str]]        = mapped_column(Text, nullable=True)
    status: Mapped[StatusTarefaEnum]  = mapped_column(Enum(StatusTarefaEnum), default=StatusTarefaEnum.PENDENTE)
    data_lancamento: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    referencia_produto: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    nota_interna: Mapped[Optional[str]]      = mapped_column(Text, nullable=True)
    data_checklist_ordem: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    # Relacionamento
    recebimento: Mapped["Recebimento"] = relationship(back_populates="tarefas")

    def __repr__(self):
        return f"<Tarefa id={self.id} recebimento_id={self.recebimento_id} status={self.status}>"

