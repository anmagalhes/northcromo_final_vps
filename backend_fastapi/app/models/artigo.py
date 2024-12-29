from typing import Optional
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from core.config import settings

class ArtigoModel(settings.Base):
    __tablename__ = "artigos"
    __table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True, autoincrement=True)
    titutlo = Column(String(100))
    descricao = Column(String(100))
    usuario_id = Column(Integer, ForeignKey('usuario.id'))
    criador = relationship(
        "User" back_populates="artigos", lazy= 'joined'
    )


