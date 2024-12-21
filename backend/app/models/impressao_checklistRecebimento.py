from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from .db import db

class ImpressaoChecklistRecebimento(db.Model):
    __tablename__ = 'impressao_checklist_recebimento'

    # Definição das colunas
    id = db.Column(db.Integer, primary_key=True)  # Chave primária
    id_checklist = db.Column(db.Integer, ForeignKey('checklist_recebimento.id'), nullable=False)  # Chave estrangeira para 'checklist_recebimento'
    nome_cliente = db.Column(db.String(100), nullable=False)
    qtd_produto = db.Column(db.Numeric(10, 2), nullable=False)
    nome_produto = db.Column(db.String(100), nullable=False)
    referencia_produto = db.Column(db.String(50), nullable=False)
    nota_interna = db.Column(db.String(50), nullable=True)
    queixa_cliente = db.Column(db.String(255), nullable=True)
    data_rec_ordem_servicos = db.Column(db.DateTime, nullable=False)
    usuario_id = db.Column(db.Integer, ForeignKey('usuario.id'), nullable=False)  # Chave estrangeira para 'usuario'
    link_pdf_checklist = db.Column(db.String(255), nullable=True)
    recebimento_id = db.Column(db.Integer, db.ForeignKey('recebimentos.id'))  # Chave estrangeira para Recebimento

    # Relacionamentos
    checklist = db.relationship('ChecklistRecebimento', backref='impressao_checklists', lazy=True)
    recebimento = db.relationship('Recebimento', backref='impressao_checklists', lazy=True)  # relacionamento com a tabela 'recebimentos'

    # Relacionamento com o usuário
    usuario = db.relationship('User', back_populates='impressao_checklists', foreign_keys=[usuario_id], lazy='joined')

    # Colunas de controle de data
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<ImpressaoChecklistRecebimento id={self.id} nome_cliente={self.nome_cliente}>'
