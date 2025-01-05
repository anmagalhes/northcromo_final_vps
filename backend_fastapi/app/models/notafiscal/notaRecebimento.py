#app/models/notafiscal/notaRecebimento.py
from sqlalchemy import Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.config import settings
from datetime import datetime
from typing import Optional, List

class NotaRecebimento(settings.Base):
    __tablename__ = "nota_recebimento"
    __table_args__ = {"extend_existing": True}

    # Chaves estrangeiras para NotaFiscal e Recebimento
    id_nota: Mapped[int] = mapped_column(Integer, ForeignKey("nota_fiscal.id_nota"), primary_key=True)
    recebimento_ordem: Mapped[int] = mapped_column(Integer, ForeignKey("recebimentos.id"), primary_key=True)
    
    def __repr__(self):
        return f"<NotaRecebimento id_nota={self.id_nota} recebimento_ordem={self.recebimento_ordem}>"