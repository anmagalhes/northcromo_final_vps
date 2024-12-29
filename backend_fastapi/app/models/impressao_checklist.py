# app/models.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class ImpressaoChecklist(Base):
    __tablename__ = "impressao_checklist"
    __table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    descricao = Column(String)
    checklist_id = Column(Integer, ForeignKey("checklist.id"))

    checklist = relationship("Checklist")
