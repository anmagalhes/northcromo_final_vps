from marshmallow import Schema, fields, post_load
from .models import Cliente, Recebimento, ChecklistRecebimento, User

class ClienteSchema(Schema):
    id = fields.Int(dump_only=True)  # Exclui do input (somente leitura)
    tipo_cliente = fields.Str(required=True)  # Tipo de Cliente
    nome_cliente = fields.Str(required=True)  # Nome do Cliente
    doc_cliente = fields.Str(required=True)  # Documento do Cliente (CPF/CNPJ)
    endereco_cliente = fields.Str(required=True)  # Endereço do Cliente
    num_cliente = fields.Str(required=True)  # Número do endereço
    bairro_cliente = fields.Str(required=True)  # Bairro
    cidade_cliente = fields.Str(required=True)  # Cidade
    uf_cliente = fields.Str(required=True)  # UF
    cep_cliente = fields.Str(required=True)  # CEP
    telefone_cliente = fields.Str(required=True)  # Telefone do Cliente
    telefone_rec_cliente = fields.Str()  # Telefone de recado
    whatsapp_cliente = fields.Str()  # WhatsApp
    data_cadastro_cliente = fields.DateTime(dump_only=True, default=datetime.utcnow)  # Data de cadastro
    fornecedor_cliente = fields.Str(required=True)  # Fornecedor associado ao cliente
    email_funcionario = fields.Str()  # E-mail do Funcionário responsável
    acao = fields.Str()  # Ação/observações adicionais
    usuario_id = fields.Int()  # Chave estrangeira para usuário

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
