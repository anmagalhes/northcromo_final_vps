from models.checklist_Recebimento import ChecklistRecebimento
from app import db

def list_checklist():
    checklists = ChecklistRecebimento.query.all()
    return [checklist.to_dict() for checklist in checklists]

def get_checklist(id):
    checklist = ChecklistRecebimento.query.get(id)
    if checklist:
        return checklist.to_dict()
    return None

def create_checklist(data):
    checklist = ChecklistRecebimento(
        id_Recebimento=data['id_Recebimento'],
        id_cliente=data['id_cliente'],
        qtd_Produto=data['qtd_Produto'],
        cod_Produto=data['cod_Produto'],
        referencia_Produto=data['referencia_Produto'],
        Status_Checklist=data['Status_Checklist']
    )
    db.session.add(checklist)
    db.session.commit()
    return checklist.to_dict()

def update_checklist(id, data):
    checklist = ChecklistRecebimento.query.get(id)
    if checklist:
        checklist.Status_Checklist = data.get('Status_Checklist', checklist.Status_Checklist)
        db.session.commit()
        return checklist.to_dict()
    return None

def delete_checklist(id):
    checklist = ChecklistRecebimento.query.get(id)
    if checklist:
        db.session.delete(checklist)
        db.session.commit()
        return True
    return False

