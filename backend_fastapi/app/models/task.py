# app/models/task.py
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.config import settings


class Task(settings.Base):
    __tablename__ = "tasks"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String, nullable=True)
    status = Column(String, default="Pending")
    order_id = Column(Integer, ForeignKey("orders.id"))

    order = relationship("Order", back_populates="tasks")
