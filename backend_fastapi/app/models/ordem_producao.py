# app/models/OrdemProducao.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.database import Base


class OrdemProducao(Base):
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
