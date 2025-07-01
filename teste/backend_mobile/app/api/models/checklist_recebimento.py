from typing import Optional, List
from sqlalchemy import ForeignKey, Text, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.api.models.mixins import TimestampMixin
from app.api.models.base import Base

class ChecklistRecebimento(Base, TimestampMixin):
    __tablename__ = "checklist_recebimento"  # ou "checklist_recebimentos" — verifique nome exato

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    recebimento_id: Mapped[int] = mapped_column(ForeignKey("recebimentos.id", ondelete="CASCADE"))

    recebimento: Mapped["Recebimento"] = relationship("Recebimento", back_populates="checklist")

    item1: Mapped[bool] = mapped_column(default=False)
    item2: Mapped[bool] = mapped_column(default=False)
    observacoes: Mapped[Optional[str]] = mapped_column(Text)
    link_pdf: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    tarefas: Mapped[List["Tarefa"]] = relationship(
        "Tarefa",
        back_populates="checklist",  # <- CORRETO
        cascade="all, delete-orphan"
    )


def __repr__(self):
    link = "yes" if self.link_pdf else "no"
    return (
        f"<ChecklistRecebimento("
        f"id={self.id}, "
        f"recebimento_id={self.recebimento_id}, "
        f"item1={self.item1}, "
        f"item2={self.item2}, "
        f"link_pdf={link}"
        f")>"
    )
