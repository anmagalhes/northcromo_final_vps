# app/models/notafiscal/notaFiscal.py
from sqlalchemy import Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.config import settings
from datetime import datetime


class NotaFiscal(settings.Base):
    __tablename__ = "nota_fiscal"
    __table_args__ = {"extend_existing": True}

    id_nota: Mapped[int] = mapped_column(Integer, primary_key=True)
    numero_nota: Mapped[str] = mapped_column(String(50), nullable=False)
    data_emissao: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
    valor_total: Mapped[float] = mapped_column(Float, nullable=False)

    # Relacionamento Muitos-para-Muitos com Recebimento
    recebimentos: Mapped[list["Recebimento"]] = relationship(
        "Recebimento",
        secondary="nota_recebimento",  # Tabela intermediária
        back_populates="notas_fiscais",  # Relacionamento reverso
    )

    def __repr__(self):
        return f"<NotaFiscal id_nota={self.id_nota} numero_nota={self.numero_nota}>"
