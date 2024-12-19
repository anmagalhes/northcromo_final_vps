from flask import Blueprint

# Criar o Blueprint para autenticação
auth_blueprint = Blueprint('auth', __name__)

from . import routes  # Importando as rotas do auth
