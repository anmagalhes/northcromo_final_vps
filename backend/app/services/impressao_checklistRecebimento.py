# checklist_recebimento/services.py
from .models import ChecklistRecebimento
from .schema import ChecklistRecebimentoSchema
from ..impressao_checklistRecebimento import db

# Inicializando o schema
checklist_schema = ChecklistRecebimentoSchema()
checklists_schema = ChecklistRecebimentoSchema(many=True)

def create_checklist(data):
    # Cria um novo checklist de recebimento
    checklist = ChecklistRecebimento(
        id_Recebimento=data['id_Recebimento'],
        id_cliente=data['id_cliente'],
        qtd_Produto=data['qtd_Produto'],
        cod_Produto=data['cod_Produto'],
        referencia_Produto=data['referencia_Produto'],
        notaInterna=data.get('notaInterna'),
        queixa_cliente=data.get('queixa_cliente'),
        data_checklist_ordem_servicos=data.get('data_checklist_ordem_servicos'),
        usuario_id=data.get('usuario_id'),
        link_pdf_checklist=data.get('link_pdf_checklist'),
        status_checklist=data['status_checklist']
    )
    db.session.add(checklist)
    db.session.commit()
    return checklist_schema.dump(checklist)

def get_all_checklists():
    # Retorna todos os checklists de recebimento
    checklists = ChecklistRecebimento.query.all()
    return checklists_schema.dump(checklists)

def get_checklist_by_id(checklist_id):
    # Retorna um checklist específico pelo ID
    checklist = ChecklistRecebimento.query.get(checklist_id)
    if checklist:
        return checklist_schema.dump(checklist)
    return None

def update_checklist(checklist_id, data):
    # Atualiza um checklist existente
    checklist = ChecklistRecebimento.query.get(checklist_id)
    if checklist:
        checklist.id_Recebimento = data.get('id_Recebimento', checklist.id_Recebimento)
        checklist.id_cliente = data.get('id_cliente', checklist.id_cliente)
        checklist.qtd_Produto = data.get('qtd_Produto', checklist.qtd_Produto)
        checklist.cod_Produto = data.get('cod_Produto', checklist.cod_Produto)
        checklist.referencia_Produto = data.get('referencia_Produto', checklist.referencia_Produto)
        checklist.notaInterna = data.get('notaInterna', checklist.notaInterna)
        checklist.queixa_cliente = data.get('queixa_cliente', checklist.queixa_cliente)
        checklist.data_checklist_ordem_servicos = data.get('data_checklist_ordem_servicos', checklist.data_checklist_ordem_servicos)
        checklist.usuario_id = data.get('usuario_id', checklist.usuario_id)
        checklist.link_pdf_checklist = data.get('link_pdf_checklist', checklist.link_pdf_checklist)
        checklist.status_checklist = data.get('status_checklist', checklist.status_checklist)
        db.session.commit()
        return checklist_schema.dump(checklist)
    return None

def delete_checklist(checklist_id):
    # Exclui um checklist pelo ID
    checklist = ChecklistRecebimento.query.get(checklist_id)
    if checklist:
        db.session.delete(checklist)
        db.session.commit()
        return True
    return False
