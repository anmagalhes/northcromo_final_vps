# app/models/order.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.config import settings


class Order(settings.Base):
    __tablename__ = 'orders'
    __table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)

    tasks = relationship("Task", back_populates="order")
