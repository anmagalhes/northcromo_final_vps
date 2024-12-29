# app/user/services.py
from sqlalchemy.orm import Session
from app.database import get_db
from fastapi import HTTPException, Depends

def create_user(name: str, username: str, password: str) -> bool:
    # A lógica de criação de usuário deve ser implementada aqui.
    # Verificar se o usuário já existe no banco
    db: Session = get_db()
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        return False
    # Caso contrário, crie o novo usuário
    new_user = User(name=name, username=username, password=password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return True

def login_user(username: str, password: str) -> bool:
    # A lógica de login de usuário deve ser implementada aqui.
    db: Session = get_db()
    user = db.query(User).filter(User.username == username).first()
    if user and user.password == password:
        return True
    return False

