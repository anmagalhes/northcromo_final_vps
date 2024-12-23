#app/modesl/produto.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.database import db  # Instância db

class Produto(db.Model):
    __tablename__ = 'produtos'

    id = db.Column(db.Integer, primary_key=True)
    cod_produto = db.Column(db.Integer, unique=True, nullable=False)
    nome_produto = db.Column(db.String(100), nullable=False)
    id_grupo = db.Column(db.Integer, ForeignKey('grupo_produto.id'))
    id_operacao_servico = db.Column(db.Integer, ForeignKey('posto_trabalho.id'))
    und_servicos = db.Column(db.String(50), nullable=False)
    hora_peca_servicos = db.Column(db.Float, nullable=True)
    id_componente = db.Column(db.Integer, ForeignKey('componente.id'))
    id_posto_trabalho = db.Column(db.Integer, ForeignKey('posto_trabalho.id'))
    fornec_produto = db.Column(db.String(100), nullable=True)
    estomin_produto = db.Column(db.Integer, nullable=True)
    und_medida_produto = db.Column(db.String(20), nullable=False)
    valor_unid_produto = db.Column(db.Float, nullable=False)
    controle_produto = db.Column(db.Boolean, default=True)
    status_produto = db.Column(db.String(20), nullable=False)
    tipo_produto = db.Column(db.String(50), nullable=False)
    origem_produto = db.Column(db.String(50), nullable=True)
    foto_produto = db.Column(db.String(255), nullable=True)
    data_cadastro_produto = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_id = db.Column(db.Integer, ForeignKey('usuario.id'))
    tipo = db.Column(db.String(50), nullable=False)
    recebimento_id = db.Column(db.Integer, ForeignKey('recebimentos.id'))

    grupo_produto = relationship("Grupo_Produto", back_populates="produtos", lazy='joined')
    # Relacionamento com o posto de trabalho (id_posto_trabalho)
    posto_trabalho = relationship(
        "PostoTrabalho", 
        back_populates="produtos", 
        foreign_keys=[id_posto_trabalho],  # Especificando qual chave estrangeira utilizar
        lazy='joined'
    )
    # Relacionamento com operação de serviço (id_operacao_servico)
    operacao_servico = relationship(
        "PostoTrabalho", 
        back_populates="operacao_servico", 
        foreign_keys=[id_operacao_servico],  # Especificando qual chave estrangeira utilizar
        lazy='joined'
    )

    componente = relationship("Componente", back_populates="produtos", lazy='joined')
    checklists = relationship("ChecklistRecebimento", back_populates="produto", lazy='joined')
    usuario = relationship("User", back_populates="produtos", lazy='joined')
    recebimentos = relationship("Recebimento", back_populates="produto", foreign_keys="Recebimento.cod_produto", lazy='joined')

    def __repr__(self):
        return f'<Produto id={self.id} nome={self.nome_produto}>'
