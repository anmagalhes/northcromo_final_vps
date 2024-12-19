from marshmallow import Schema, fields, post_load
from app.models.foto_recebimento import FotoRecebimento

class FotoRecebimentoSchema(Schema):
    id = fields.Int(dump_only=True)  # Apenas para exibição
    id_ordem = fields.Str(required=True)  # ID da ordem
    recebimento_id = fields.Int(required=True)  # ID do recebimento
    nome_foto = fields.Str(required=True)  # Nome da foto
    usuario_id = fields.Int(required=False)  # ID do usuário (opcional)

    # Campos de data
    created_at = fields.DateTime(dump_only=True)  # Data de criação
    updated_at = fields.DateTime(dump_only=True)  # Data de última atualização
    deleted_at = fields.DateTime(dump_only=True)  # Data de exclusão (opcional)

    # Relacionamento com Recebimento e Usuário
    usuario = fields.Nested('UserSchema', only=["id", "name"], dump_only=True)  # Apenas o nome do usuário
    ordem = fields.Nested('RecebimentoSchema', only=["id", "id_ordem"], dump_only=True)  # Relacionamento com Recebimento

    # Função para carregar o objeto no banco após validação
    @post_load
    def make_foto_recebimento(self, data, **kwargs):
        return FotoRecebimento(**data)
