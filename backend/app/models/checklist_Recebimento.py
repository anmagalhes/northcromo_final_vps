from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import db

class ChecklistRecebimento(db.Model):
    __tablename__ = 'checklist_recebimento'

    id = db.Column(db.Integer, primary_key=True)
    id_Recebimento = db.Column(db.Integer, ForeignKey('recebimentos.id'), nullable=False)  # ID do recebimento
    id_cliente = db.Column(db.Integer, ForeignKey('clientes.id'), nullable=False)  # ID do cliente
    qtd_Produto = db.Column(Numeric(10, 2), nullable=False)  # Quantidade do produto
    cod_Produto = db.Column(db.Integer, ForeignKey('produtos.id'), nullable=False)  # Código do produto
    referencia_Produto = db.Column(db.String(50), nullable=False)  # Referência do produto
    notaInterna = db.Column(db.String(50), nullable=True)  # Nota interna (opcional)
    qUEIXA_CLIENTE = db.Column(db.String(255), nullable=True)  # Queixa do cliente (opcional)
    dataChecklist_OrdemServicos = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Data do checklist
    usuario_id = db.Column(db.Integer, ForeignKey('usuario.id'))  # Chave estrangeira de usuários
    LINK_PDF_CHECKLIST = db.Column(db.String(255), nullable=True)  # Link do PDF do checklist
    Status_Checklist = db.Column(db.String(50), nullable=False)  # Status do checklist (ex: 'Concluído', 'Em andamento', etc.)

    # Relacionamentos
    recebimento = relationship("Recebimento", back_populates="checklists")
    cliente = relationship("Cliente", back_populates="checklists")
    produto = relationship("Produto", back_populates="checklists")
    usuario = relationship("User", back_populates="checklists")
    impressao_checklists = relationship("ImpressaoChecklistRecebimento", backref="checklist")
    checklist = db.relationship('ChecklistRecebimento', backref='impressao_checklists')
    

    # Colunas de data e hora
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Data de criação
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Data de última atualização
    deleted_at = db.Column(db.DateTime, nullable=True)  # Data de exclusão (opcional para soft delete)

    def __repr__(self):
        return f'<ChecklistRecebimento {self.name}>'
