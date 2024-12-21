from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, Text, Numeric
from sqlalchemy.orm import relationship
from .db import db  # Instância db

class Produto(db.Model):
    __tablename__ = 'produtos'

    # Colunas do Produto
    id = db.Column(db.Integer, primary_key=True)
    cod_produto = db.Column(db.Integer, unique=True, nullable=False)  # Código do produto
    nome_produto = db.Column(db.String(100), nullable=False)
    id_grupo = db.Column(db.Integer, ForeignKey('grupo_produto.id'))  # Chave estrangeira para 'Grupo'
    id_operacao_servico = db.Column(db.Integer, ForeignKey('posto_trabalho.id'))  # Chave estrangeira para 'OperacaoServico'
    und_servicos = db.Column(db.String(50), nullable=False)  # Unidade de serviço
    hora_peca_servicos = db.Column(db.Float, nullable=True)  # Hora de serviço por peça
    id_componente = db.Column(db.Integer, ForeignKey('componente.id'))  # Chave estrangeira para 'Componente'
    id_posto_trabalho = db.Column(db.Integer, ForeignKey('postos_trabalho.id'))  # Chave estrangeira para 'PostoTrabalho'
    fornec_produto = db.Column(db.String(100), nullable=True)  # Fornecedor do produto
    estomin_produto = db.Column(db.Integer, nullable=True)  # Estoque mínimo do produto
    und_medida_produto = db.Column(db.String(20), nullable=False)  # Unidade de medida do produto
    valor_unid_produto = db.Column(db.Float, nullable=False)  # Valor unitário do produto
    controle_produto = db.Column(db.Boolean, default=True)  # Controle do produto (ativo ou inativo)
    status_produto = db.Column(db.String(20), nullable=False)  # Status do produto (ex: "Ativo", "Inativo")
    tipo_produto = db.Column(db.String(50), nullable=False)  # Tipo do produto
    origem_produto = db.Column(db.String(50), nullable=True)  # Origem do produto (ex: nacional, importado)
    foto_produto = db.Column(db.String(255), nullable=True)  # Foto do produto (URL ou caminho)
    data_cadastro_produto = db.Column(db.DateTime, default=datetime.utcnow)  # Data de cadastro
    usuario_id = db.Column(db.Integer, ForeignKey('usuario.id'))  # Chave estrangeira de usuários
    tipo = db.Column(db.String(50), nullable=False)  # Tipo de produto
    recebimento_id = db.Column(db.Integer, ForeignKey('recebimentos.id'))  # Chave estrangeira para recebimentos


    # Relacionamentos
    grupo = relationship("Grupo_Produto", back_populates="produtos", lazy='joined')  # Relacionamento com 'Grupo'
    operacao_servico = relationship("PostoTrabalho", back_populates="produtos", lazy='joined')  # Relacionamento com 'OperacaoServico'
    componente = relationship("Componente", back_populates="produtos", lazy='joined')  # Relacionamento com 'Componente'
    posto_trabalho = relationship('PostoTrabalho', back_populates='produtos', lazy='joined')  # Relacionamento com 'PostoTrabalho'
    checklists = relationship("ChecklistRecebimento", back_populates="produto", lazy='joined')
    usuario = relationship("User", back_populates='produto', foreign_keys=[usuario_id], lazy='joined')
    grupo_produto = relationship("Grupo_Produto", back_populates="produtos", lazy='joined')
    recebimentos = relationship("Recebimento", back_populates="produtos", lazy='joined')


    def __repr__(self):
        return f'<Produto id={self.id} name={self.nome}>'
