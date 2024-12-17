# app/schemas/grupo_produto_schema.py

from marshmallow import Schema, fields, post_load
from app.models.grupo_produto import Grupo_Produto  # Certifique-se de que o nome da classe é "Grupo_Produto" (com G maiúsculo)

class Grupo_ProdutoSchema(Schema):
    # Definindo campos do schema
    id = fields.Int(dump_only=True)  # Campo somente leitura
    name = fields.Str(required=True)  # Nome do grupo de produto
    usuario_id = fields.Int()  # ID do usuário associado

    # Relacionamento com o modelo Usuario (assumindo que você tem o schema 'UserSchema')
    usuario = fields.Nested('UserSchema', dump_only=True)

    # Campos de timestamp
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    deleted_at = fields.DateTime(dump_only=True)

    @post_load
    def make_grupo_produto(self, data, **kwargs):
        """Converte os dados carregados em um objeto da model Grupo_Produto"""
        return Grupo_Produto(**data)  # Certifique-se de que o nome da classe é "Grupo_Produto" (com G maiúsculo)
    
# Instâncias do schema para uso
grupo_produto_schema = Grupo_ProdutoSchema()  # Para uma instância única
grupo_produtos_schema = Grupo_ProdutoSchema(many=True)  # Para várias instâncias
