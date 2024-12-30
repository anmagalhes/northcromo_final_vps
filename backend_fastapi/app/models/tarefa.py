# app/models/Tarefa.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.config import settings

class Tarefa(settings.Base):
    __tablename__ = "tarefa"
    __table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    descricao = Column(String)
    status = Column(String, default="Pendente")
    ordem_producao_id = Column(Integer, ForeignKey('ordem_producao.id'))

    ordem_producao = relationship('OrdemProducao', back_populates='tarefas')
