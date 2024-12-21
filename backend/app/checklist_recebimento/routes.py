# checklist_recebimento/routes.py

from flask import Blueprint, request, jsonify
from .services import list_checklist, get_checklist, create_checklist, update_checklist, delete_checklist

# Criando o Blueprint para o ChecklistRecebimento
checklist_recebimento_blueprint = Blueprint('checklist_recebimento', __name__)

# Rota para listar todos os checklists
@checklist_recebimento_blueprint.route('/', methods=['GET'])
def get_all_checklists():
    checklists = list_checklist()
    return jsonify(checklists)

# Rota para obter um checklist específico
@checklist_recebimento_blueprint.route('/<int:id>', methods=['GET'])
def get_single_checklist(id):
    checklist = get_checklist(id)
    if checklist:
        return jsonify(checklist)
    return jsonify({"message": "Checklist not found"}), 404

# Rota para criar um novo checklist
@checklist_recebimento_blueprint.route('/', methods=['POST'])
def create_new_checklist():
    data = request.get_json()
    new_checklist = create_checklist(data)
    return jsonify(new_checklist), 201

# Rota para atualizar um checklist existente
@checklist_recebimento_blueprint.route('/<int:id>', methods=['PUT'])
def update_checklist_info(id):
    data = request.get_json()
    updated_checklist = update_checklist(id, data)
    if updated_checklist:
        return jsonify(updated_checklist)
    return jsonify({"message": "Checklist not found"}), 404

# Rota para excluir um checklist
@checklist_recebimento_blueprint.route('/<int:id>', methods=['DELETE'])
def delete_checklist_info(id):
    deleted = delete_checklist(id)
    if deleted:
        return jsonify({"message": "Checklist deleted successfully"})
    return jsonify({"message": "Checklist not found"}), 404
