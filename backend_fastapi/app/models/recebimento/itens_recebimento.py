# app/models/recebimento/itens_recebimento.py

from sqlalchemy import Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.config import settings

class ItensRecebimento(settings.Base):
    __tablename__ = "itens_recebimento"
    __table_args__ = {"extend_existing": True}

    # Definindo a chave primária do item de recebimento
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Relacionamento com Produto
    id_produto: Mapped[int] = mapped_column(Integer, ForeignKey("produtos.id"), nullable=False)
    produto: Mapped["Produto"] = relationship("Produto", back_populates="itens_recebimento")
    
    # Relacionamento com Recebimento
    id_recebimento: Mapped[int] = mapped_column(Integer, ForeignKey("recebimentos.id"), nullable=False)
    recebimento: Mapped["Recebimento"] = relationship("Recebimento", back_populates="itens")

    # Campos adicionais para armazenar a quantidade, preço unitário e preço total
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False)
    preco_unitario: Mapped[float] = mapped_column(Float, nullable=False)
    preco_total: Mapped[float] = mapped_column(Float, nullable=False)

    def __repr__(self):
        # Representação amigável do objeto, para exibição no log ou debug
        return f"<ItensRecebimento id={self.id} produto={self.produto.nome_produto} quantidade={self.quantidade}>"
