# checklist_recebimento/routes.py
from flask import request, jsonify
from . import checklist_recebimento_blueprint
from .services import create_checklist, get_all_checklists, get_checklist_by_id, update_checklist, delete_checklist

# Rota para listar todos os checklists
@checklist_recebimento_blueprint.route('/', methods=['GET'])
def get_checklists():
    checklists = get_all_checklists()
    return jsonify(checklists), 200

# Rota para obter um checklist pelo ID
@checklist_recebimento_blueprint.route('/<int:id>', methods=['GET'])
def get_checklist(id):
    checklist = get_checklist_by_id(id)
    if checklist:
        return jsonify(checklist), 200
    return jsonify({"message": "Checklist não encontrado!"}), 404

# Rota para criar um novo checklist
@checklist_recebimento_blueprint.route('/', methods=['POST'])
def create_new_checklist():
    data = request.get_json()
    checklist = create_checklist(data)
    return jsonify(checklist), 201

# Rota para atualizar um checklist
@checklist_recebimento_blueprint.route('/<int:id>', methods=['PUT'])
def update_checklist_route(id):
    data = request.get_json()
    checklist = update_checklist(id, data)
    if checklist:
        return jsonify(checklist), 200
    return jsonify({"message": "Checklist não encontrado!"}), 404

# Rota para deletar um checklist
@checklist_recebimento_blueprint.route('/<int:id>', methods=['DELETE'])
def delete_checklist_route(id):
    if delete_checklist(id):
        return jsonify({"message": "Checklist excluído com sucesso!"}), 200
    return jsonify({"message": "Checklist não encontrado!"}), 404
