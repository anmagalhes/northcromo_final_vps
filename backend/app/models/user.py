# models/user.py
from datetime import datetime  # Importando o datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import validates  # Importando o 'validates' para validações
from .db import db  # Importa a instância do db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Data de criação
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Data de última atualização
    deleted_at = db.Column(db.DateTime, nullable=True)  # Data de exclusão (soft delete)

    def __repr__(self):
        return f'<User {self.username}>'
    
    @validates('created_at')
    def validate_created_at(self, key, value):
        """Valida e define o created_at"""
        return value or datetime.utcnow()

    @validates('updated_at')
    def validate_updated_at(self, key, value):
        """Valida e define o updated_at"""
        return value or datetime.utcnow()
    