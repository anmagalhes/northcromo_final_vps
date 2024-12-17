from flask import Flask
from marshmallow import Schema, fields
from models import StoreModel, ItemModel
from db import db

# Schema para a loja (Store)
class StoreSchema(Schema):
    class Meta:
        # Aqui indicamos que queremos que o Marshmallow trabalhe com o modelo StoreModel
        fields = ("id", "name")  # Campos que queremos expor no schema

# Schema para o item (Item)
class ItemSchema(Schema):
    class Meta:
        fields = ("id", "name", "price", "store_id")  # Campos que queremos expor no schema

    # Definindo uma relação: Vamos incluir os dados da loja relacionada
    store = fields.Nested(StoreSchema)

