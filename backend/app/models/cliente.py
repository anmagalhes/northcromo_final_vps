from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import db  # Importando a instância do db

class Cliente(db.Model):
    __tablename__ = 'clientes'  # Nome da tabela no banco de dados

    id = db.Column(db.Integer, primary_key=True)  # ID do Cliente (obrigatório)
    
    # Colunas obrigatórias
    tipo_cliente = db.Column(db.String(50), nullable=False)  # Tipo de Cliente
    nome_cliente = db.Column(db.String(100), nullable=False)  # Nome do Cliente
    doc_cliente = db.Column(db.String(20), nullable=False)  # Documento do Cliente (CPF/CNPJ)
    endereco_cliente = db.Column(db.String(255), nullable=False)  # Endereço do Cliente
    num_cliente = db.Column(db.String(20), nullable=False)  # Número do endereço
    bairro_cliente = db.Column(db.String(100), nullable=False)  # Bairro
    cidade_cliente = db.Column(db.String(100), nullable=False)  # Cidade
    uf_cliente = db.Column(db.String(2), nullable=False)  # UF
    cep_cliente = db.Column(db.String(10), nullable=False)  # CEP
    telefone_cliente = db.Column(db.String(20), nullable=False)  # Telefone do Cliente
    
    # Colunas que podem ser nulas (não obrigatórias)
    telefone_rec_cliente = db.Column(db.String(20), nullable=False)  # Telefone de recado
    whatsapp_cliente = db.Column(db.String(20), nullable=False)  # WhatsApp
    email_funcionario = db.Column(db.String(100), nullable=False)  # E-mail do Funcionário responsável
    acao = db.Column(db.String(255), nullable=True)  # Ação/observações adicionais
    fornecedor_cliente = db.Column(db.String(100), nullable=False)  # Fornecedor associado ao cliente

    # Colunas de datas
    data_cadastro_cliente = db.Column(db.DateTime, default=datetime.utcnow)  # Data de cadastro
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Data de criação
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)  # Data de atualização

    # Chave estrangeira para o usuário criador
    usuario_id = db.Column(db.Integer, ForeignKey('usuario.id'))  # Chave estrangeira de usuários

    # Relacionamentos
    usuario = relationship("Users", back_populates="clientes")  # Relacionamento com Usuários
    recebimentos = relationship("Recebimento", back_populates="cliente")
    checklists = relationship("ChecklistRecebimento", back_populates="cliente")

    def __repr__(self):
        return f'<Cliente {self.nome_cliente}>'
