# app/models/notafiscal/notaRecebimento.py
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.core.config import settings
from app.api.models.base import Base


class Nota_Recebimento(settings.Base):
    __tablename__ = "nota_recebimento"
    __table_args__ = {"extend_existing": True}

    # Chaves estrangeiras para NotaFiscal e Recebimento
    id_nota: Mapped[int] = mapped_column(
        Integer, ForeignKey("nota_fiscal.id_nota"), primary_key=True
    )

    recebimento_ordem: Mapped[int] = mapped_column(
        Integer, ForeignKey("recebimentos.id"), primary_key=True
    )

    def __repr__(self):
        return f"<Notarecebimento id_nota={self.id_nota} recebimento_ordem={self.recebimento_ordem}>"
