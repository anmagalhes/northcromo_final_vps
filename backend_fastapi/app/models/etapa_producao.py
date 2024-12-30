# app/models.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON, ForeignKey, Numeric
from typing import List, Optional

from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates

from app.core.config import settings

class EtapaProducao(settings.Base):
    __tablename__ = "etapa_producao"
    __table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    ordem_producao_id = Column(Integer, ForeignKey("ordem_producao.id"))

    ordem_producao = relationship("OrdemProducao", back_populates="etapas")
