# cliente/schema.py
from marshmallow import Schema, fields, post_load, ValidationError
from datetime import datetime
from ..models import Cliente

# Função de validação para verificar se o usuário existe
def validate_usuario_id(value):
    from app.models import User
    # Verifica se o usuário com esse id existe
    user = User.query.get(value)
    if not user:
        raise ValidationError(f"Usuário com ID {value} não encontrado.")
    return value

class ClienteSchema(Schema):
    id = fields.Int(dump_only=True)  # Exclui do input (somente leitura)

    tipo_cliente = fields.Str(required=True)
    nome_cliente = fields.Str(required=True)
    doc_cliente = fields.Str(required=True)
    endereco_cliente = fields.Str(allow_none=True)
    num_cliente = fields.Str(allow_none=True)
    bairro_cliente = fields.Str(allow_none=True)
    cidade_cliente = fields.Str(allow_none=True)
    uf_cliente = fields.Str(allow_none=True)
    cep_cliente = fields.Str(allow_none=True)
    telefone_cliente = fields.Str(allow_none=True)
    telefone_rec_cliente = fields.Str(allow_none=True)
    whatsapp_cliente = fields.Str(allow_none=True)

    # Timestamps
    data_cadastro_cliente = fields.DateTime(dump_only=True, default=datetime.utcnow)  # Usado para exibir apenas
    fornecedor_cliente = fields.Str(allow_none=True)
    email_funcionario = fields.Str(allow_none=True)
    acao = fields.Str(allow_none=True)
    usuario_id = fields.Int(validate=validate_usuario_id, required=True)

    # Relacionamentos com 'usuario', 'recebimentos' e 'checklists', limitando os campos
    usuario = fields.Nested('UserSchema', only=["id", "username"], dump_only=True)
    recebimentos = fields.List(fields.Nested('RecebimentoSchema', only=["id", "valor"], dump_only=True))
    checklists = fields.List(fields.Nested('ChecklistRecebimentoSchema', only=["id", "status"], dump_only=True))

    # Timestamps
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @post_load
    def make_cliente(self, data, **kwargs):
        """Converte o schema em um objeto da model Cliente"""
        return Cliente(**data)  # Isso cria uma instância de Cliente a partir dos dados validados
