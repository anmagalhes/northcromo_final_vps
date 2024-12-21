from datetime import datetime  # Importando o datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from .db import db

class Recebimento(db.Model):
    __tablename__ = 'recebimentos'

    id = db.Column(db.Integer, primary_key=True)
    id_ordem = db.Column(db.String(9), nullable=False)  # Número da ordem
    tipo_ordem = db.Column(db.String(4), nullable=False)
    id_cliente = db.Column(db.Integer, ForeignKey('clientes.id'), nullable=False)
    qtd_produto = db.Column(Numeric(10, 2), nullable=False) 
    cod_produto = db.Column(db.Integer, ForeignKey('produtos.id'), nullable=False)
    referencia_produto = db.Column(db.String(50), nullable=False)
    nota_interna = db.Column(db.String(50), nullable=True)
    vendedor_id = db.Column(db.Integer, ForeignKey('funcionarios.id'))
    queixa_cliente = db.Column(db.String(255), nullable=True)
    status_ordem = db.Column(db.String(50), nullable=True)
    data_cadastro = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    usuario_id = db.Column(db.Integer, ForeignKey('usuario.id'), nullable=False)

    # Relacionamentos
    cliente = relationship("Cliente", back_populates="recebimentos")
    produto = relationship("Produto", back_populates="recebimentos")
    # Relacionamento: Agora utilizando o nome correto da classe 'User' (não 'Usuario')
    usuario = relationship("User", back_populates='grupo_produtos', foreign_keys=[usuario_id], lazy='joined')

    ##fotos = relationship('FotoRecebimento', back_populates='ordem')
    funcionario = relationship('Funcionario', back_populates='recebimentos_cadastrados')
    checklists = relationship("ChecklistRecebimento", back_populates="recebimento")
    impressao_checklists = relationship("ImpressaoChecklistRecebimento", backref="recebimento")
    
    
    # Colunas de data e hora
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Data de criação
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Data de última atualização
    deleted_at = db.Column(db.DateTime, nullable=True)  # Data de exclusão (opcional para soft delete)

    def __repr__(self):
        return f'<Recebimento id={self.id} name={self.name}>'
