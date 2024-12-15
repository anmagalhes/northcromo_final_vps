# checklist_recebimento/schema.py
from marshmallow import Schema, fields

class ChecklistRecebimentoSchema(Schema):
    id = fields.Int(dump_only=True)  # ID gerado automaticamente
    id_Recebimento = fields.Int(required=True)
    id_cliente = fields.Int(required=True)
    qtd_Produto = fields.Decimal(required=True)
    cod_Produto = fields.Int(required=True)
    referencia_Produto = fields.Str(required=True)
    notaInterna = fields.Str()
    queixa_cliente = fields.Str()
    data_checklist_ordem_servicos = fields.DateTime()
    usuario_id = fields.Int()
    link_pdf_checklist = fields.Str()
    status_checklist = fields.Str(required=True)

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    deleted_at = fields.DateTime(dump_only=True)

