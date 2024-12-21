from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from .db import db

class Recebimento(db.Model):
    __tablename__ = 'recebimentos'

    id = db.Column(db.Integer, primary_key=True)
    id_ordem = db.Column(db.String(9), nullable=False)  # Número da ordem
    tipo_ordem = db.Column(db.String(4), nullable=False)  # Tipo da ordem
    id_cliente = db.Column(db.Integer, ForeignKey('clientes.id'), nullable=False)  # Chave estrangeira para Cliente
    qtd_produto = db.Column(Numeric(10, 2), nullable=False)  # Quantidade do produto
    cod_produto = db.Column(db.Integer, ForeignKey('produtos.id'), nullable=False)  # Chave estrangeira para Produto
    referencia_produto = db.Column(db.String(50), nullable=False)  # Referência do produto
    nota_interna = db.Column(db.String(50), nullable=True)  # Nota interna (opcional)
    vendedor_id = db.Column(db.Integer, ForeignKey('funcionarios.id'))  # Chave estrangeira para Funcionario
    queixa_cliente = db.Column(db.String(255), nullable=True)  # Queixa do cliente (opcional)
    status_ordem = db.Column(db.String(50), nullable=True)  # Status da ordem (opcional)
    data_cadastro = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Data de cadastro
    usuario_id = db.Column(db.Integer, ForeignKey('usuario.id'), nullable=False)  # Chave estrangeira para Usuario

    # Relacionamentos
    cliente = relationship("Cliente", back_populates="recebimentos", lazy='joined')  # Relacionamento com Cliente
    produto = relationship("Produto", back_populates="recebimentos", lazy='joined')  # Relacionamento com Produto
    usuario = relationship("User", back_populates="recebimentos", foreign_keys=[usuario_id], lazy='joined')  # Relacionamento com Usuario
    funcionario = relationship('Funcionario', back_populates='recebimentos_cadastrados', lazy='joined')  # Relacionamento com Funcionario
    checklists = relationship("ChecklistRecebimento", back_populates="recebimento", lazy='joined')  # Relacionamento com ChecklistRecebimento
    impressao_checklists = relationship("ImpressaoChecklistRecebimento", backref="recebimento", lazy='joined')  # Relacionamento com ImpressaoChecklistRecebimento
    
    # Colunas de data e hora
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Data de criação
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Data de última atualização
    deleted_at = db.Column(db.DateTime, nullable=True)  # Data de exclusão (opcional para soft delete

    def __repr__(self):
        return f'<Recebimento id={self.id} ordem={self.id_ordem}>'
