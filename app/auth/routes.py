from flask import request, jsonify
from . import auth_blueprint
from .services import create_user, login_user

# Rota de registro
@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    username = data.get('username')
    password = data.get('password')
    
    if create_user(name, username, password):
        return jsonify({"message": "Usuário criado com sucesso!"}), 201
    else:
        return jsonify({"message": "Usuário já existe!"}), 400

# Rota de login
@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if login_user(username, password):
        return jsonify({"message": "Login bem-sucedido!"}), 200
    else:
        return jsonify({"message": "Credenciais inválidas!"}), 401
