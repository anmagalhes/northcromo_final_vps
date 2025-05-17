# app/models/photo.py

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

# Modelo para Foto
class Photo(Base):
    __tablename__ = 'photos'

    id = Column(Integer, primary_key=True, autoincrement=True)  # ID único para a foto
    file_name = Column(String(255), nullable=False)  # Nome do arquivo da foto
    file_link = Column(String(255), nullable=False)  # Link para a foto
    order_id = Column(String(36), ForeignKey('orders.id'), nullable=False)  # Chave estrangeira para a ordem
    sequence = Column(Integer, nullable=False)  # Sequência da foto
    year = Column(Integer, nullable=False)  # Ano da foto

    # Relacionamento com o modelo de Ordem
    order = relationship("Order", back_populates="photos")
