from marshmallow import Schema, fields, post_load
from app.models.defeito import Defeito
from app.models.componente import Componente
from app.models.user import User

class DefeitoSchema(Schema):
    id = fields.Int(dump_only=True)  # Exclui do input (somente leitura)
    nome = fields.Str(required=True)  # Nome do defeito
    usuario_id = fields.Int()  # Chave estrangeira para o Usuário
    componente_id = fields.Int()  # Chave estrangeira para o Componente

    # Relacionamento com o Usuário
    usuario = fields.Nested('UserSchema', dump_only=True)  # Dados do usuário relacionados

    # Relacionamento com o Componente
    componente = fields.Nested('ComponenteSchema', dump_only=True)  # Dados do componente relacionados

    # Timestamps
    created_at = fields.DateTime(dump_only=True)  # Data de criação
    updated_at = fields.DateTime(dump_only=True)  # Data de atualização
    deleted_at = fields.DateTime(dump_only=True)  # Data de exclusão (opcional)

    @post_load
    def make_defeito(self, data, **kwargs):
        """Converte os dados carregados em um objeto da model Defeito"""
        return Defeito(**data)
