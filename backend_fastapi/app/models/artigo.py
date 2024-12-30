# app/models/artigo.py
from core.config import settings
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class ArtigoModel(settings.Base):
    __tablename__ = "artigos"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    titutlo = Column(String(100))
    descricao = Column(String(100))
    usuario_id = Column(Integer, ForeignKey("usuario.id"))

    # Relacionamento com o modelo 'User' (usuário)
    criador = relationship("User", back_populates="artigos", lazy="joined")

    # Método __repr__ para a classe ArtigoModel
    def __repr__(self):
        return f"<Artigo {self.titutlo}>"
