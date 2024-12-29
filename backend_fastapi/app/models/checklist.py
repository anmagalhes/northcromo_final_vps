# app/models.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Checklist(Base):
    __tablename__ = "checklist"
    __table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    descricao = Column(String)
    tarefa_id = Column(Integer, ForeignKey("tarefa.id"))

    tarefa = relationship("Tarefa", back_populates="checklists")
