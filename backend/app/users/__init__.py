from flask import Blueprint

# Criar o Blueprint para usuários
users_blueprint = Blueprint('users', __name__)

from . import routes  # Importando as rotas de usuários
