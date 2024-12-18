from flask import Blueprint

# Criar o Blueprint para usuários
users_blueprint = Blueprint('user', __name__)

# Importar as rotas do arquivo routes.py
from . import routes