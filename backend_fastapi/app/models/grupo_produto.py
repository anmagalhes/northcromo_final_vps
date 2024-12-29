# app/models.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class GrupoProduto(Base):
    __tablename__ = "grupo_produto"  # Nome da tabela
    __table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)  # Nome do grupo de produto

    # Definindo a relação com Produto
    produtos = relationship("Produto", back_populates="grupo_produto")
