from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from uuid import uuid4
from datetime import datetime

# Modelo para a Ordem
class Order(Base):
    __tablename__ = 'orders'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))  # ID único para a ordem
    description = Column(String(255), nullable=False)  # Descrição da ordem
    created_at = Column(Integer, default=lambda: int(datetime.now().timestamp()))  # Timestamp de criação

    # Relacionamento com o modelo de Foto
    photos = relationship("Photo", back_populates="order")
