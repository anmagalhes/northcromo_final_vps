# app/models/OrdemProducao.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON, ForeignKey, Numeric, Boolean
from typing import List, Optional

from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates

from app.core.config import settings

class OrdemProducao(settings.Base):
    __tablename__ = "ordem_producao"
    __table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True, index=True)
    numero = Column(String, unique=True, index=True)
    descricao = Column(String)
    data_criacao = Column(DateTime)
    recebimento = Column(DateTime)
    status = Column(String, default="Pendente")

    # Relacionamento com Tarefa
    tarefas = relationship('Tarefa', back_populates='ordem_producao')
