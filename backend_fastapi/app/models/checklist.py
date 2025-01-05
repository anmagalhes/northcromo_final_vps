from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.config import settings

class CheckList(settings.Base):
    __tablename__ = "checklists"
    __table_args__ = {"extend_existing": True}

    id_checklist: Mapped[int] = mapped_column(Integer, primary_key=True)
    descricao: Mapped[str] = mapped_column(String(255), nullable=False)
    data_criacao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    # Relacionamento com Recebimento
    id_ordem: Mapped[int] = mapped_column(Integer, ForeignKey("recebimentos.id_ordem"))
    recebimento: Mapped["Recebimento"] = relationship("Recebimento", back_populates="checklist")

    def __repr__(self):
        return f"<CheckList id_checklist={self.id_checklist} descricao={self.descricao}>"
