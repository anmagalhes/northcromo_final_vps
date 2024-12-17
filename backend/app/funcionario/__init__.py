from flask import Blueprint

# Cria o blueprint para o módulo de funcionários
funcionario_blueprint = Blueprint('funcionario', __name__)

# Importa as rotas para registrá-las no blueprint
from . import routes
