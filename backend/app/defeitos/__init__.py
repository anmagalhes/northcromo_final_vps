from flask import Blueprint

# Cria o blueprint para o módulo defeitos
defeito_blueprint = Blueprint('defeito', __name__)

# Importa as rotas que serão registradas no blueprint
from . import routes

