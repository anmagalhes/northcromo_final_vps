# app/utils.py

from sqlalchemy.orm import Session
from app.models import Photo

def get_next_sequence(order_id: str, db: Session):
    # Buscar o número total de fotos já associadas a essa ordem
    photo_count = db.query(Photo).filter(Photo.order_id == order_id).count()
    # A sequência será o próximo número após o número de fotos existentes
    return photo_count + 1
