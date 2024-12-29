#app/models/artigo.py
from typing import Optional
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import validates, relationship

from core.config import settings

class ArtigoModel(settings.Base):
    __tablename__ = "artigos"
    __table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True, autoincrement=True)
    titutlo = Column(String(100))
    descricao = Column(String(100))
    usuario_id = Column(Integer, ForeignKey('usuario.id'))

     # Relacionamento com o modelo 'User' (usuário)
    criador = relationship(
        "User", 
        back_populates="artigos", 
        lazy="joined"
    )
    
    
  # Método __repr__ para a classe ArtigoModel
    def __repr__(self):
        return f'<Artigo {self.titutlo}>'