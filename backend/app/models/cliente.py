# app/models/cliente
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import db  # Importa o db corretamente de 'database.py'

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

    # Chave estrangeira para o usuário criador
    usuario_id = db.Column(db.Integer, ForeignKey('usuario.id'))  # Chave estrangeira de usuários

    # Relacionamentos
    usuario = relationship('User', back_populates='clientes')  # Correção: 'Users' -> 'User'
    recebimentos = relationship('Recebimento', back_populates='cliente')
    checklists = relationship('ChecklistRecebimento', back_populates='cliente')
    defeitos = db.relationship('Defeito', backref='cliente', lazy=True)

    def __repr__(self):
        return f'<Cliente {self.nome_cliente}>'
