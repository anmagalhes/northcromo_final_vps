# app/services/order_service.py
from typing import List

from sqlalchemy.orm import Session

from app.models.order import Order
from app.schema.order_schem import OrderSchema


def create_order(db: Session, order: OrderSchema) -> Order:
    db_order = Order(title=order.title, description=order.description)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def get_orders(db: Session, skip: int = 0, limit: int = 10) -> List[Order]:
    return db.query(Order).offset(skip).limit(limit).all()
