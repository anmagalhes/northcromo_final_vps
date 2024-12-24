# app/models/cliente.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app import db  

class Cliente(db.Model):
    __tablename__ = 'clientes'  # Nome da tabela no banco de dados

    id = db.Column(db.Integer, primary_key=True)  # ID do Cliente (obrigatório)
    
    # Colunas obrigatórias
    tipo_cliente = db.Column(db.String(50), nullable=True)  # Tipo de Cliente
    nome_cliente = db.Column(db.String(100), nullable=True)  # Nome do Cliente
    doc_cliente = db.Column(db.String(20), nullable=True)  # Documento do Cliente (CPF/CNPJ)
    endereco_cliente = db.Column(db.String(255), nullable=True)  # Endereço do Cliente
    num_cliente = db.Column(db.String(20), nullable=True)  # Número do endereço
    bairro_cliente = db.Column(db.String(100), nullable=True)  # Bairro
    cidade_cliente = db.Column(db.String(100), nullable=True)  # Cidade
    uf_cliente = db.Column(db.String(2), nullable=True)  # UF
    cep_cliente = db.Column(db.String(10), nullable=True)  # CEP
    telefone_cliente = db.Column(db.String(20), nullable=True)  # Telefone do Cliente
    
    # Colunas que podem ser nulas (não obrigatórias)
    telefone_rec_cliente = db.Column(db.String(20), nullable=True)  # Telefone de recado
    whatsapp_cliente = db.Column(db.String(20), nullable=True)  # WhatsApp
    email_funcionario = db.Column(db.String(100), nullable=True)  # E-mail do Funcionário responsável
    acao = db.Column(db.String(255), nullable=True)  # Ação/observações adicionais
    fornecedor_cliente = db.Column(db.String(100), nullable=True)  # Fornecedor associado ao cliente

    # Colunas de datas
    data_cadastro_cliente = db.Column(db.DateTime, default=datetime.utcnow)  # Data de cadastro
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Data de criação
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)  # Data de atualização
    usuario_id = db.Column(db.Integer, ForeignKey('usuario.id'))  # Chave estrangeira de usuários

    # Relacionamentos
    usuario = relationship("User", back_populates="clientes", lazy='joined')
    #recebimentos = relationship("Recebimento", back_populates="cliente", lazy='select')
    #checklists = relationship("ChecklistRecebimento", back_populates="cliente", lazy='select')

    def __repr__(self):
        return f'<Cliente {self.nome_cliente}>'

    def to_json(self):
        return {
            "id": self.id,
            "tipo_cliente": self.tipo_cliente,
            "nome_cliente": self.nome_cliente,
            "doc_cliente": self.doc_cliente,
            "endereco_cliente": self.endereco_cliente,
            "num_cliente": self.num_cliente,
            "bairro_cliente": self.bairro_cliente,
            "cidade_cliente": self.cidade_cliente,
            "uf_cliente": self.uf_cliente,
            "cep_cliente": self.cep_cliente,
            "telefone_cliente": self.telefone_cliente,
            "telefone_rec_cliente": self.telefone_rec_cliente,
            "whatsapp_cliente": self.whatsapp_cliente,
            "data_cadastro_cliente": self.data_cadastro_cliente,
            "fornecedor_cliente": self.fornecedor_cliente,
            "email_funcionario": self.email_funcionario,
            "acao": self.acao,
            "usuario_id": self.usuario_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

