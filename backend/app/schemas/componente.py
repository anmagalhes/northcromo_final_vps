from marshmallow import Schema, fields, post_load
from .models import Componente, Defeito, Produto, Users

class ComponenteSchema(Schema):
    id = fields.Int(dump_only=True)  # Exclui do input (somente leitura)
    name = fields.Str(required=True)  # Nome do Componente
    usuario_id = fields.Int()  # Chave estrangeira para Usuário

    # Relacionamentos
    usuario = fields.Nested('UserSchema', dump_only=True)  # Exibe dados do usuário relacionado
    defeitos = fields.List(fields.Nested('DefeitoSchema', dump_only=True))  # Relacionamento com defeitos
    produtos = fields.List(fields.Nested('ProdutoSchema', dump_only=True))  # Relacionamento com produtos

    # Timestamps
    created_at = fields.DateTime(dump_only=True)  # Data de criação
    updated_at = fields.DateTime(dump_only=True)  # Data de atualização
    deleted_at = fields.DateTime(dump_only=True)  # Data de exclusão (opcional)

    @post_load
    def make_componente(self, data, **kwargs):
        """Converte o schema em um objeto da model Componente"""
        return Componente(**data)
