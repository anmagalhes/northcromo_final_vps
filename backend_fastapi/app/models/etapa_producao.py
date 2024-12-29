# app/models.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class EtapaProducao(Base):
    __tablename__ = "etapa_producao"
    __table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    ordem_producao_id = Column(Integer, ForeignKey("ordem_producao.id"))

    ordem_producao = relationship("OrdemProducao", back_populates="etapas")
