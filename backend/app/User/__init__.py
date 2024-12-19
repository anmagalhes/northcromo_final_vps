from flask import Blueprint

# Criar o Blueprint para usuários
users_blueprint = Blueprint('user', __name__)

# Importar as rotas do arquivo routes.pyss
from . import routes