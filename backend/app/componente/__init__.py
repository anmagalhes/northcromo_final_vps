from flask import Blueprint

# Criação do Blueprint para Componente
componente_blueprint = Blueprint('componente', __name__)

# Importa as rotas para o blueprint
from . import routes
