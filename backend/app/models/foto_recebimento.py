from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import db

class FotoRecebimento(db.Model):
    __tablename__ = 'foto_recebimento'  # Nome da tabela

    id = db.Column(db.Integer, primary_key=True)  # ID da Foto
    id_ordem = db.Column(db.String(50), nullable=False)  # ID da ordem (chave estrangeira)
    recebimento_id = db.Column(db.Integer, ForeignKey('recebimentos.id'), nullable=False)
    nome_foto = db.Column(db.String(255), nullable=False)  # Nome ou caminho do arquivo da foto
    
    # Relacionamento com a tabela Recebimento
    ordem = relationship("Recebimento", back_populates="fotos")

    # Adicionando as colunas de data e hora
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Data de criação
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Data de última atualização
    deleted_at = db.Column(db.DateTime, nullable=True)  # Data de exclusão (opcional para soft delete)

    def __repr__(self):
        return f'<FotoRecebimento {self.id_ordem} - {self.nome_foto}>'
