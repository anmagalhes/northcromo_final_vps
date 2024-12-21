# cliente/schema.py
from marshmallow import Schema, fields, post_load
from ..models.cliente import Cliente
from datetime import datetime

class ClienteSchema(Schema):
    id = fields.Int(dump_only=True)  # Exclui do input (somente leitura)
    
    tipo_cliente = fields.Str(allow_none=True)  # Tipo de Cliente (pode ser nulo)
    nome_cliente = fields.Str(allow_none=True)  # Nome do Cliente (pode ser nulo)
    doc_cliente = fields.Str(allow_none=True)  # Documento do Cliente (pode ser nulo)
    endereco_cliente = fields.Str(allow_none=True)  # Endereço do Cliente (pode ser nulo)
    num_cliente = fields.Str(allow_none=True)  # Número do endereço (pode ser nulo)
    bairro_cliente = fields.Str(allow_none=True)  # Bairro (pode ser nulo)
    cidade_cliente = fields.Str(allow_none=True)  # Cidade (pode ser nulo)
    uf_cliente = fields.Str(allow_none=True)  # UF (pode ser nulo)
    cep_cliente = fields.Str(allow_none=True)  # CEP (pode ser nulo)
    telefone_cliente = fields.Str(allow_none=True)  # Telefone do Cliente (pode ser nulo)
    telefone_rec_cliente = fields.Str(allow_none=True)  # Telefone de recado (pode ser nulo)
    whatsapp_cliente = fields.Str(allow_none=True)  # WhatsApp (pode ser nulo)
    
    # Campos obrigatórios removidos, agora todos podem ser nulos.
    data_cadastro_cliente = fields.DateTime(dump_only=True, default=datetime.utcnow)  # Data de cadastro
    fornecedor_cliente = fields.Str(allow_none=True)  # Fornecedor associado ao cliente (pode ser nulo)
    email_funcionario = fields.Str(allow_none=True)  # E-mail do Funcionário responsável (pode ser nulo)
    acao = fields.Str(allow_none=True)  # Ação/observações adicionais (pode ser nulo)
    usuario_id = fields.Int(allow_none=True)  # Chave estrangeira para usuário (pode ser nulo)

    # Relacionamentos
    usuario = fields.Nested('UserSchema', dump_only=True)  # Exibe dados do usuário relacionado
    recebimentos = fields.List(fields.Nested('RecebimentoSchema', dump_only=True))  # Relacionamento com recebimentos
    checklists = fields.List(fields.Nested('ChecklistRecebimentoSchema', dump_only=True))  # Relacionamento com checklists

    # Timestamps
    created_at = fields.DateTime(dump_only=True)  # Data de criação
    updated_at = fields.DateTime(dump_only=True)  # Data de atualização

    @post_load
    def make_cliente(self, data, **kwargs):
        """Converte o schema em um objeto da model Cliente"""
        return Cliente(**data)

