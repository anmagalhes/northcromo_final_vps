from flask import Blueprint

# Cria o blueprint para o módulo cliente
cliente_blueprint = Blueprint('cliente', __name__)

# Importa as rotas que serão registradas no blueprint
from . import routes