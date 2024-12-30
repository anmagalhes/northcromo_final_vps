# app/models.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.config import settings


class Produto(settings.Base):
    __tablename__ = "produto"
    __table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    descricao = Column(String)
    grupo_produto_id = Column(Integer, ForeignKey("grupo_produto.id"))

    # Relacionamento com GrupoProduto
    grupo_produto = relationship("GrupoProduto", back_populates="produtos")
