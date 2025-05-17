# app/create_db.py
from app.database import Base, engine
from app.models import order

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)
